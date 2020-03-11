from django.urls import path
from . import views
from django.conf.urls import url


app_name = 'polls'
urlpatterns = [
    #path('', views.index, name='index'),
    path('',views.IndexView.as_view(),name='index'),
    #path('specifics/<int:question_id>',views.detail,name='detail'),
    path('specifics/<int:pk>/',views.DetailView.as_view(), name='detail'),
    #path('<int:question_id>/results/',views.results,name='results'),
    path('<int:pk>/results/',views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/',views.vote, name='vote'),
    path('addpoll/',views.add_poll, name='addpoll'),
    path('<int:question_id>/add_choice/',views.add_choice,name='add_choice'),
    path('login/', views.login_request , name='login'),
    path('logout/',views.logout_request,name='logout'),
    path('register', views.register, name='register'),


]
