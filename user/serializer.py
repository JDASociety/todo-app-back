from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name']  # Ajusta los campos según tu modelo


class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    name = serializers.CharField(required=True)
    password = serializers.CharField(
        write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'password')
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ('id', 'created_at')

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password'],
        )

        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, data):
        try:
            user = User.objects.get(email=data['email'])

            if not user.check_password(data['password']):
                raise serializers.ValidationError(
                    "Las credenciales proporcionadas son incorrectas.")

        except User.DoesNotExist:
            raise serializers.ValidationError(
                "Las credenciales proporcionadas son incorrectas.")

        return user
