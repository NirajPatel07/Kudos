from rest_framework import serializers
from organizations.models import Organization
from users.models import User
from kudos.models import Kudo

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name', 'description', 'created_at']

class UserSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'organization', 'kudos_available']

class UserBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']

class KudoSerializer(serializers.ModelSerializer):
    giver = UserBasicSerializer(read_only=True)
    receiver = UserBasicSerializer(read_only=True)
    receiver_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Kudo
        fields = ['id', 'giver', 'receiver', 'receiver_id', 'message', 'created_at']
        read_only_fields = ['giver', 'created_at']
    
    def create(self, validated_data):
        validated_data['giver'] = self.context['request'].user
        return super().create(validated_data)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
