"""djangotext1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib.auth.decorators import login_required
from django.urls import path, include
from home.views import UserHome, GetAllData, get_posts_choose, create_posts, update_posts, delete_posts, \
    RegisterView, UserAddArticle, UserLogin, UserLogout
from home import views
from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r'Posts', views.work_view_set)
#
# router1 = DefaultRouter()
# router1.register(r'Posts', views.get_set)

urlpatterns = [
    path('', UserLogin.as_view(), name='login'),
    path('home', login_required(UserHome.as_view()), name="home"),
    path(r'admin/', admin.site.urls),

    path('login/', UserLogin.as_view(), name="login"),
    path('register/', RegisterView.as_view(), name="register"),
    path('logout/', UserLogout.as_view(), name="logout"),
    path('article/', login_required(UserAddArticle.as_view()), name="article"),



    path('user', login_required(GetAllData.as_view())),
    path('user/<get_id>', login_required(get_posts_choose), name='get_choose'),
    path('user-posts', create_posts),
    path('update-posts/<mode_id>', update_posts, name='edit'),
    path('delete-posts/<data_id>', delete_posts, name='delete'),

    # path(r'api/', include(router.urls)),
    # path(r'get/', include(router1.urls)),

]
