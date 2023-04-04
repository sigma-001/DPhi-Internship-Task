from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .serializers import RegistrationSerializer, LoginSerializer, HackathonSerializer, HackathonSubmissionSerializer
from .models import Hackathon, HackathonSubmission
from django.core.exceptions import ObjectDoesNotExist

class RegistrationAPIView(generics.CreateAPIView):

    serializer_class = RegistrationSerializer
    
    
class LoginAPIView(APIView):
    
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        if data['success'] is True:
            status_code = status.HTTP_200_OK
        else:
            status_code = status.HTTP_401_UNAUTHORIZED
        return Response(data, status = status_code)


class HackathonViewset(ModelViewSet):
    
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = HackathonSerializer
    
    def get_queryset(self):
        if self.request.method == 'GET':
            return Hackathon.objects.all()
        else:
            return Hackathon.objects.filter(creator = self.request.user)
            
    def create(self, request, *args, **kwargs):
        request.data.update({'creator': request.user.id})
        return super().create(request, *args, **kwargs)
    
    
    @action(detail=True, methods=['post'], permission_classes = [IsAuthenticated])
    def enroll_in_hackathon(self, request, pk):
        try:
            hackathon = Hackathon.objects.get(id = pk)
            hackathon.enrolled_by.add(request.user)
            return Response({"success": True})
            
        except ObjectDoesNotExist:
            return Response({"success": False,
                             "error": "Provide a valid hackathon id"},
                             status = status.HTTP_400_BAD_REQUEST)
    
    @action(detail = False, methods = ['get'], permission_classes = [IsAuthenticated])
    def enrolled_hackathons(self, request):
        user = self.request.user
        enrolled_hackathons = user.enrolled_hackathons.all()
        return Response({"success": True, 
                         "data": HackathonSerializer(enrolled_hackathons, many = True).data})

   
class HackathonSubmissionViewset(ModelViewSet):
    
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = HackathonSubmissionSerializer
    
    def get_queryset(self):
        if self.request.method == 'GET':
            return HackathonSubmission.objects.all()
        else:
            return HackathonSubmission.objects.filter(submitted_by = self.request.user)
        
        
    def create(self, request, *args, **kwargs):
        request.data.update({'submitted_by': request.user.id})
        return super().create(request, *args, **kwargs)
    
    
    @action(detail=True, methods=['post'], permission_classes = [IsAuthenticated])
    def star_submission(self, request, pk):
        try:
            hackathon_submission = HackathonSubmission.objects.get(id = pk)
            hackathon_submission.starred_by.add(request.user)
            return Response({"success": True})
            
        except ObjectDoesNotExist:
            return Response({"success": False,
                             "error": "Provide a valid hackathon submission id"},
                             status = status.HTTP_400_BAD_REQUEST)
            
    
    @action(detail = False, methods = ['get'], permission_classes = [IsAuthenticated])
    def starred_submissions(self, request):
        user = self.request.user
        favourite_submissions = user.favourite_submissions.all()
        return Response({"success": True, 
                         "data": HackathonSubmissionSerializer(favourite_submissions, many = True).data})
