"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from artists import views
from rest_framework.routers import DefaultRouter
from artists.api import ArtistsViewset,ShowViewset,TypeViewset,IncomeViewset,ExpenseViewset,UsersViewset,UserProfileViewSet


router = DefaultRouter()
router.register("artists", ArtistsViewset, basename="artists")
router.register("show", ShowViewset, basename="show")
router.register("type", TypeViewset, basename="type")
router.register("income", IncomeViewset, basename="income")
router.register("expense", ExpenseViewset, basename="expense")
router.register("users", UsersViewset, basename="users")
router.register("user-profile", UserProfileViewSet, basename="user-profile")

urlpatterns = [
    path('', views.ShowArtistsView.as_view()),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
