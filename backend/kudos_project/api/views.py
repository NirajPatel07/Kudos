from django.shortcuts import render
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.serializers import ValidationError
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from organizations.models import Organization
from users.models import User
from kudos.models import Kudo
from .serializers import (
    OrganizationSerializer, UserSerializer, UserBasicSerializer, 
    KudoSerializer, LoginSerializer
)

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return Response({
                'user': UserSerializer(user).data,
                'message': 'Login successful'
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    logout(request)
    return Response({'message': 'Logout successful'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    return Response(UserSerializer(request.user).data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def organization_users(request):
    users = User.objects.filter(organization=request.user.organization).exclude(id=request.user.id)
    return Response(UserBasicSerializer(users, many=True).data)

@method_decorator(csrf_exempt, name='dispatch')
class KudoListCreateView(generics.ListCreateAPIView):
    serializer_class = KudoSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Return kudos given to or by the current user within their organization
        return Kudo.objects.filter(
            Q(giver=self.request.user) | Q(receiver=self.request.user)
        ).select_related('giver', 'receiver')
    
    def perform_create(self, serializer):
        user = self.request.user
        receiver_id = serializer.validated_data['receiver_id']
        
        # Check if user has kudos available
        if user.kudos_available <= 0:
            raise ValidationError("You have no kudos available to give")
        
        # Check if receiver is in the same organization
        try:
            receiver = User.objects.get(id=receiver_id, organization=user.organization)
        except User.DoesNotExist:
            raise ValidationError("Receiver not found in your organization")
        
        # Check if user is not giving kudo to themselves
        if receiver == user:
            raise ValidationError("You cannot give a kudo to yourself")
        
        # Save the kudo and decrease available kudos
        serializer.save(giver=user, receiver=receiver)
        user.kudos_available -= 1
        user.save()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def received_kudos(request):
    kudos = Kudo.objects.filter(receiver=request.user).select_related('giver')
    return Response(KudoSerializer(kudos, many=True).data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def given_kudos(request):
    kudos = Kudo.objects.filter(giver=request.user).select_related('receiver')
    return Response(KudoSerializer(kudos, many=True).data)
