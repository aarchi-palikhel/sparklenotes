from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    # Notes URLs
    path('notes/', views.note_list, name='note_list'),
    path('notes/create/', views.note_create, name='note_create'),
    path('notes/<int:pk>/edit/', views.note_edit, name='note_edit'),
    path('notes/<int:pk>/delete/', views.note_delete, name='note_delete'),
    path('notes/<int:pk>/summarize/', views.summarize_note, name='summarize_note'),
    path('clear-summary/', views.clear_summary, name='clear_summary'),
    
    # Todo URLs
    path('todos/', views.todo_list, name='todo_list'),
    path('todos/create/', views.todo_create, name='todo_create'),
    path('todos/<int:pk>/toggle/', views.todo_toggle, name='todo_toggle'),
    path('todos/<int:pk>/delete/', views.todo_delete, name='todo_delete'),
    path('todos/suggest/', views.suggest_todo, name='suggest_todo'),
]