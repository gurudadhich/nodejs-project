from django.contrib.auth.models import User
from rest_framework import serializers

from user_login.models import File

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password',
                  'email', 'first_name', 'last_name',)
        read_only_fields = ('id',)
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'write_only': True}
        }


class UserSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = User
        fields = ('id', 'user',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        print(validated_data)
        user_data = validated_data.get('user')
        user = User.objects.create(
            username=user_data.get('username'),
        )
        user.set_password(user_data.get('password'))
        user.save()
        return user

class FileSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = ('id', 'user', 'file', 'unique_code',)
        read_only_fields = ('id',)
        
    def get_file(self, obj):
        return self.context['request'].build_absolute_uri(obj.file.url)
            
class UserWithFilesSerializer(serializers.ModelSerializer):
    files = FileSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name', 'files',)
        read_only_fields = ('id',)
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'write_only': True}
        }