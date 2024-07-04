from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from bookstoreapp.models import Author, Book

from .serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    """
    viewset for viewing and editing book instances.
    """

    serializer_class = BookSerializer
    permission_classes = [
        IsAuthenticated
    ]  # Ensures that only authenticated users can access this viewset

    def get_queryset(self):
        """
        This view should return a list of all the books
        for the currently authenticated user.
        """
        user = self.request.user
        return Book.objects.filter(user=user)  # Filter books by the authenticated user

    def perform_create(self, serializer):
        """
        Save the new book instance with the authenticated user as the owner.
        """
        serializer.save(
            user=self.request.user
        )  # Set the user to the currently authenticated user

    @action(detail=False, methods=["get"], url_path="by-author/(?P<author_id>[^/.]+)")
    def list_books_by_author(self, request, author_id=None):
        """
        Custom action to list books by a specific author.
        """
        try:
            author = Author.objects.get(
                id=author_id
            )  # Attempt to retrieve the author by ID
        except Author.DoesNotExist:
            return Response(
                {"error": "Author not found"}, status=404
            )  # Return 404 if the author does not exist

        # Filter books by the specified author and the authenticated user
        serializer = self.get_serializer(
            Book.objects.filter(author=author, user=request.user), many=True
        )
        return Response(serializer.data)  # Return the serialized data of the books
