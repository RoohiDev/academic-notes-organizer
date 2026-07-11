from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course, Note
from .forms import CourseForm, NoteForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.db.models import Q


#Course Views
@login_required
def course_list(request):
    courses = Course.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'notes/course_list.html', {'courses': courses})

@login_required
def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.user = request.user
            course.save()
            messages.success(request, 'Course created successfully.')
            return redirect('notes:course_list')
    else:
        form = CourseForm()
    return render(request, 'notes/course_form.html', {'form': form, 'title': 'Create new course.'})

@login_required
def course_edit(request, pk):
    course = get_object_or_404(Course, pk=pk, user=request.user)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request,'Course edited successfully.')
            return redirect('notes:course_list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'notes/course_form.html', {'form': form, 'title': 'Edit course.'})
    
@login_required
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk, user=request.user)
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Course deleted successfully.')
        return redirect('notes:course_list')
    return render(request, 'notes/course_confirm_delete.html', {'course': course})


#Note Views
@login_required
def note_list(request, course_id):
    course = get_object_or_404(Course, pk=course_id, user=request.user)
    notes = course.notes.all().order_by('-created_at')
    return render(request, 'notes/note_list.html', {'course': course, 'notes': notes})

@login_required
def note_create(request, course_id):
    course = get_object_or_404(Course, pk=course_id, user=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.course = course
            note.save()
            messages.success(request, 'Note created successfully.')
            return redirect('notes:note_list', course_id=course.id)
    else:
        form = NoteForm()
    return render(request, 'notes/note_form.html', {'form': form, 'course': course, 'title': 'Create new note'})

@login_required
def note_edit(request, course_id, pk):
    course = get_object_or_404(Course, pk=course_id, user=request.user)
    note = get_object_or_404(Note, pk=pk, course=course)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, 'Note edited successfully.')
            return redirect('notes:note_list', course_id=course.id)
    else:
        form = NoteForm(instance=note)
    return render(request, 'notes/note_form.html', {'form': form, 'course': course, 'title': 'Edit note'})

@login_required
def note_delete(request, course_id, pk):
    course = get_object_or_404(Course, pk=course_id, user=request.user)
    note = get_object_or_404(Note, pk=pk, course=course)
    if request.method == 'POST':
        note.delete()
        messages.success(request, 'Note deleted successfully.')
        return redirect('notes:note_list', course_id=course.id)
    return render(request, 'notes/note_confirm_delete.html', {'course': course, 'note': note})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'User {user.username} created successfully.')
            return redirect('notes:course_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

#Search view
@login_required
def search_notes(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        results = Note.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query),
            course__user=request.user
        ).order_by('-created_at')
    return render(request, 'notes/search_results.html', {'query': query, 'results': results})