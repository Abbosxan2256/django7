from django.contrib import admin

from apps.models import Vacancies, User


@admin.register(Vacancies)
class VacanciesAdmin(admin.ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass
