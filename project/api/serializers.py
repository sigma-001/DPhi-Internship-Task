from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Hackathon, HackathonSubmission

User = get_user_model()

class AuthenticationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['username', 'password'] 
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.pop('password')
        refresh = RefreshToken.for_user(instance)
        data['token'] = str(refresh.access_token)
        return data


class RegistrationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['username', 'password'] 
        
        
    def create(self, validated_data):
        user = User.objects.create_user(username = validated_data['username'],
                                        password = validated_data['password'])
        return user

    def to_representation(self, instance):
        data = {'success' : True}
        data['data'] = AuthenticationSerializer(instance).data
        return data

class LoginSerializer(serializers.Serializer):
    
    username = serializers.CharField(write_only = True)
    password = serializers.CharField(write_only = True)
    success = serializers.BooleanField(read_only = True)
    data = serializers.JSONField(read_only = True)
    
    class Meta:
        fields = ['username', 'password']
        
    def validate(self, data):
        
        data = super().validate(data)
        user = authenticate(username = data['username'], password = data['password'])
        if user is None:
            return {
                'success' : False,
                'data': "Invalid username or password"}
        else:
            return {
                'success' : True,
                'data' : AuthenticationSerializer(user).data
            }
        

class HackathonSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Hackathon
        fields = '__all__'
        
        
class HackathonSubmissionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = HackathonSubmission
        fields = '__all__'
        
    
    def validate(self, data):
        
        if data['hackathon'].creator == data['submitted_by']:
            raise ValidationError("User can't create a submission against self created hackathon")
        
        if HackathonSubmission.objects.filter(hackathon = data['hackathon'], 
                                              submitted_by = data['submitted_by']).exists():
            raise ValidationError("User had already created the submission to this hackathon")
        
        
    #     If the user doesn't submit the files or links as mentioned according to the
    #     submission types mentioned while creating the hackathon an error is thrown.
    
    #     Even if a person try to submit the things apart from mentioned, those values 
    #     will not be considered and updated to null values.
    
        if data['hackathon'].submission_type == 'file':
            try:
                data['file']
                data.update({'image': None, 'url': None})
            except KeyError:
                raise ValidationError('Provide the required file with the submission')
            
        if data['hackathon'].submission_type == 'url':
            try:
                data['url']
                data.update({'image': None, 'file': None})
            except KeyError:
                raise ValidationError('Provide the required url with the submission')
            
        if data['hackathon'].submission_type == 'image':
            try:
                data['image']
                data.update({'file': None, 'url': None})
            except KeyError:
                raise ValidationError('Provide the required image with the submission')
            
        return data
