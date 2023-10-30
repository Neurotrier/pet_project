from django.urls import path
from .views import *

urlpatterns = [
    path('', home_page, name='home'),
    path('registration/', Registration.as_view(), name='registration'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', logout_from_site, name='logout'),
    path('account/<str:username>/', Account.as_view(), name='account'),
    path('account/<str:username>/<slug:list_slug>/', ListFormView.as_view(), name='listform'),
    path('createlist/', CreateList.as_view(), name='createlist'),
    path('createtask/', CreateTask.as_view(), name='createtask'),
    path('deletetask/<int:pk>', DeleteTask.as_view(), name='deletetask'),
    path('updatetask/<int:pk>', UpdateTask.as_view(), name='updatetask'),
    path('deletelist/<int:pk>', DeleteList.as_view(), name='deletelist'),
]