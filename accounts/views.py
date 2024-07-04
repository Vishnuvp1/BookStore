from django.contrib.auth import authenticate, get_user_model
from rest_framework import generics, permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    """
    API view to register a new user.
    """
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save() 

        return Response(
            {"message": "User created successfully"}, status=status.HTTP_201_CREATED
        ) 


class LoginView(APIView):
    """
    API view to log in a user and return an authentication token.
    """
    permission_classes = (AllowAny,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "Username and password are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )  # Return an error if username or password is missing

        user = authenticate(username=username, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user) 
            return Response({"token": token.key})  
        else:
            return Response({"error": "Invalid credentials"}, status=401)  
