from django.urls import path
from user_login.views import user_signup_login, file

urlpatterns = [
    path("api/v1/user/signup", user_signup_login.UserSignup.as_view()),
    path("api/v1/user/login", user_signup_login.UserLogin.as_view()),
    path("api/v1/user/profile", user_signup_login.UserProfile.as_view()),

    path("api/v1/user/file/upload", file.FileUploadView.as_view()),
    path("api/v1/user/file/get", file.FileListView.as_view()),
    path("api/v1/user/file/remove/<int:id>/", file.FileRemoveView.as_view()),
    path('api/v1/user/file/download/<str:unique_code>/', file.FileDownloadView.as_view(), name='file-download'),
]
