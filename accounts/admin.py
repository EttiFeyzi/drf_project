from django.contrib import admin
from accounts.models import User,PhoneOTP

admin.site.register(User)

admin.site.register(PhoneOTP)