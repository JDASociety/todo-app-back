from django.shortcuts import get_list_or_404
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from datetime import datetime

from .models import Todo
from .serializers import TodoSerializer
from user.authentication import UserJWTAuthentication

# Create your views here.


class TodoPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'


class TodoViewSet(ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    pagination_class = TodoPagination
    permission_classes = [IsAuthenticated]
    authentication_classes = [UserJWTAuthentication]

    def get_queryset(self):
        queryset = super().get_queryset()

        user = self.request.user
        queryset = queryset.filter(user=user)

        done = self.request.query_params.get('done')

        if done is not None:
            queryset = queryset.filter(done=(done.lower() == 'true'))

        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date and end_date:
            start_date = datetime.fromisoformat(start_date)
            end_date = datetime.fromisoformat(end_date)
            queryset = queryset.filter(
                updated_at__date__range=(start_date, end_date))

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['delete'], url_path='delete-multiple')
    def delete_multiple(self, request):
        ids = request.data.get('ids', [])

        if not ids:
            return Response({"error": "No se proporcionaron IDs."}, status=status.HTTP_400_BAD_REQUEST)

        todos = get_list_or_404(Todo, id__in=ids)

        for todo in todos:
            todo.delete()

        return Response({"message": "Tareas eliminadas correctamente."}, status=status.HTTP_204_NO_CONTENT)

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
