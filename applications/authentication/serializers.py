from django.contrib.auth.password_validation import validate_password
from django.db import IntegrityError
from rest_framework import serializers
from .models import User, Notification

class UserSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'phone', 'nationality', 'passport_number', 'address', 'city', 'country', 'user_type', 'is_active', 'is_staff', 'is_superuser', 'last_login', 'date_joined', 'created_at', 'updated_at')

        read_only_fields = fields


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    password_confirm = serializers.CharField(style={'input_type': 'password'}, write_only=True) # Campo temporal para confirmar contraseña

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm', 'first_name', 'last_name', 'phone', 'nationality', 'passport_number', 'address', 'city', 'country')

    def validate(self, data):
        if data['password'] != data.get('password_confirm'):
            raise serializers.ValidationError({"password_confirm": "Las contraseñas ingresadas no son iguales"}) # Comparación de contraseñas
        
        data.pop('password_confirm')
        validate_password(data['password'], user=User(**data)) # Validación de contraseña en base a reglas
        return data

    def create(self, validated_data):
        validated_data['user_type'] = 'customer'  # Rol por defecto (cliente)
        try:
            user = User.objects.create_user(**validated_data)
            return user
        except IntegrityError:
            raise serializers.ValidationError({"detail": "Usuario o email ya registrado"})
        

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

        fields = (
            'first_name', 
            'last_name', 
            'phone', 
            'address', 
            'city', 
            'country', 
            'passport_number'
        )
        
        read_only_fields = ('username', 'email', 'user_type', 'is_active', 'nationality')


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password     = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({'confirm_password': 'Las contraseñas no coinciden.'})
        validate_password(data['new_password'])
        return data


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    token        = serializers.CharField()
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({'confirm_password': 'Las contraseñas no coinciden.'})
        validate_password(data['new_password'])
        return data


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'type', 'title', 'message', 'is_read', 'link', 'created_at']
        read_only_fields = ['id', 'type', 'title', 'message', 'link', 'created_at']