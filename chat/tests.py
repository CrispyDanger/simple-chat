from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Thread, Message


class ThreadTestCase(TestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            username="user1", password="testpass"
        )
        self.user2 = get_user_model().objects.create_user(
            username="user2", password="testpass"
        )

    def test_add_participant(self):
        """
        Test that a participant can be added to a thread
        """
        thread = Thread.objects.create()
        thread.add_participant(self.user1)
        self.assertEqual(thread.participants.count(), 1)

    def test_add_too_many_participants(self):
        """
        Test that an exception is raised when attempting to add more than 2 participants
        to a thread
        """
        thread = Thread.objects.create()
        thread.add_participant(self.user1)
        thread.add_participant(self.user2)
        with self.assertRaises(Exception):
            thread.add_participant(
                get_user_model().objects.create_user(
                    username="user3", password="testpass"
                )
            )

    def test_thread_str_method(self):
        """
        Test that the string representation of a thread is formatted correctly
        """
        thread = Thread.objects.create()
        thread.add_participant(self.user1)
        thread.add_participant(self.user2)
        self.assertEqual(str(thread), "user1 and user2 Chat")


class MessageTestCase(TestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            username="user1", password="testpass"
        )
        self.user2 = get_user_model().objects.create_user(
            username="user2", password="testpass"
        )
        self.thread = Thread.objects.create()
        self.thread.add_participant(self.user1)
        self.thread.add_participant(self.user2)

    def test_message_str_method(self):
        """
        Test that the string representation of a message is formatted correctly
        """
        message = Message.objects.create(
            sender=self.user1, text="Test message", thread=self.thread
        )
        self.assertEqual(
            str(message), f'{self.user1} message in "user1 and user2 Chat"'
        )
