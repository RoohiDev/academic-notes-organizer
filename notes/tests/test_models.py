from django.test import TestCase
from django.contrib.auth.models import User
from notes.models import Course, Note

class CourseModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_course_creation(self):
        course = Course.objects.create(
            user=self.user,
            title='Advanced Programming',
            description='Basic Mathematics'
        )
        self.assertEqual(course.title, 'Advanced Programming')
        self.assertEqual(str(course), 'Advanced Programming')
        self.assertEqual(course.user.username, 'testuser')


class NoteModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.course = Course.objects.create(user=self.user, title='Advanced Programming')

    def test_note_creation(self):
        note = Note.objects.create(
            course=self.course,
            title='OOP',
            content='This is the content of the note.'
        )
        self.assertEqual(note.title, 'OOP')
        self.assertEqual(str(note), 'OOP')
        self.assertEqual(note.course.title, 'Advanced Programming')

    def test_note_content(self):
        note = Note.objects.create(
            course=self.course,
            title='Django',
            content='This is about Django.'
        )
        self.assertTrue('Django' in note.content)