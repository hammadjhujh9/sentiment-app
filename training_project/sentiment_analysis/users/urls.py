from django.urls import path
from .views import login_view, logout_view, index, signup_view, upload_sentence

urlpatterns = [
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('index/', index, name='index'),
    path('signup/', signup_view, name='signup'),
    path('upload/', upload_sentence, name='upload'),
]
