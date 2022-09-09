from rest_framework.serializers import ModelSerializer, SerializerMethodField, Field
from .models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','first_name','last_name','email','password','telephone','cp','curp','rfc','date','is_superuser','is_staff', 'address']
    
    def create(self, validated_data):
        raw_password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if raw_password is not None:
            instance.set_password(raw_password)
        instance.save()
        return instance
            
class isStaffUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'address'
        ]