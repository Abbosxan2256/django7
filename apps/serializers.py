from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.models import Vacancies, User


#
# from apps.models import Product, Category, Course, CategoryCourse
#
#
# class ProductSerializer(ModelSerializer):
#     class Meta:
#         model = Product
#         fields = 'name', 'price', 'image'
#
#
# class CategorySerializer(ModelSerializer):
#     class Meta:
#         model = Category
#         fields = 'name', 'slug'
#
#
# class CategoryCourseSerializer(ModelSerializer):
#     class Meta:
#         model = CategoryCourse
#         fields = 'name'
#
#
# class CourseSerializer(ModelSerializer):
#     class Meta:
#         model = Course
#         fields = 'name', 'video', 'price'


class VacanciesSerializer(ModelSerializer):
    class Meta:
        model = Vacancies
        fields = 'title', 'price', 'qualification', 'address', 'description', 'created_at', 'employer'


class UserSerializer(ModelSerializer):
    class Meta:
        model = Vacancies
        fields = '__all__'


class EmailSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = 'email',


class SuccessCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        email = data.get('email')
        code = data.get('code')

        if not email:
            raise serializers.ValidationError("Email is required")

        if not code:
            raise serializers.ValidationError("Verification code is required")

        return data