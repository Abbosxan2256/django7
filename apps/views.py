import time
from random import randint
import re

from celery.bin.control import status
from django.core.mail import send_mail
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, GenericAPIView
from rest_framework.response import Response

from apps.filters import VacancyFilter
from apps.models import Vacancies, User
from apps.serializers import VacanciesSerializer, UserSerializer, EmailSerializer, SuccessCodeSerializer
from root import settings

import redis


class VacanciesListCreateAPIView(ListCreateAPIView):
    queryset = Vacancies.objects.all()
    serializer_class = VacanciesSerializer
    filterset_class = VacancyFilter

    def get_object(self):
        return self.request.user


class VacanciesRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Vacancies.objects.all()
    serializer_class = UserSerializer


class SendEmailGenericAPIView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = EmailSerializer

    def post(self, request):
        user_email = request.data.get('email')

        code = redis.StrictRedis('localhost', 6379, db=1)

        verification_code = '{:06d}'.format(randint(0, 999999))

        subject = 'Hisob tasdiqlash kodi'
        message = f'tasdiqlash kodi: {verification_code}'
        strs = ''
        digits = re.findall(r'\d+', message)
        strs.join(digits)
        code.set(strs, user_email)
        from_email = settings.EMAIL_HOST_USER

        try:
            send_mail(subject, message, from_email, [user_email])
            return Response({'message': 'Verification code success'})
        except Exception as e:
            return Response({'error': str(e)}, status=status().HTTP_500_INTERNAL_SERVER_ERROR)


class CheckSuccessCode(GenericAPIView):
    serializer_class = SuccessCodeSerializer

    def post(self, request):
        user_email = request.data.get('email')
        provided_code = request.data.get('code')

        if not user_email or not provided_code:
            return Response({'error': 'email va code mavjud emas'}, status=status.HTTP_400_BAD_REQUEST)

        redis_conn = redis.StrictRedis(host='localhost', port=6379, db=1)
        stored_code = redis_conn.get(user_email)
        stored_timestamp = redis_conn.get(f"{user_email}:timestamp")

        if stored_code == provided_code:
            if stored_timestamp:
                current_timestamp = int(time.time())
                stored_timestamp = int(stored_timestamp)
                if current_timestamp - stored_timestamp <= 60:
                    redis_conn.delete(user_email)
                    redis_conn.delete(f"{user_email}:timestamp")
                    return Response({'message': 'Verification successful'}, status=status.HTTP_200_OK)

            return Response({'error': 'Verification code has expired'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Invalid verification code'}, status=status.HTTP_400_BAD_REQUEST)
