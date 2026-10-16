from django.shortcuts import render

# Create your views here.


from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

from .serializers import UserProfileSerializer
from .account_serializers import OfficialAccountSerializer
from .permissions import IsSuperAdmin

User = get_user_model()

class CurrentUserProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    
class OfficialAccountCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = OfficialAccountSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]