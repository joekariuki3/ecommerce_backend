import logging

from rest_framework import mixins, permissions, status, viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import UserSerializer

logger = logging.getLogger(__name__)


class RegisterUserView(CreateAPIView):
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        logger.info(f"New user registered: {user.email}")


class UserViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        logger.info(f"User {self.request.user.email} fetching their profile.")
        return self.queryset.filter(id=self.request.user.id)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if refresh_token is None:
            logger.warning("Logout attempt without refresh token.")
            return Response(
                data={"detail": '"refresh" is required.', "code": "required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            logger.info(f"User {request.user.email} logged out successfully.")
            return Response(
                data={
                    "success": True,
                    "message": "Successfully logged out.",
                    "code": "success",
                },
                status=status.HTTP_205_RESET_CONTENT,
            )
        except Exception as e:
            logger.error(f"Error during logout for user {request.user.email}: {e}")
            return Response(
                data={
                    "success": False,
                    "error": "Invalid token.",
                    "code": "bad_request",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
