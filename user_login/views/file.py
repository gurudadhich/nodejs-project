from rest_framework import generics, permissions
from user_login.serializers import FileSerializer
from rest_framework import permissions

class FileUploadView(generics.CreateAPIView):
    serializer_class = FileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
