from django.urls import path
from . import views

app_name='user'

urlpatterns = [
    path('', views.index, name='index' ),
    path('login/', views.login, name='login'  ),
    path('logout/', views.logout, name='logout'  ),
    path('save/', views.save, name='save' ),
    path('restart/', views.restart, name='restart' ),
    path('shutdown/', views.shutdown, name='shutdown' ),
    path('upload/', views.upload_doc, name='upload' ),
    path('update/', views.update, name='update' ),
    path('flash/', views.flash, name='flash' ),
    
    path('adcconfig/', views.adcconfig, name='adcconfig' ),
    path('adcsave/', views.adcsave, name='adcsave' ),    
    path('ssengconfig/', views.ssengconfig, name='ssengconfig' ),
    path('ssengsave/', views.ssengsave, name='ssengsave' ),
    path('ssengconfig2/', views.ssengconfig2, name='ssengconfig2' ),
    path('ssengsave2/', views.ssengsave2, name='ssengsave2' ),
    path('inidownload/', views.inidownload, name='inidownload' ),
    path('swupload/', views.swupload, name='swupload' ),
    path('swupdate/', views.swupdate, name='swupdate' ),
    path('swflash/', views.swflash, name='swflash' ),    
    path('reboot/', views.reboot, name='reboot' ),
    path('download/<file_id>/', views.download, name='download'),    

]
