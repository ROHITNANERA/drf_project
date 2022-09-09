from django.contrib import admin
from django.urls import path,include
from myapp.views import PatientViewset,ReviewViewset,get_time,resiter_user, user_logout
from rest_framework.routers import DefaultRouter
# from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
router = DefaultRouter()
router.register('viewset/patient', PatientViewset,basename="patient")

urlpatterns = [
    path('admin/', admin.site.urls),
    path("gettime/",get_time,name="time"),
    path('myapp/',include('myapp.urls')),
    path('',include(router.urls)),
    # path('user/login/',obtain_auth_token,name="login"), #for simple token authentication
    path('user/login/',TokenObtainPairView.as_view(),name="obtain_token"), #to obtain jwt token
    path('user/refresh/',TokenRefreshView.as_view(),name="refresh_token"), # to refresh the jwt token.
    path("user/register/",resiter_user,name="user_register"),
    path('user/logout/',user_logout,name="logout"),
]
