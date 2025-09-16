from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, permissions, status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterUserSerializer, UserSerializer
from .models import User


class RegisterUserView(APIView):
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(id=self.request.user.id)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh = request.data.get("refresh")
            if not refresh:
                return Response(
                    data={"detail": "'refresh' is required.", "code": "required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            RefreshToken(refresh).blacklist()
            return Response(
                data={
                    "success": True,
                    "message": "Successfully logged out.",
                    "code": "success",
                },
                status=status.HTTP_205_RESET_CONTENT,
            )
        except Exception as e:
            return Response(
                data={"success": False, "error": str(e), "code": "bad_request"},
                status=status.HTTP_400_BAD_REQUEST,
            )
