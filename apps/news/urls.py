from django.urls import path
from .views import HomeView, DetailView

app_name = 'news'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('details/<int:news_id>/',DetailView.as_view(), name='details')
]