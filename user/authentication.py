from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import exceptions
from .models import User


class UserJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        try:
            user_id = validated_token.get('user_id')

            user = User.objects.get(id=user_id)

            return user
        except User.DoesNotExist:
            return None
        except User.SomeException as e:
            raise exceptions.AuthenticationFailed('Usuario no válido')
