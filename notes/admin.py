import logging
from django.contrib import admin, messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
from django.conf import settings
from django.urls import path
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Note, TodoItem

logger = logging.getLogger(__name__)


# ── Email helper ───────────────────────────────────────────────────────────────

def _send_overdue_reminders(request):
    """
    Find all overdue, incomplete, not-yet-reminded todos and send one
    grouped email per user. Returns (sent_count, error_count, total_todos).
    """
    now = timezone.now()
    site_url = getattr(settings, 'SITE_URL', request.build_absolute_uri('/').rstrip('/'))
    todos_url = f'{site_url}/todos/'

    overdue = (
        TodoItem.objects
        .filter(completed=False, reminder_sent=False, due_date__lt=now)
        .exclude(user__email='')
        .select_related('user')
        .order_by('user_id', 'due_date')
    )

    if not overdue.exists():
        return 0, 0, 0

    todos_by_user = {}
    for todo in overdue:
        todos_by_user.setdefault(todo.user, []).append(todo)

    total = overdue.count()
    sent = errors = 0

    for user, todos in todos_by_user.items():
        subject = f'⏰ You have {len(todos)} overdue task{"s" if len(todos) > 1 else ""}!'
        context = {
            'user': user,
            'todos': todos,
            'todos_url': todos_url,
            'their_their': 'their' if len(todos) > 1 else 'its',
        }
        html_message = render_to_string(
            'accounts/emails/overdue_reminder_email.html', context
        )
        try:
            send_mail(
                subject=subject,
                message=strip_tags(html_message),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                html_message=html_message,
                fail_silently=False,
            )
            TodoItem.objects.filter(pk__in=[t.pk for t in todos]).update(reminder_sent=True)
            sent += 1
            logger.info('Overdue reminder sent to %s (%d todos)', user.email, len(todos))
        except Exception as e:
            errors += 1
            logger.error('Overdue reminder failed for %s: %s', user.email, e)

    return sent, errors, total


# ── Proxy model so we get a clean admin entry point ───────────────────────────

class OverdueReminderProxy(TodoItem):
    """Proxy used only to attach a custom admin page — no data is exposed."""
    class Meta:
        proxy = True
        verbose_name = 'Overdue Reminder'
        verbose_name_plural = 'Send Overdue Reminders'


@admin.register(OverdueReminderProxy)
class OverdueReminderAdmin(admin.ModelAdmin):
    """
    Admin page that shows overdue stats and a single send button.
    Users' notes and todos are never listed or accessible here.
    """

    # Disable all standard changelist/change views
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        # Allow access to our custom page only
        return request.user.is_staff

    # ── Custom URLs ────────────────────────────────────────────────────────────

    def get_urls(self):
        return [
            path(
                '',
                self.admin_site.admin_view(self.overdue_dashboard),
                name='notes_overduereminderproxy_changelist',
            ),
            path(
                'send/',
                self.admin_site.admin_view(self.send_reminders_view),
                name='notes_overduereminderproxy_send',
            ),
        ]

    # ── Dashboard view ─────────────────────────────────────────────────────────

    def overdue_dashboard(self, request):
        now = timezone.now()

        pending_count = TodoItem.objects.filter(
            completed=False, reminder_sent=False, due_date__lt=now
        ).exclude(user__email='').count()

        already_sent_count = TodoItem.objects.filter(
            completed=False, reminder_sent=True, due_date__lt=now
        ).count()

        affected_users = (
            TodoItem.objects
            .filter(completed=False, reminder_sent=False, due_date__lt=now)
            .exclude(user__email='')
            .values('user')
            .distinct()
            .count()
        )

        context = {
            **self.admin_site.each_context(request),
            'title': 'Send Overdue Reminders',
            'pending_count': pending_count,
            'already_sent_count': already_sent_count,
            'affected_users': affected_users,
            'opts': self.model._meta,
        }
        return render(request, 'admin/notes/overdue_reminder_dashboard.html', context)

    # ── Send action ────────────────────────────────────────────────────────────

    def send_reminders_view(self, request):
        if request.method != 'POST':
            return HttpResponseRedirect('../')

        sent, errors, total = _send_overdue_reminders(request)

        if total == 0:
            self.message_user(request, 'No overdue todos found that need reminders.', messages.INFO)
        else:
            if sent:
                self.message_user(
                    request,
                    f'✅ Sent reminder emails to {sent} user(s) covering {total} overdue todo(s).',
                    messages.SUCCESS,
                )
            if errors:
                self.message_user(
                    request,
                    f'❌ {errors} email(s) failed — check the server logs.',
                    messages.ERROR,
                )

        return HttpResponseRedirect('../')


# ── Keep Note and TodoItem OUT of the admin entirely ──────────────────────────
# (do not register them — users' data stays private)

admin.site.site_header = 'SparkleNotes Administration'
admin.site.site_title  = 'SparkleNotes Admin'
admin.site.index_title = 'Welcome to SparkleNotes Admin Portal'
