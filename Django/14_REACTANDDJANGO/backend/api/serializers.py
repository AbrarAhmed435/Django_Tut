# Import the built-in User model from Django
from django.contrib.auth.models import User

# Import Django REST Framework's serializer classes
from rest_framework import serializers
from .models import Note
# Define a serializer for the User model
class UserSerializer(serializers.ModelSerializer):

    # Meta class provides metadata about the serializer
    class Meta:
        model = User  # The model this serializer works with
        fields = ['id', 'username', 'password']  # Fields to include in the API

        # extra_kwargs is used to set extra options for fields
        # We set 'password' as write_only so it won't appear in responses
        extra_kwargs = {
            'password': {'write_only': True}
        }

    # Override the create() method to handle password hashing
    def create(self, validated_data):
        # Use Django's built-in create_user() which hashes the password
        user = User.objects.create_user(**validated_data)
        return user  # Return the newly created user object
    
class NoteSerializer(serializers.ModelSerializer):
        class Meta:
            model = Note
            fields = ['id','title','content','created_at','author']
            extra_kwargs={"author":{'read_only':True}}