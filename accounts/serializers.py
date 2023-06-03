from rest_framework import  serializers
from accounts.models import APIKey
from django.contrib.auth.models import User

class UserAPIkeySerializer(serializers.ModelSerializer):
    class Meta:
        model = APIKey
        fields = ['key', 'company', 'created_at', 'updated_at']


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    apikey = UserAPIkeySerializer(many=False,required=False)
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name', 'is_superuser','apikey']
        extra_kwargs = {
            'password': {'write_only': True},
        }
    def create(self, validated_data):
        password = validated_data.pop('password')
        password2 = validated_data.pop('password2')
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data):
        validated_data.pop('password', None)  # Exclude password field
        validated_data.pop('password2', None)  # Exclude password2 field           
        instance = super().update(instance, validated_data)
        return instance  # Return the updated instance

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.context.get('view') and self.context['view'].action == 'update': # If the request is an update
            self.fields['password'].required = False
            self.fields['email'].required = False
            self.fields['username'].required = False
            self.fields['password2'].required = False

