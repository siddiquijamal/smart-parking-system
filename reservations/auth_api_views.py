from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .auth_serializers import RegisterSerializer

# ✅ REGISTER
@api_view(['POST'])
@permission_classes([AllowAny])
def register_api(request):
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        token = Token.objects.create(user=user)
        return Response({
            "message": "User registered successfully",
            "token": token.key
        })

    return Response(serializer.errors, status=400)


# ✅ LOGIN
@api_view(['POST'])
@permission_classes([AllowAny])
def login_api(request):
    user = authenticate(
        username=request.data.get('username'),
        password=request.data.get('password')
    )

    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            "message": "Login successful",
            "token": token.key
        })

    return Response({"error": "Invalid credentials"}, status=401)


# ✅ LOGOUT
@api_view(['POST'])
def logout_api(request):
    request.user.auth_token.delete()
    return Response({"message": "Logged out successfully"})
