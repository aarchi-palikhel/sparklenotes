from django.contrib import admin
from .models import Note, TodoItem

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('title', 'content')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'content')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    # Display content preview in list view
    def content_preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Content Preview'

@admin.register(TodoItem)
class TodoItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'completed', 'created_at', 'due_date')
    list_filter = ('completed', 'created_at', 'due_date')
    search_fields = ('title', 'description')
    list_editable = ('completed',)  # Allow editing completion status directly from list view
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Task Information', {
            'fields': ('title', 'description', 'completed')
        }),
        ('Due Date', {
            'fields': ('due_date',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    # Custom action to mark selected todos as completed
    actions = ['mark_as_completed', 'mark_as_incomplete']
    
    def mark_as_completed(self, request, queryset):
        updated = queryset.update(completed=True)
        self.message_user(request, f'{updated} todo item(s) marked as completed.')
    mark_as_completed.short_description = "Mark selected todos as completed"
    
    def mark_as_incomplete(self, request, queryset):
        updated = queryset.update(completed=False)
        self.message_user(request, f'{updated} todo item(s) marked as incomplete.')
    mark_as_incomplete.short_description = "Mark selected todos as incomplete"

# Optional: You can also customize the admin site header and title
admin.site.site_header = "Notes App Administration"
admin.site.site_title = "Notes App Admin"
admin.site.index_title = "Welcome to Notes App Admin Portal"