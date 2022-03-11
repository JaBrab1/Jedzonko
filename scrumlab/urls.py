"""scrumlab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from jedzonko.views import IndexView, Dashboard, RecipeID, RecipeList, RecipeAdd, RecipeModify, PlanAddRecipe, \
    PlanID, PlanAdd, PlanList, ContactView, AboutView, PlanModify, UserLogin, UserLogout, FullLoginView, AccountModify,\
    ChangeDateAccount, ResetPasswordView, DeleteUser, UserAllView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view()),
    path('main/', Dashboard.as_view()),
    path('recipe/<int:id>/', RecipeID.as_view()),
    path('recipe/list/', RecipeList.as_view()),
    path('recipe/add/', RecipeAdd.as_view()),
    path('recipe/modify/<int:id>/', RecipeModify.as_view()),
    path('plan/modify/<int:id>/', PlanModify.as_view()),
    path('plan/<int:id>/', PlanID.as_view()),
    path('plan/add/', PlanAdd.as_view()),
    path('plan/add-recipe/', PlanAddRecipe.as_view()),
    path('plan/list/', PlanList.as_view()),
    path('contact/', ContactView.as_view()),
    path('about/', AboutView.as_view()),
    path('login/', UserLogin.as_view(), name="login2"),
    path('logout/', UserLogout.as_view(), name="logout"),
    path('add_user/', FullLoginView.as_view(), name="fulllog"),
    path('modify/<int:id>/', AccountModify.as_view(), name="modify"),
    path('changedateuser/<int:id>/', ChangeDateAccount.as_view(), name="change"),
    path('reset_password/<int:id>/', ResetPasswordView.as_view(), name="reset"),
    path('deleteuser/<int:id>/', DeleteUser.as_view(), name="delete"),
    path('userall/', UserAllView.as_view(), name="view")
]
