from rest_framework import generics, permissions
from user_login.models import File
from user_login.serializers import FileSerializer
from django.http import FileResponse
import mimetypes
from rest_framework.response import Response
from rest_framework import authentication, permissions, status
from rest_framework.views import APIView
from rest_framework.parsers import FormParser, MultiPartParser

class FileUploadView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = FileSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                
                status=status.HTTP_201_CREATED
            )
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
 

class FileListView(generics.ListAPIView):
    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]
    serializer_class = FileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return File.objects.filter(user=self.request.user)

class FileRemoveView(APIView):
    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]
    serializer_class = FileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, id):
        print("remove file")
        print(id)
        print("****")
        try:
            file = File.objects.get(id=id,user=request.user)
            file.delete()
            return Response({"success": True})

        except File.DoesNotExist:
            return Response(
                data={"error": "File not found"},
                status=status.HTTP_404_NOT_FOUND
            )

class FileDownloadView(APIView):
    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, unique_code):
        if request.user.is_authenticated:
            
            try:
                uploaded_file = File.objects.get(user=request.user, unique_code=unique_code)
            except File.DoesNotExist:
                return Response("File not found.", status=404)
            
            path = uploaded_file.file.path 
            mimetype, encoding = mimetypes.guess_type(path, strict=True)
            if not mimetype:
                mimetype = "application/octet-stream"

            try:
                media = open(path, "rb")
                return FileResponse(media, content_type=mimetype)
            except IOError:
                return Response("File not found.", status=404)

        return Response("Access to this file is not permitted.", status=403)