from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .authentication import UserJWTAuthentication

from .models import User
from .serializer import UserRegisterSerializer, UserLoginSerializer, UserSerializer

# Create your views here.


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'], url_path='register')
    def register(self, request):
        serializer = UserRegisterSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()
        token = RefreshToken.for_user(user)

        response = {
            'user': serializer.data,
            'token': str(token.access_token),
        }

        return Response(response, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_data = serializer.validated_data

        user_data.last_login = timezone.now()
        user_data.save(update_fields=['last_login'])

        token = RefreshToken.for_user(user_data)
        user = UserSerializer(user_data).data

        return Response({
            'user': user,
            'token': str(token.access_token)
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['delete'], url_path='delete_account', permission_classes=[IsAuthenticated], authentication_classes=[UserJWTAuthentication])
    def delete_account(self, request):
        try:
            request.user.delete()

            return Response({"message": "Cuenta eliminada correctamente."}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({"error": "Usuario no encontrado."}, status=status.HTTP_404_NOT_FOUND)
