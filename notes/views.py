from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Note, TodoItem
from .forms import NoteForm, TodoForm
from notes_project.gemini_client import gemini_client
from django.contrib.auth.decorators import login_required

@login_required(login_url='accounts:login')
def home(request):
    """Home page showing user statistics and recent items"""
    if request.user.is_authenticated:
        total_notes = request.user.notes.count()
        total_todos = request.user.todos.count()
        completed_todos = request.user.todos.filter(completed=True).count()
        recent_notes = request.user.notes.all()[:5]
        recent_todos = request.user.todos.all()[:5]
        
        context = {
            'total_notes': total_notes,
            'total_todos': total_todos,
            'completed_todos': completed_todos,
            'recent_notes': recent_notes,
            'recent_todos': recent_todos,
        }
        return render(request, 'notes/home.html', context)
    return redirect('accounts:login')

@login_required(login_url='accounts:login')
def note_list(request):
    notes = request.user.notes.all()
    return render(request, 'notes/note_list.html', {'notes': notes})

@login_required(login_url='accounts:login')
def note_create(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user  # Add this line
            note.save()
            messages.success(request, 'Note created successfully! ✨')
            return redirect('note_list')
    else:
        form = NoteForm()
    return render(request, 'notes/note_form.html', {'form': form, 'title': 'Create Note'})

@login_required(login_url='accounts:login')
def note_edit(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, 'Note updated successfully! 💫')
            return redirect('note_list')
    else:
        form = NoteForm(instance=note)
    return render(request, 'notes/note_form.html', {'form': form, 'title': 'Edit Note', 'note': note})

@login_required(login_url='accounts:login')
def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == 'POST':
        note.delete()
        messages.success(request, 'Note deleted successfully! 💫')
        return redirect('note_list')
    return render(request, 'notes/note_confirm_delete.html', {'note': note})

@login_required(login_url='accounts:login')
def summarize_note(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    summary = gemini_client.summarize_note(note.content)
    
    # Store summary in session to show on note list
    request.session['last_summary'] = {
        'note_title': note.title,
        'summary': summary
    }
    messages.info(request, f'✨ AI summary generated for "{note.title}"!')
    
    return redirect('note_list')

@require_POST
def clear_summary(request):
    if 'last_summary' in request.session:
        del request.session['last_summary']
    return JsonResponse({'status': 'success'})

@login_required(login_url='accounts:login')
def todo_list(request):
    todos = request.user.todos.all().order_by('-created_at')
    return render(request, 'notes/todo_list.html', {'todos': todos})

@login_required(login_url='accounts:login')
def todo_create(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            messages.success(request, 'Todo created successfully! 🌟')
            return redirect('todo_list')
    else:
        form = TodoForm()
    return render(request, 'notes/todo_form.html', {'form': form, 'title': 'Create Todo'})

@login_required(login_url='accounts:login')
def todo_toggle(request, pk):
    todo = get_object_or_404(TodoItem, pk=pk, user=request.user)
    todo.completed = not todo.completed
    todo.save()
    
    status = "completed" if todo.completed else "marked incomplete"
    messages.success(request, f'Todo {status}! {"🎉" if todo.completed else "📝"}')
    
    return redirect('todo_list')

@login_required(login_url='accounts:login')
def todo_delete(request, pk):
    todo = get_object_or_404(TodoItem, pk=pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        messages.success(request, 'Todo deleted successfully! 🎉')
        return redirect('todo_list')
    return render(request, 'notes/todo_confirm_delete.html', {'todo': todo})

@login_required(login_url='accounts:login')
def suggest_todo(request):
    if request.method == 'POST':
        task_description = request.POST.get('task_description', '')
        suggestions = gemini_client.suggest_todo(task_description)
        return JsonResponse({'suggestions': suggestions})
    return JsonResponse({'error': 'Invalid request'})


# ── New AI Views ───────────────────────────────────────────────────────────────

@login_required(login_url='accounts:login')
def improve_note(request, pk):
    """Rewrite a note to be clearer or more formal."""
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == 'POST':
        style = request.POST.get('style', 'clear')
        improved = gemini_client.improve_note(note.content, style=style)
        return JsonResponse({'improved': improved})
    return JsonResponse({'error': 'Invalid request'})


@login_required(login_url='accounts:login')
def suggest_title(request):
    """Suggest a title based on note content typed so far."""
    if request.method == 'POST':
        content = request.POST.get('content', '')
        title = gemini_client.suggest_title(content)
        return JsonResponse({'title': title})
    return JsonResponse({'error': 'Invalid request'})


@login_required(login_url='accounts:login')
def detect_mood(request, pk):
    """Detect the mood/tone of a note."""
    note = get_object_or_404(Note, pk=pk, user=request.user)
    mood = gemini_client.detect_mood(note.content)
    return JsonResponse({'mood': mood})


@login_required(login_url='accounts:login')
def suggest_due_date(request):
    """Suggest a due date based on task description."""
    if request.method == 'POST':
        description = request.POST.get('description', '')
        due_date = gemini_client.suggest_due_date(description)
        if due_date:
            return JsonResponse({'due_date': due_date})
        return JsonResponse({'due_date': None, 'message': 'Could not determine a date'})
    return JsonResponse({'error': 'Invalid request'})


@login_required(login_url='accounts:login')
def weekly_digest(request):
    """Show the weekly AI digest page."""
    from django.utils import timezone
    from datetime import timedelta
    week_ago = timezone.now() - timedelta(days=7)

    notes = request.user.notes.filter(created_at__gte=week_ago).order_by('-created_at')
    # TodoItem has no updated_at — use created_at to find todos created this week
    # and check completed separately
    completed_todos = request.user.todos.filter(completed=True, created_at__gte=week_ago)
    pending_todos = request.user.todos.filter(completed=False).order_by('due_date')

    digest = gemini_client.generate_weekly_digest(
        request.user, notes, completed_todos, pending_todos
    )
    context = {
        'digest': digest,
        'notes': notes,
        'completed_todos': completed_todos,
        'pending_todos': pending_todos,
        'notes_count': notes.count(),
        'completed_count': completed_todos.count(),
        'pending_count': pending_todos.count(),
    }
    return render(request, 'notes/weekly_digest.html', context)