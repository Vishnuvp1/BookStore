from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from bookstoreapp.models import Author, Book

User = get_user_model()


class BookTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.author1 = Author.objects.create(name="Author 1")
        self.author2 = Author.objects.create(name="Author 2")

        self.book1_data = {"title": "Book 1", "published_date": "2023-01-01"}
        self.book2_data = {"title": "Book 2", "published_date": "2023-01-02"}

        self.book1 = Book.objects.create(
            user=self.user, author=self.author1, **self.book1_data
        )
        self.book2 = Book.objects.create(
            user=self.user, author=self.author2, **self.book2_data
        )

    def tearDown(self):
        self.client.logout()

    def test_create_book(self):
        new_book_data = {
            "title": "sample book",
            "author": {"id": self.author1.id},
            "published_date": "2024-01-01",
        }
        response = self.client.post("/api/books/", new_book_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    def test_retrieve_book(self):
        response = self.client.get(f"/api/books/{self.book1.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.book1_data["title"])

    def test_update_book(self):
        updated_data = {
            "title": "Updated Title",
            "author": {"id": self.author1.id},
            "published_date": "2022-12-31",
        }
        response = self.client.put(
            f"/api/books/{self.book1.id}/", updated_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, updated_data["title"])
        self.assertEqual(str(self.book1.published_date), updated_data["published_date"])

    def test_delete_book(self):
        response = self.client.delete(f"/api/books/{self.book1.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    def test_list_books_by_author(self):
        response = self.client.get(f"/api/books/by-author/{self.author1.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], self.book1_data["title"])

    def test_list_books_by_nonexistent_author(self):
        response = self.client.get("/api/books/by-author/999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_books_by_author_unauthenticated(self):
        self.client.logout()
        response = self.client.get(f"/api/books/by-author/{self.author1.id}/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_books_by_another_user(self):
        user_anonymous = User.objects.create_user(
            username="anotheruser", password="password456", email="anonymous@gmail.com"
        )
        self.client.force_authenticate(user=user_anonymous)
        response = self.client.get(f"/api/books/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_list_books_by_author_of_another_user(self):
        user_anonymous = User.objects.create_user(
            username="anotheruser", password="password456", email="anonymous@gmail.com"
        )
        self.client.force_authenticate(user=user_anonymous)
        response = self.client.get(f"/api/books/by-author/{self.author1.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
