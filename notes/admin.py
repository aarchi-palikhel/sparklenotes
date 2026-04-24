from django.contrib import admin
from .models import Note, TodoItem

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'updated_at')
    list_filter = ('created_at', 'user')
    search_fields = ('title', 'content')
    readonly_fields = ('created_at', 'updated_at')
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        super().save_model(request, obj, form, change)

@admin.register(TodoItem)
class TodoItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'completed', 'created_at', 'due_date')
    list_filter = ('completed', 'created_at', 'user')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at',)
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        super().save_model(request, obj, form, change)

# Optional: You can also customize the admin site header and title
admin.site.site_header = "Notes App Administration"
admin.site.site_title = "Notes App Admin"
admin.site.index_title = "Welcome to Notes App Admin Portal"