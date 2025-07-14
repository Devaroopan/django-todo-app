from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, index, login_view, logout_view, signup_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('', index, name='index'),  # Home page (TODO list)
    path('complete/<int:task_id>/', views.toggle_complete, name='task-complete-toggle'),
    path('delete/<int:task_id>/', views.delete_task, name='task-delete'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
      path('signup/',signup_view, name='signup'),
    path('api/', include(router.urls)),

    # JWT Token endpoints (still useful)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
