from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('send_message', views.send_Message, name='send_Message'),
    path('automatic_reply', views.automatic_reply, name='automatic_reply'),
    path('get_channel', views.get_channel, name='get_channel'),
    path('chat_newmessage', views.chat_newmessage, name='chat_newmessage'),
    path('getTelegramCode', views.getTelegramCode, name='getTelegramCode'),
    path('update2fa', views.update2fa, name='update2fa'),
    path('send_code_request', views.send_code_request, name='send_code_request'),
    path('sign_up', views.send_code_request, name='sign_up'),
    path('get_sign_up', views.get_sign_up, name='get_sign_up'),
    path('sign_up_ok', views.sign_up_ok, name='sign_up_ok'),
    path('get_pubspeak_message', views.get_pubspeak_message, name='get_pubspeak_message'),
    path('join_channel', views.join_channel, name='join_channel'),
    path('get_user', views.get_user, name='get_user'),
    path('replyclient', views.replyclient, name='replyclient'),
    path('updateProfile', views.updateProfile, name='updateProfile'),
    path('channelVerify', views.channelVerify, name='channelVerify'),
    # path('asyncget_user', views.asyncget_user, name='asyncget_user'),
]