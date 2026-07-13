from usersapp.serializers.register_serializer import RegisterSerializer,User
from rest_framework import generics,permissions

class RegisterAPI(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

