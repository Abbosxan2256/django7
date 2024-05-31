from django.urls import path

from apps.views import VacanciesListCreateAPIView, VacanciesRetrieveUpdateDestroyAPIView, SendEmailGenericAPIView, \
    CheckSuccessCode

urlpatterns = [
    path('vacancies', VacanciesListCreateAPIView.as_view()),
    path('vacancies/<int:pk>', VacanciesRetrieveUpdateDestroyAPIView.as_view()),
    path('send_email', SendEmailGenericAPIView.as_view()),
    path('success', CheckSuccessCode.as_view())
]