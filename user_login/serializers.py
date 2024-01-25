from django.contrib.auth.models import User
from rest_framework import serializers

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

