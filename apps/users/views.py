from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, permissions
from .serializers import RegisterUserSerializer, UserSerializer
from .models import User

class RegisterUserView(APIView):
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return [self.request.user]