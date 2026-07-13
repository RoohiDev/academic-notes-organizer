from django.test import TestCase
from notes.forms import CourseForm, NoteForm

class CourseFormTest(TestCase):
    def test_valid_form(self):
        data = {'title': 'Advanced Programming', 'description': 'Python, OOP and Django'}
        form = CourseForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_empty_title(self):
        data = {'title': '', 'description': 'No title'}
        form = CourseForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_invalid_form_missing_title(self):
        data = {'description': 'Missing title'}
        form = CourseForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)


class NoteFormTest(TestCase):
    def test_valid_form(self):
        data = {'title': 'OOP', 'content': 'This is the content.'}
        form = NoteForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_empty_title(self):
        data = {'title': '', 'content': 'Some content'}
        form = NoteForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_invalid_form_empty_content(self):
        data = {'title': 'Django', 'content': ''}
        form = NoteForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors)