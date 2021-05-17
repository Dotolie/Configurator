from django.urls import path
from . import views

app_name='user'

urlpatterns = [
    path('', views.index, name='index' ),
    path('login/', views.login, name='login'  ),
    path('logout/', views.logout, name='logout'  ),
    path('save/', views.save, name='save' ),

    path('shutdown/', views.shutdown, name='shutdown' ),
    path('upload/', views.upload_doc, name='upload' ),
    path('update/', views.update, name='update' ),
    path('flash/', views.flash, name='flash' ),
    
    path('inidownload/', views.inidownload, name='inidownload' ),
    path('swupload/', views.swupload, name='swupload' ),
    path('swupdate/', views.swupdate, name='swupdate' ),
    path('swflash/', views.swflash, name='swflash' ),    
    path('reboot/', views.reboot, name='reboot' ),
    path('download/<file_id>/', views.download, name='download'),    


    path('tempflash2/', views.tempflash2, name='tempflash2' ),
    path('dustflash2/', views.dustflash2, name='dustflash2' ),
    path('disp/<int:question_id>', views.disp, name='disp'),
    path('dispdust/', views.dispdust, name='dispdust'),
    path('dustflash/', views.dustflash, name='dustflash' ),
    path('disptemp/', views.disptemp, name='disptemp'),
    path('tempflash/', views.tempflash, name='tempflash' ),
    path('restartdocker/', views.restartdocker, name='restartdocker' ),
    path('portsave/', views.portsave, name='portsave' ),
    path('periodconfig/', views.periodconfig, name='periodconfig' ),
    path('periodsave/', views.periodsave, name='periodsave' ),
    path('devices/', views.MyDeviceList.as_view(), name='devices'),
    path('devlist/', views.devlist, name='devlist'),    
    path('devlist2/', views.devlist2, name='devlist2'),    
    path('addDevice/', views.addDevice, name='addDevice'),
    path('devdelete/<int:question_id>', views.devdelete, name='devdelete'),
    path('devedit/<int:question_id>', views.devedit, name='devedit'),
    path('savelist', views.savelist, name='savelist'),

]
