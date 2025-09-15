from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterUserSerializer

class RegisterUserView(APIView):
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
