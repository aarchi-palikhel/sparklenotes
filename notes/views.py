from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Note, TodoItem
from .forms import NoteForm, TodoForm
from notes_project.gemini_client import gemini_client

def home(request):
    return render(request, 'notes/home.html')

def note_list(request):
    notes = Note.objects.all().order_by('-created_at')
    return render(request, 'notes/note_list.html', {'notes': notes})

def note_create(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Note created successfully! ✨')
            return redirect('note_list')
    else:
        form = NoteForm()
    return render(request, 'notes/note_form.html', {'form': form, 'title': 'Create Note'})

def note_edit(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, 'Note updated successfully! 💫')
            return redirect('note_list')
    else:
        form = NoteForm(instance=note)
    return render(request, 'notes/note_form.html', {'form': form, 'title': 'Edit Note'})

def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == 'POST':
        note.delete()
        messages.success(request, 'Note deleted successfully! 💫')
        return redirect('note_list')
    return render(request, 'notes/note_confirm_delete.html', {'note': note})

def summarize_note(request, pk):
    note = get_object_or_404(Note, pk=pk)
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

def todo_list(request):
    todos = TodoItem.objects.all().order_by('-created_at')
    return render(request, 'notes/todo_list.html', {'todos': todos})

def todo_create(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Todo created successfully! 🌟')
            return redirect('todo_list')
    else:
        form = TodoForm()
    return render(request, 'notes/todo_form.html', {'form': form, 'title': 'Create Todo'})

def todo_toggle(request, pk):
    todo = get_object_or_404(TodoItem, pk=pk)
    todo.completed = not todo.completed
    todo.save()
    
    status = "completed" if todo.completed else "marked incomplete"
    messages.success(request, f'Todo {status}! {"🎉" if todo.completed else "📝"}')
    
    return redirect('todo_list')

def todo_delete(request, pk):
    todo = get_object_or_404(TodoItem, pk=pk)
    if request.method == 'POST':
        todo.delete()
        messages.success(request, 'Todo deleted successfully! 🎉')
        return redirect('todo_list')
    return render(request, 'notes/todo_confirm_delete.html', {'todo': todo})

def suggest_todo(request):
    if request.method == 'POST':
        task_description = request.POST.get('task_description', '')
        suggestions = gemini_client.suggest_todo(task_description)
        return JsonResponse({'suggestions': suggestions})
    return JsonResponse({'error': 'Invalid request'})