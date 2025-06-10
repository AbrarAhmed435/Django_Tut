from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import UserSerializer, NoteSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Note

# ============================
# View to List and Create Notes
# ============================

class NoteListCreate(generics.ListCreateAPIView):
    # Use NoteSerializer to handle input/output
    serializer_class = NoteSerializer

    # Only authenticated users can access this view
    permission_classes = [IsAuthenticated]

    # This method determines which notes to show when the user sends a GET request
    def get_queryset(self):
        user = self.request.user  # Get the current logged-in user
        return Note.objects.filter(author=user)  # Return only the notes belonging to this user

    # This method is called automatically when a valid POST request is made to create a new note
    def perform_create(self, serializer):
        if serializer.is_valid():  # Check if data is valid (although DRF already does this before calling perform_create)
            serializer.save(author=self.request.user)  # Save the note with the current user as the author
        else:
            print(serializer.errors)  # Print validation errors (not necessary in production)

# ============================
# View to Register New Users
# ============================

class CreateUserView(generics.CreateAPIView):
    # This view allows new users to be created
    queryset = User.objects.all()  # Define the model objects this view works on
    serializer_class = UserSerializer  # Use custom serializer for user creation
    permission_classes = [AllowAny]  # Allow both authenticated and unauthenticated users to access this view (public endpoint)

class NoteDelete(generics.DestroyAPIView):
    serializer_class=NoteSerializer
    permission_classes=[IsAuthenticated]
    
    def get_queryset(self):
        user=self.request.user
        return Note.objects.filter(author=user)
    