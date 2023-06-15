from django.contrib import admin

# Register your models here.
from .models import NacebelCode, NacebelCodeAdvice, NacebelCodeCoverAdvice

admin.site.register(NacebelCode)
admin.site.register(NacebelCodeAdvice)
admin.site.register(NacebelCodeCoverAdvice)
