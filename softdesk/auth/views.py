from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from auth import serializers


class SignupView(generics.CreateAPIView):
    """
    View création d'utilisateur
    """
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = serializers.RegisterSerializer


class MyObtainTokenPairView(TokenObtainPairView):
    """
    View récupération de token
    """
    permission_classes = [AllowAny]
    serializer_class = serializers.MyTokenObtainPairSerializer


class ChangePasswordView(generics.UpdateAPIView):
    """
    View changement de mdp
    """
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ChangePasswordSerializer

    def get_object(self):
        return User.objects.get(pk=self.request.user.id)


class LogoutView(APIView):
    """
    View deconnexion
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Post du token utilisateur
        Si celui-ci est valide, il est ajouté à la blacklis
        Ce token ne pourra plus être utilisé
        """
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response("Déconnecté")
        except Exception:
            raise ValidationError("Erreur de déconnexion")


class UsersListView(generics.ListAPIView):
    """
    View liste d'utilisateurs
    """
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.UsersListSerializer
