import logging
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import User, Project, Category, Priority, Task
from .serializers import (
    UserSerializer,
    ProjectSerializer,
    CategorySerializer,
    PrioritySerializer,
    TaskSerializer
)
from .permissions import IsAdmin, IsManager, IsEmployee

logger = logging.getLogger(__name__)

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsManager]


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsManager]


class PriorityViewSet(ModelViewSet):
    queryset = Priority.objects.all()
    serializer_class = PrioritySerializer
    permission_classes = [IsManager]


class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['project', 'priority', 'category']
    search_fields = ['title', 'description']
    permission_classes = [IsEmployee]
    queryset = Task.objects.none()
    
    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'manager']:
            return Task.objects.all()
        return Task.objects.filter(assignee=user)

    def perform_create(self, serializer):
        logger.info("Создание новой задачи")
        serializer.save()