from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from user_app.serializers import RegistrationSerializer, UserProfileSerializer


@api_view(["POST"])
def registration_view(request):
    if request.method == "POST":
        serializer = RegistrationSerializer(data=request.data)

        data = {}

        if serializer.is_valid():
            account = serializer.save()

            data["response"] = "Registro Exitoso"
            data["username"] = account.username
            data["email"] = account.email

            refresh_token = RefreshToken.for_user(account)
            data["token"] = {
                "refresh": str(refresh_token),
                "access": str(refresh_token.access_token)
            }
        else:
            data = serializer.errors

        return Response(data)


class UserProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)