from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course
from .forms import CourseForm

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
