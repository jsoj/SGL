from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import permissions, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import GroupSerializer, UserSerializer

User = get_user_model()  # Obtém o modelo de usuário atual

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite visualizar ou editar usuários.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite visualizar ou editar grupos.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    return Response({"message": "Bem-vindo, você está autenticado!"})

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Bem-vindo, você está autenticado!"})