from django.test import TestCase
from notes.forms import CourseForm, NoteForm
from django.core.files.uploadedfile import SimpleUploadedFile

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
        self.assertIn('__all__', form.errors)


class NoteFormFileTest(TestCase):
    def test_valid_form_with_file_only(self):
        file = SimpleUploadedFile('test.txt', b'This is a test file content.', content_type='text/plain')
        data = {'title': 'Text File Note', 'content': ''}
        files = {'attachment': file}
        form = NoteForm(data=data, files=files)
        self.assertTrue(form.is_valid())

    def test_valid_form_with_content_and_file(self):
        file = SimpleUploadedFile('test.txt', b'This is a test file content.', content_type='text/plain')
        data = {'title': 'Mixed Note', 'content': 'This is content.'}
        files = {'attachment': file}
        form = NoteForm(data=data, files=files)
        self.assertTrue(form.is_valid())

    def test_invalid_form_empty_content_and_no_file(self):
        data = {'title': 'Empty Note', 'content': ''}
        files = {}
        form = NoteForm(data=data, files=files)
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)