from django import forms
from .models import Course, Note

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description']

class CustomClearableFileInput(forms.ClearableFileInput):
    clear_checkbox_label = 'Tick to remove the current file and save'

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content', 'attachment']
        widgets = {
            'attachment': CustomClearableFileInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get('content')
        attachment = cleaned_data.get('attachment')

        if not content and not attachment:
            raise forms.ValidationError('Content or a file attachment is required.')
        
        return cleaned_data