from django.contrib import admin
from django.urls import path, include
from todo.views import index 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('todo.urls')),
    path('api/', include('todo.urls')),  # your API
    path('login/', include('todo.urls')),  # login and logout
    path('', index, name='index'),
]
