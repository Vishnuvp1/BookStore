from django.contrib.auth import get_user_model
from rest_framework import serializers

from bookstoreapp.models import Author, Book

User = get_user_model()


class AuthorRelatedField(serializers.RelatedField):
    """
    Custom field to handle the representation and validation of the Author model.
    """

    def to_representation(self, value):
        # Convert the Author instance to a dictionary representation
        return {"id": value.id, "name": value.name}

    def to_internal_value(self, data):
        # Convert the input data into an Author instance
        if isinstance(data, dict):
            if "id" in data:
                try:
                    # Try to get the Author by ID
                    return Author.objects.get(id=data["id"])
                except Author.DoesNotExist:
                    raise serializers.ValidationError(
                        "Author with this ID does not exist."
                    )
            else:
                # Create a new Author if only the name is provided
                return Author.objects.create(name=data["name"])
        raise serializers.ValidationError(
            "Invalid data. Expected a dictionary with 'id' or 'name'."
        )


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model, including a custom field for the author.
    """

    author = AuthorRelatedField(queryset=Author.objects.all())

    class Meta:
        model = Book
        fields = ["id", "title", "author", "published_date"]

    def create(self, validated_data):
        # Pop the author from validated data and create a new Book instance
        author = validated_data.pop("author")
        book = Book.objects.create(author=author, **validated_data)
        return book

    def update(self, instance, validated_data):
        # Update the Book instance with new data
        author = validated_data.pop("author")
        instance.author = author
        instance.title = validated_data.get("title", instance.title)
        instance.published_date = validated_data.get(
            "published_date", instance.published_date
        )
        instance.user = validated_data.get("user", instance.user)
        instance.save()
        return instance
