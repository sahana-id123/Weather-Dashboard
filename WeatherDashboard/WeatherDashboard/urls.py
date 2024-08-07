from django.contrib import admin
from django.urls import path
from dashboard.views import home, history

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('history/', history, name='history'),
]
