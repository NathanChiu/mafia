from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'player_profile'
# urlpatterns = [
#     path('',views.index, name='index'),
#     path('<int:question_id>/', views.detail, name="detail"),
#     path('<int:question_id>/results/', views.results, name="results"),
#     path('<int:question_id>/vote/', views.vote, name="vote"),
# ]
urlpatterns = [
    # path('', views.IndexView.as_view(), name='index'),
    path('', views.index, name='index'),
    # path('signup/', views.signup, name='signup'),
    # path('change_password/', views.change_password, name='change_password'),
    # path('logout/', views.logout, name='logout'),
    # path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # path('<int:question_id>/vote/', views.vote, name='vote'),
]
