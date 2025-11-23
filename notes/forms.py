from django import forms
from .models import Note, TodoItem

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded-md'}),
            'content': forms.Textarea(attrs={'class': 'w-full p-2 border border-gray-300 rounded-md', 'rows': 4}),
        }

class TodoForm(forms.ModelForm):
    class Meta:
        model = TodoItem
        fields = ['title', 'description', 'due_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded-md'}),
            'description': forms.Textarea(attrs={'class': 'w-full p-2 border border-gray-300 rounded-md', 'rows': 3}),
            'due_date': forms.DateTimeInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded-md', 'type': 'datetime-local'}),
        }