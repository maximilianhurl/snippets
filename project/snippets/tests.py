from django.test import TestCase
from project.snippets.models import Snippet


class TestSnippetsModel(TestCase):

    def test_create(self):
        snippet = Snippet()
        snippet.text = "#Hello"
        snippet.save()

        snippet = Snippet.objects.first()
        self.assertTrue(snippet.id)
        self.assertTrue(snippet.created)
        self.assertTrue(snippet.modified)
        self.assertEqual(snippet.text.rendered, "<h1>Hello</h1>")
        self.assertEqual(snippet.text.raw, "#Hello")
