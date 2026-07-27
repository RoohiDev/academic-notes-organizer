from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from notes.models import Course, Note
from django.core.files.uploadedfile import SimpleUploadedFile
import os

class ViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.course = Course.objects.create(user=self.user, title='Advanced Programming',description='Python, OOP, Django')
        self.note = Note.objects.create(course=self.course, title='Django', content='This is about Django.')

    # Auth test
    def test_course_list_requires_login(self):
        response = self.client.get(reverse('notes:course_list'))
        self.assertRedirects(response, f'{reverse("login")}?next={reverse("notes:course_list")}')

    def test_note_list_requires_login(self):
        response = self.client.get(reverse('notes:note_list', args=[self.course.id]))
        self.assertRedirects(response, f'{reverse("login")}?next={reverse("notes:note_list", args=[self.course.id])}')
    
    # User access to thier data test
    def test_user_can_only_see_own_courses(self):
        self.client.login(username='testuser', password='12345')

        other_user = User.objects.create_user(username='hacker', password='12345')
        Course.objects.create(user=other_user, title='Secret Course')
        
        response = self.client.get(reverse('notes:course_list'))
        self.assertContains(response, 'Advanced Programming')
        self.assertNotContains(response, 'Secret Course')

    def test_user_cannot_edit_others_course(self):
        other_user = User.objects.create_user(username='hacker', password='12345')
        other_course = Course.objects.create(user=other_user, title='Secret Course')
        
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('notes:course_edit', args=[other_course.id]))
        self.assertEqual(response.status_code, 404)

    # CRUD course test
    def test_course_create(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('notes:course_create'), {
            'title': 'Fundamentals of Programming',
            'description': 'Algorithm, Flowchart, CPP'
            })
        self.assertRedirects(response, reverse('notes:course_list'))
        self.assertTrue(Course.objects.filter(title='Fundamentals of Programming').exists())

    def test_course_update(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('notes:course_edit', args=[self.course.id]), {
            'title': 'Advanced Programming (Updated)',
            'description': 'New description'
            })
        self.assertRedirects(response, reverse('notes:course_list'))
        self.course.refresh_from_db()
        self.assertEqual(self.course.title, 'Advanced Programming (Updated)')

    def test_course_delete(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('notes:course_delete', args=[self.course.id]))
        self.assertRedirects(response, reverse('notes:course_list'))
        self.assertFalse(Course.objects.filter(id=self.course.id).exists())

    # CRUD note test
    def test_note_create(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('notes:note_create', args=[self.course.id]), {
            'title': 'OOP',
            'content': 'This is about OOP.'
            })
        self.assertRedirects(response, reverse('notes:course_list'))
        self.assertTrue(Note.objects.filter(title='OOP').exists())

    def test_note_update(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('notes:note_edit', args=[self.course.id, self.note.id]), {
            'title': 'Django (Updated)',
            'content': 'New content about Django.'
            })
        self.assertRedirects(response, reverse('notes:course_list'))
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, 'Django (Updated)')

    def test_note_delete(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('notes:note_delete', args=[self.course.id, self.note.id]))
        self.assertRedirects(response, reverse('notes:course_list'))
        self.assertFalse(Note.objects.filter(id=self.note.id).exists())

    # Search test
    def test_search_returns_results(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('notes:search_notes'), {'q': 'django'})
        self.assertContains(response, 'Django')
        self.assertNotContains(response, 'No result for')

    def test_search_no_results(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('notes:search_notes'), {'q': 'nonexistent'})
        self.assertContains(response, 'No result for')

# Upload file Tests
class FileUploadTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.course = Course.objects.create(user=self.user, title='Advanced Programming', description='Python, OOP, Django')

    def test_note_create_with_file(self):
        self.client.login(username='testuser', password='12345')
        
        file_content = b'This is a test file content.'
        file = SimpleUploadedFile('test.txt', file_content, content_type='text/plain')
        
        response = self.client.post(reverse('notes:note_create', args=[self.course.id]), {
            'title': 'Note with File',
            'content': '',
            'attachment': file
        })
        
        self.assertRedirects(response, reverse('notes:course_list'))
        note = Note.objects.get(title='Note with File')
        self.assertTrue(note.attachment)
        self.assertTrue(note.attachment.name.startswith('notes/'))
        
        note.attachment.delete()

    def test_note_update_with_new_file(self):
        self.client.login(username='testuser', password='12345')
        
        old_file = SimpleUploadedFile('old.txt', b'old content', content_type='text/plain')
        note = Note.objects.create(course=self.course, title='Note with Old File', content='', attachment=old_file)
        
        new_file = SimpleUploadedFile('new.txt', b'new content', content_type='text/plain')
        response = self.client.post(reverse('notes:note_edit', args=[self.course.id, note.id]), {
            'title': 'Note with New File',
            'content': '',
            'attachment': new_file
        })
        
        note.refresh_from_db()
        self.assertRedirects(response, reverse('notes:course_list'))
        self.assertTrue('new.txt' in note.attachment.name)
        
        note.attachment.delete()

    def test_clear_attachment_via_checkbox(self):
        self.client.login(username='testuser', password='12345')

        file = SimpleUploadedFile('to_clear.txt', b'content', content_type='text/plain')
        note = Note.objects.create(course=self.course, title='Note to Clear', content='', attachment=file)

        response = self.client.post(reverse('notes:note_edit', args=[self.course.id, note.id]), {
            'title': 'Note to Clear',
            'content': 'Some content to keep the form valid.',
            'attachment': '',
            'attachment-clear': 'on'
        })
        note.refresh_from_db()
        self.assertRedirects(response, reverse('notes:course_list'))
        self.assertFalse(note.attachment)