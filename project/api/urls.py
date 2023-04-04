from django.urls import path, include
from .views import HackathonViewset, HackathonSubmissionViewset, RegistrationAPIView, LoginAPIView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'creation', HackathonViewset, basename='Hackathon')
router.register(r'submission', HackathonSubmissionViewset, basename='HackathonSubmission')

urlpatterns = [
    path('hackathon/', include(router.urls)),
    path('register/', RegistrationAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
]