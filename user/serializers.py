from rest_framework import serializers
from django.contrib.auth.models import User
from user.models import *
from django.contrib.auth import get_user_model

User = get_user_model()


# Register Serializer
class RegistrationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = (
            "name",
            "Email_Address",
            "zipcode",
            "Date_of_Birth",
            "password",
            
        )
            

        
        extra_kwargs = {"password": {"write_only": True}}
        
    
    def create(self,validated_data):
        account = User.objects.create(
            Email_Address= validated_data["Email_Address"],
            Date_of_Birth = validated_data["Date_of_Birth"],
            name = validated_data["name"],
            zipcode = validated_data["zipcode"],
            
        )
        password = validated_data["password"]
        print(account)
        account.set_password(password)
        account.save()
        return account

# Users Info Serializers
class UsersInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'
  

# Weather Data Serializer
class WeatherClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherClass
        fields = '__all__'