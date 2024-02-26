from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Todo
from .serializers import TodoSerializer
from user.authentication import UserJWTAuthentication

# Create your views here.


class TodoViewSet(ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [UserJWTAuthentication]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'], url_path='latest-todo')
    def latest_todo(self, request):
        try:
            latest_todo = self.get_queryset().latest('updated_at')
            serializer = self.get_serializer(latest_todo)

            return Response(serializer.data)
        except Todo.DoesNotExist:
            return Response({"message": "No hay tareas disponibles."}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'], url_path='status-todo')
    def get_status_todo(self, request):
        try:
            user_todos = self.get_queryset()

            total_todos = user_todos.count()
            completed_todos = user_todos.filter(done=True).count()
            incomplete_todos = total_todos - completed_todos

            data = {
                'totalTodos': total_todos,
                'completedTodos': completed_todos,
                'incompleteTodos': incomplete_todos,
            }

            return Response(data)
        except Todo.DoesNotExist:
            return Response({"message": "No hay tareas disponibles."}, status=status.HTTP_404_NOT_FOUND)
