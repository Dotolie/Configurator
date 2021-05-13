from django.shortcuts import render, redirect
from .models import Myuser
from django.http import HttpResponse
from django.contrib.auth import login as dlogin, logout as dlogout, authenticate
from configparser import ConfigParser
from .forms import DocumentForm
from .models import Document
from django.template import loader, RequestContext
from django.template import Context, Template

# ------ ywkim
from django.views.generic import TemplateView
from django.views.generic import ListView
from .models import MyDevice
from .forms import deviceForm
# ------ 

import subprocess 
import time
import datetime
import threading
import os.path
import mimetypes
import os
import zmq
import json


g_model = "it"
g_result = "start"

# Create your views here.
path_envlist = "/mnt/tmp/env_list.txt"
path_iotcap = "/tmp/iot-cap"
path_iotput = "/tmp/iot-put"
path_fpga = "/tmp/fpga"
path_work = "/home/iot-box/app"
path_device = "/home/iot-box/app/Configs/device.ini"

#path_configurator = "/home/configurator"
#path_configs = "/home/odroid/IOTEdge/iotedge/Configs/ssengine/"
#path_sconfig2 = "/home/odroid/IOTEdge/iotedge/Configs/ssengine/config_ssengine2.ini"
#path_sconfig = "/home/odroid/IOTEdge/iotedge/Configs/ssengine/config_ssengine.ini"
#path_aconfig = "/home/odroid/IOTEdge/iotedge/Configs/ssengine/adc.ini"

path_configurator = "/home/iot-box/Configurator"
path_configs = "/home/iot-box/app/Configs/"
path_tconfig = "/home/iot-box/app/Configs/period.ini"
path_sconfig = "/home/iot-box/app/Configs/device.ini"
path_aconfig = "/home/iot-box/app/Configs/config.ini"


path_pconfig = "/home/iot-box/app/Configs/config.ini"


def thflash():
    command = subprocess.check_output(["pwd"])
    aa=  command.decode('utf-8')
    print("thflash=", aa)
    
    run = subprocess.check_output(["chmod", "+x", "media/a64.sh"])
    run = subprocess.check_output(["./media/a64.sh"])

def flash(request):
    value = {}
    count=request.GET.get('count', None)            
    if int(count) == 0:
        t = threading.Thread(target=thflash)
        t.start()
    else:
        try:
            command = subprocess.check_output(["cat","./media/status"])
            value['command']=  command.decode('utf-8')
        except subprocess.CalledProcessError as e:
            value['command']= "error"

    return render(request, 'flash.html', value )

def upload_doc(request):
    if request.user.is_authenticated:
        context = {}
        form = DocumentForm()
        if request.method == 'POST':
            form = DocumentForm(request.POST, request.FILES)  # Do not forget to add: request.FILES
            update = request.POST.get('update', None)

            if update == None:
                if form.is_valid():
                    newdoc = Document(docfile=request.FILES['docfile'])
                    newdoc.save()
                    context['filename'] = request.FILES['docfile']
                    return render(request, 'upload_doc.html', context)
            else:
                return redirect('/user/update')

        return render(request, 'upload_doc.html', context)
    return redirect('/user/login')    

def update(request):
    if request.user.is_authenticated:
        return render(request, 'update.html')
    return redirect('/user/login')    

def ConfigRead():
    data = {}
    
    config_parser = ConfigParser()
    res = config_parser.read(path_sconfig)

    if res:
        ftpaddress = config_parser.get('COMMON', 'FTPADDRESS', fallback='10.166.101.49')
        ftpport = config_parser.get('COMMON', 'FTPPORT', fallback=21)
        samplerate = config_parser.get('COMMON', 'samplerate', fallback=20282)
        signaltype = config_parser.get('COMMON', 'Signaltype', fallback=1)
        cutoff = config_parser.get('COMMON', 'cutoff', fallback=10141)
        usefilter = config_parser.get('COMMON', 'use filter', fallback=1)
        window = config_parser.get('COMMON', 'window', fallback=3)
        taps = config_parser.get('COMMON', 'taps', fallback=16)

        ch_count = config_parser.get('CHANNEL', 'CH_count', fallback=4)
        ch0 = config_parser.get('CHANNEL', 'ch0', fallback=1)
        ch1 = config_parser.get('CHANNEL', 'ch1', fallback=1)
        ch2 = config_parser.get('CHANNEL', 'ch2', fallback=1)
        ch3 = config_parser.get('CHANNEL', 'ch3', fallback=1)

        busedopposite = config_parser.get('DATA', 'bUsedOpposite', fallback=0)
        ch0_gravity_calc = config_parser.get('DATA', 'ch0_Gravity_Calc', fallback=5)
        ch0_gravity_base = config_parser.get('DATA', 'ch0_Gravity_Base', fallback=5)
        ch0_const_current = config_parser.get('DATA', 'ch0_Const_Current', fallback=51.5)
        ch1_gravity_calc = config_parser.get('DATA', 'ch1_Gravity_Calc', fallback=5)
        ch1_gravity_base = config_parser.get('DATA', 'ch1_Gravity_Base', fallback=5)
        ch1_const_current = config_parser.get('DATA', 'ch1_Const_Current', fallback=51.5)
        ch2_gravity_calc = config_parser.get('DATA', 'ch2_Gravity_Calc', fallback=5)
        ch2_gravity_base = config_parser.get('DATA', 'ch2_Gravity_Base', fallback=5)
        ch2_const_current = config_parser.get('DATA', 'ch2_Const_Current', fallback=51.5)
        ch3_gravity_calc = config_parser.get('DATA', 'ch3_Gravity_Calc', fallback=5)
        ch3_gravity_base = config_parser.get('DATA', 'ch3_Gravity_Base', fallback=5)
        ch3_const_current = config_parser.get('DATA', 'ch3_Const_Current', fallback=51.5)
        ch4_gravity_calc = config_parser.get('DATA', 'ch4_Gravity_Calc', fallback=5)
        ch4_gravity_base = config_parser.get('DATA', 'ch4_Gravity_Base', fallback=5)
        ch4_const_current = config_parser.get('DATA', 'ch4_Const_Current', fallback=51.5)
        ch5_gravity_calc = config_parser.get('DATA', 'ch5_Gravity_Calc', fallback=5)
        ch5_gravity_base = config_parser.get('DATA', 'ch5_Gravity_Base', fallback=5)
        ch5_const_current = config_parser.get('DATA', 'ch5_Const_Current', fallback=51.5)
        ch6_gravity_calc = config_parser.get('DATA', 'ch6_Gravity_Calc', fallback=5)
        ch6_gravity_base = config_parser.get('DATA', 'ch6_Gravity_Base', fallback=5)
        ch6_const_current = config_parser.get('DATA', 'ch6_Const_Current', fallback=51.5)
        ch7_gravity_calc = config_parser.get('DATA', 'ch7_Gravity_Calc', fallback=5)
        ch7_gravity_base = config_parser.get('DATA', 'ch7_Gravity_Base', fallback=5)
        ch7_const_current = config_parser.get('DATA', 'ch7_Const_Current', fallback=51.5)
        ch8_gravity_calc = config_parser.get('DATA', 'ch8_Gravity_Calc', fallback=5)
        ch8_gravity_base = config_parser.get('DATA', 'ch8_Gravity_Base', fallback=5)
        ch8_const_current = config_parser.get('DATA', 'ch8_Const_Current', fallback=51.5)
        ch9_gravity_calc = config_parser.get('DATA', 'ch9_Gravity_Calc', fallback=5)
        ch9_gravity_base = config_parser.get('DATA', 'ch9_Gravity_Base', fallback=5)
        ch9_const_current = config_parser.get('DATA', 'ch9_Const_Current', fallback=51.5)
        ch10_gravity_calc = config_parser.get('DATA', 'ch10_Gravity_Calc', fallback=5)
        ch10_gravity_base = config_parser.get('DATA', 'ch10_Gravity_Base', fallback=5)
        ch10_const_current = config_parser.get('DATA', 'ch10_Const_Current', fallback=51.5)
        ch11_gravity_calc = config_parser.get('DATA', 'ch11_Gravity_Calc', fallback=5)
        ch11_gravity_base = config_parser.get('DATA', 'ch11_Gravity_Base', fallback=5)
        ch11_const_current = config_parser.get('DATA', 'ch11_Const_Current', fallback=51.5)
        ch12_gravity_calc = config_parser.get('DATA', 'ch12_Gravity_Calc', fallback=5)
        ch12_gravity_base = config_parser.get('DATA', 'ch12_Gravity_Base', fallback=5)
        ch12_const_current = config_parser.get('DATA', 'ch12_Const_Current', fallback=51.5)
        ch13_gravity_calc = config_parser.get('DATA', 'ch13_Gravity_Calc', fallback=5)
        ch13_gravity_base = config_parser.get('DATA', 'ch13_Gravity_Base', fallback=5)
        ch13_const_current = config_parser.get('DATA', 'ch13_Const_Current', fallback=51.5)
        ch14_gravity_calc = config_parser.get('DATA', 'ch14_Gravity_Calc', fallback=5)
        ch14_gravity_base = config_parser.get('DATA', 'ch14_Gravity_Base', fallback=5)
        ch14_const_current = config_parser.get('DATA', 'ch14_Const_Current', fallback=51.5)
        ch15_gravity_calc = config_parser.get('DATA', 'ch15_Gravity_Calc', fallback=5)
        ch15_gravity_base = config_parser.get('DATA', 'ch15_Gravity_Base', fallback=5)
        ch15_const_current = config_parser.get('DATA', 'ch15_Const_Current', fallback=51.5)

        eqpid = config_parser.get('VIB_Setting', 'EQPID', fallback='MVT')
        chid = config_parser.get('VIB_Setting', 'CHID', fallback='B')
        debug_mode_enable = config_parser.get('VIB_Setting', 'Debug_Mode_Enable', fallback=0)
        ftp_log_enable = config_parser.get('VIB_Setting', 'FTP_Log_Enable', fallback=0)
        ftp_log_raw_enable = config_parser.get('VIB_Setting', 'FTP_Log_Raw_Enable', fallback=0)
        ftp_log_feat_enable = config_parser.get('VIB_Setting', 'FTP_Log_Feat_Enable', fallback=0)
        ftp_log_buffer = config_parser.get('VIB_Setting', 'FTP_Log_Buffer', fallback=300)
        ftp_log_split = config_parser.get('VIB_Setting', 'FTP_Log_Split', fallback=2)
        sampled_n = config_parser.get('VIB_Setting', 'Sampled_N', fallback=20280)
        iot_send_interval = config_parser.get('VIB_Setting', 'IoT_Send_Interval', fallback=0)
        feat_t_set = config_parser.get('VIB_Setting', 'Feat_T_Set', fallback='11111111')
        feat_f_set = config_parser.get('VIB_Setting', 'Feat_F_Set', fallback='1111111444')
        ffeat_t_set = config_parser.get('VIB_Setting', 'FFeat_T_Set', fallback='11111111')
        ffeat_f_set = config_parser.get('VIB_Setting', 'FFeat_F_Set', fallback='1111111444')
        freq_remove_dc = config_parser.get('VIB_Setting', 'Freq_Remove_DC', fallback=0)
        freq_remove_dc_band = config_parser.get('VIB_Setting', 'Freq_Remove_DC_Band', fallback=5)
        freq_decend_n = config_parser.get('VIB_Setting', 'Freq_Decend_N', fallback=5)
        freq_band_num = config_parser.get('VIB_Setting', 'Freq_Band_Num', fallback=3)
        freq_band_1_center = config_parser.get('VIB_Setting', 'Freq_Band_1_Center', fallback=61)
        freq_band_1_range = config_parser.get('VIB_Setting', 'Freq_Band_1_Range', fallback=10)
        freq_band_2_center = config_parser.get('VIB_Setting', 'Freq_Band_2_Center', fallback=100)
        freq_band_2_range = config_parser.get('VIB_Setting', 'Freq_Band_2_Range', fallback=10)
        freq_band_3_center = config_parser.get('VIB_Setting', 'Freq_Band_3_Center', fallback=159)
        freq_band_3_range = config_parser.get('VIB_Setting', 'Freq_Band_3_Range', fallback=10)
        freq_band_4_center = config_parser.get('VIB_Setting', 'Freq_Band_4_Center', fallback=200)
        freq_band_4_range = config_parser.get('VIB_Setting', 'Freq_Band_4_Range', fallback=10)
        freq_band_5_center = config_parser.get('VIB_Setting', 'Freq_Band_5_Center', fallback=250)
        freq_band_5_range = config_parser.get('VIB_Setting', 'Freq_Band_5_Range', fallback=10)
        freq_band_6_center = config_parser.get('VIB_Setting', 'Freq_Band_6_Center', fallback=300)
        freq_band_6_range = config_parser.get('VIB_Setting', 'Freq_Band_6_Range', fallback=10)
        freq_band_7_center = config_parser.get('VIB_Setting', 'Freq_Band_7_Center', fallback=350)
        freq_band_7_range = config_parser.get('VIB_Setting', 'Freq_Band_7_Range', fallback=10)
        freq_band_8_center = config_parser.get('VIB_Setting', 'Freq_Band_8_Center', fallback=400)
        freq_band_8_range = config_parser.get('VIB_Setting', 'Freq_Band_8_Range', fallback=10)
        freq_band_9_center = config_parser.get('VIB_Setting', 'Freq_Band_9_Center', fallback=450)
        freq_band_9_range = config_parser.get('VIB_Setting', 'Freq_Band_9_Range', fallback=10)
        freq_band_10_center = config_parser.get('VIB_Setting', 'Freq_Band_10_Center', fallback=500)
        freq_band_10_range = config_parser.get('VIB_Setting', 'Freq_Band_10_Range', fallback=10)

        
    else:
        samplerate = 20282
        ftpaddress = '10.166.101.49'
        ftpport = 21
        signaltype = 1
        cutoff = 10141
        usefilter = 1
        window = 3
        taps = 16

        ch_count = 4
        ch0 = 1
        ch1 = 1
        ch2 = 1
        ch3 = 1
        
        busedopposite = 0
        ch0_gravity_calc = 5
        ch0_gravity_base = 5
        ch0_const_current = 51.5
        ch1_gravity_calc = 5
        ch1_gravity_base = 5
        ch1_const_current = 51.5
        ch2_gravity_calc = 5
        ch2_gravity_base = 5
        ch2_const_current = 51.5
        ch3_gravity_calc = 5
        ch3_gravity_base = 5
        ch3_const_current = 51.5
        ch4_gravity_calc = 5
        ch4_gravity_base = 5
        ch4_const_current = 51.5
        ch5_gravity_calc = 5
        ch5_gravity_base = 5
        ch5_const_current = 51.5
        ch6_gravity_calc = 5
        ch6_gravity_base = 5
        ch6_const_current = 51.5
        ch7_gravity_calc = 5
        ch7_gravity_base = 5
        ch7_const_current = 51.5
        ch8_gravity_calc = 5
        ch8_gravity_base = 5
        ch8_const_current = 51.5
        ch9_gravity_calc = 5
        ch9_gravity_base = 5
        ch9_const_current = 51.5
        ch10_gravity_calc = 5
        ch10_gravity_base = 5
        ch10_const_current = 51.5
        ch11_gravity_calc = 5
        ch11_gravity_base = 5
        ch11_const_current = 51.5
        ch12_gravity_calc = 5
        ch12_gravity_base = 5
        ch12_const_current = 51.5
        ch13_gravity_calc = 5
        ch13_gravity_base = 5
        ch13_const_current = 51.5
        ch14_gravity_calc = 5
        ch14_gravity_base = 5
        ch14_const_current = 51.5
        ch15_gravity_calc = 5
        ch15_gravity_base = 5
        ch15_const_current = 51.5

        eqpid = 'MVT'
        chid = 'B'
        debug_mode_enable = 0
        ftp_log_enable = 0
        ftp_log_raw_enable = 0
        ftp_log_feat_enable = 0
        ftp_log_buffer = 300
        ftp_log_split = 2
        sampled_n = 20280
        iot_send_interval =0 
        feat_t_set = '11111111'
        feat_f_set = '1111111444'
        ffeat_t_set = '11111111'
        ffeat_f_set = '1111111444'
        freq_remove_dc = 0
        freq_remove_dc_band = 5
        freq_decend_n = 5        
        freq_band_num = 3
        freq_band_1_center = 61
        freq_band_1_range = 10
        freq_band_2_center = 100
        freq_band_2_range = 10
        freq_band_3_center = 159
        freq_band_3_range = 10
        freq_band_4_center = 200
        freq_band_4_range = 10
        freq_band_5_center = 250
        freq_band_5_range = 10
        freq_band_6_center = 300
        freq_band_6_range = 10
        freq_band_7_center = 350
        freq_band_7_range = 10
        freq_band_8_center = 400
        freq_band_8_range = 10
        freq_band_9_center = 450
        freq_band_9_range = 10
        freq_band_10_center = 500
        freq_band_10_range = 10
        
        
    data['ftpaddress'] = ftpaddress
    data['ftpport'] = ftpport
    data['samplerate'] = samplerate
    data['signaltype'] = signaltype
    data['cutoff'] = cutoff
    data['usefilter'] = usefilter
    data['window'] = window
    data['taps'] = taps
    
    data['ch_count'] = ch_count
    data['ch0'] = ch0
    data['ch1'] = ch1
    data['ch2'] = ch2
    data['ch3'] = ch3

    data['busedopposite'] = busedopposite
    data['ch0_gravity_calc'] = ch0_gravity_calc
    data['ch0_gravity_base'] = ch0_gravity_base
    data['ch0_const_current'] = ch0_const_current

    data['ch1_gravity_calc'] = ch1_gravity_calc
    data['ch1_gravity_base'] = ch1_gravity_base
    data['ch1_const_current'] = ch1_const_current

    data['ch2_gravity_calc'] = ch2_gravity_calc
    data['ch2_gravity_base'] = ch2_gravity_base
    data['ch2_const_current'] = ch2_const_current

    data['ch3_gravity_calc'] = ch3_gravity_calc
    data['ch3_gravity_base'] = ch3_gravity_base
    data['ch3_const_current'] = ch3_const_current

    data['ch4_gravity_calc'] = ch4_gravity_calc
    data['ch4_gravity_base'] = ch4_gravity_base
    data['ch4_const_current'] = ch4_const_current

    data['ch5_gravity_calc'] = ch5_gravity_calc
    data['ch5_gravity_base'] = ch5_gravity_base
    data['ch5_const_current'] = ch5_const_current

    data['ch6_gravity_calc'] = ch6_gravity_calc
    data['ch6_gravity_base'] = ch6_gravity_base
    data['ch6_const_current'] = ch6_const_current
    
    data['ch7_gravity_calc'] = ch7_gravity_calc
    data['ch7_gravity_base'] = ch7_gravity_base
    data['ch7_const_current'] = ch7_const_current

    data['ch8_gravity_calc'] = ch8_gravity_calc
    data['ch8_gravity_base'] = ch8_gravity_base
    data['ch8_const_current'] = ch8_const_current

    data['ch9_gravity_calc'] = ch9_gravity_calc
    data['ch9_gravity_base'] = ch9_gravity_base
    data['ch9_const_current'] = ch9_const_current

    data['ch10_gravity_calc'] = ch10_gravity_calc
    data['ch10_gravity_base'] = ch10_gravity_base
    data['ch10_const_current'] = ch10_const_current

    data['ch11_gravity_calc'] = ch11_gravity_calc
    data['ch11_gravity_base'] = ch11_gravity_base
    data['ch11_const_current'] = ch11_const_current

    data['ch12_gravity_calc'] = ch12_gravity_calc
    data['ch12_gravity_base'] = ch12_gravity_base
    data['ch12_const_current'] = ch12_const_current

    data['ch13_gravity_calc'] = ch13_gravity_calc
    data['ch13_gravity_base'] = ch13_gravity_base
    data['ch13_const_current'] = ch13_const_current
    
    data['ch14_gravity_calc'] = ch14_gravity_calc
    data['ch14_gravity_base'] = ch14_gravity_base
    data['ch14_const_current'] = ch14_const_current

    data['ch15_gravity_calc'] = ch15_gravity_calc
    data['ch15_gravity_base'] = ch15_gravity_base
    data['ch15_const_current'] = ch15_const_current
    
    data['eqpid'] = eqpid;
    data['chid'] = chid;
    data['debug_mode_enable'] = debug_mode_enable
    data['ftp_log_enable'] = ftp_log_enable
    data['ftp_log_raw_enable'] = ftp_log_raw_enable
    data['ftp_log_feat_enable'] = ftp_log_feat_enable
    data['ftp_log_buffer'] = ftp_log_buffer
    data['ftp_log_split'] = ftp_log_split
    data['sampled_n'] = sampled_n
    data['iot_send_interval'] = iot_send_interval
    data['feat_t_set'] = feat_t_set
    data['feat_f_set'] = feat_f_set
    data['ffeat_t_set'] = ffeat_t_set
    data['ffeat_f_set'] = ffeat_f_set
    data['freq_remove_dc'] = freq_remove_dc
    data['freq_remove_dc_band'] = freq_remove_dc_band
    data['freq_decend_n'] = freq_decend_n
    data['freq_band_num'] = freq_band_num
    data['freq_band_1_center'] = freq_band_1_center
    data['freq_band_1_range'] = freq_band_1_range
    data['freq_band_2_center'] = freq_band_2_center 
    data['freq_band_2_range'] = freq_band_2_range
    data['freq_band_3_center'] = freq_band_3_center
    data['freq_band_3_range'] = freq_band_3_range
    data['freq_band_4_center'] = freq_band_4_center
    data['freq_band_4_range'] = freq_band_4_range
    data['freq_band_5_center'] = freq_band_5_center
    data['freq_band_5_range'] = freq_band_5_range
    data['freq_band_6_center'] = freq_band_6_center
    data['freq_band_6_range'] = freq_band_6_range
    data['freq_band_7_center'] = freq_band_7_center
    data['freq_band_7_range'] = freq_band_7_range
    data['freq_band_8_center'] = freq_band_8_center
    data['freq_band_8_range'] = freq_band_8_range
    data['freq_band_9_center'] = freq_band_9_center
    data['freq_band_9_range'] = freq_band_9_range
    data['freq_band_10_center'] = freq_band_10_center
    data['freq_band_10_range'] = freq_band_10_range

    return data


def AdcRead():
    data = {}
    
    config_parser = ConfigParser()
    res = config_parser.read(path_aconfig)

    if res:
        samplerate = config_parser.get('COMMON', 'samplerate', fallback=20282)
        cutoff = config_parser.get('COMMON', 'cutoff', fallback=10141)
        usefilter = config_parser.get('COMMON', 'use filter', fallback=0)
        window = config_parser.get('COMMON', 'window', fallback=3)
        taps = config_parser.get('COMMON', 'taps', fallback=16)

        ch0 = config_parser.get('CHANNEL', 'ch0', fallback=1)
        ch1 = config_parser.get('CHANNEL', 'ch1', fallback=1)
        ch2 = config_parser.get('CHANNEL', 'ch2', fallback=1)
        ch3 = config_parser.get('CHANNEL', 'ch3', fallback=1)

        ch4 = config_parser.get('CHANNEL', 'ch4', fallback=1)
        ch5 = config_parser.get('CHANNEL', 'ch5', fallback=1)
        ch6 = config_parser.get('CHANNEL', 'ch6', fallback=1)
        ch7 = config_parser.get('CHANNEL', 'ch7', fallback=1)
        ch8 = config_parser.get('CHANNEL', 'ch8', fallback=1)
        ch9 = config_parser.get('CHANNEL', 'ch9', fallback=1)
        ch10 = config_parser.get('CHANNEL', 'ch10', fallback=1)
        ch11 = config_parser.get('CHANNEL', 'ch11', fallback=1)
        ch12 = config_parser.get('CHANNEL', 'ch12', fallback=1)
        ch13 = config_parser.get('CHANNEL', 'ch13', fallback=1)
        ch14 = config_parser.get('CHANNEL', 'ch14', fallback=1)
        ch15 = config_parser.get('CHANNEL', 'ch15', fallback=1)

        voltage = config_parser.get('VOLTAGECHANNEL', 'ch0', fallback=1)
        
    else:
        samplerate = 20282
        cutoff = 10141
        usefilter = 0
        window = 3
        taps = 16

        ch0 = 1
        ch1 = 1
        ch2 = 1
        ch3 = 1

        ch4 = 1
        ch5 = 1
        ch6 = 1
        ch7 = 1
        ch8 = 1
        ch9 = 1
        ch10 = 1
        ch11 = 1
        ch12 = 1
        ch13 = 1
        ch14 = 1
        ch15 = 1

        voltage = 1
        
    data['samplerate'] = samplerate
    data['cutoff'] = cutoff
    if usefilter=='1':
        data['usefilter'] = usefilter
    data['window'] = window
    data['taps'] = taps

    if ch0=='1':
        data['ch0'] = ch0
    if ch1=='1':
        data['ch1'] = ch1
    if ch2=='1':
        data['ch2'] = ch2
    if ch3=='1':
        data['ch3'] = ch3

    if ch4=='1':
        data['ch4'] = ch4
    if ch5=='1':
        data['ch5'] = ch5
    if ch6=='1':        
        data['ch6'] = ch6
    if ch7=='1':        
        data['ch7'] = ch7
    if ch8=='1':        
        data['ch8'] = ch8
    if ch9=='1':
        data['ch9'] = ch9
    if ch10=='1':        
        data['ch10'] = ch10
    if ch11=='1':
        data['ch11'] = ch11
    if ch12=='1':
        data['ch12'] = ch12
    if ch13=='1':
        data['ch13'] = ch13
    if ch14=='1':
        data['ch14'] = ch14
    if ch15=='1':
        data['ch15'] = ch15
    if voltage=='1':
        data['voltage'] = voltage
        
    return data


def ConfigWrite(data):
    config_writer = ConfigParser()
    config_writer.optionxform = lambda option: option
    config_writer['COMMON'] = {
			'FTPADDRESS': data['ftpaddress'],
			'FTPPORT': data['ftpport'],
			'samplerate': data['samplerate'], 
			'Signaltype': data['signaltype'],
            'cutoff' : data['cutoff'],
            'use filter' : data['usefilter'],
            'window' : data['window'],
            'taps' : data['taps'],
	} 
    config_writer['CHANNEL'] = {
            'CH_count' : data['ch_count'],
            'CH0' : data['ch0'],
            'CH1' : data['ch1'],
            'CH2' : data['ch2'],
            'CH3' : data['ch3'],
    }
    config_writer['DATA'] = {
            'bUsedOpposite' : data['busedopposite'],
            'ch0_Gravity_Calc' : data['ch0_gravity_calc'],
            'ch0_Gravity_Base' : data['ch0_gravity_base'],
            'ch0_Const_Current' : data['ch0_const_current'],
            'ch1_Gravity_Calc' : data['ch1_gravity_calc'],
            'ch1_Gravity_Base' : data['ch1_gravity_base'],
            'ch1_Const_Current' : data['ch1_const_current'],
            'ch2_Gravity_Calc' : data['ch2_gravity_calc'],
            'ch2_Gravity_Base' : data['ch2_gravity_base'],
            'ch2_Const_Current' : data['ch2_const_current'],
            'ch3_Gravity_Calc' : data['ch3_gravity_calc'],
            'ch3_Gravity_Base' : data['ch3_gravity_base'],
            'ch3_Const_Current' : data['ch3_const_current'],
            'ch4_Gravity_Calc' : data['ch4_gravity_calc'],
            'ch4_Gravity_Base' : data['ch4_gravity_base'],
            'ch4_Const_Current' : data['ch4_const_current'],
            'ch5_Gravity_Calc' : data['ch4_gravity_calc'],
            'ch5_Gravity_Base' : data['ch5_gravity_base'],
            'ch5_Const_Current' : data['ch5_const_current'],
            'ch6_Gravity_Calc' : data['ch6_gravity_calc'],
            'ch6_Gravity_Base' : data['ch6_gravity_base'],
            'ch6_Const_Current' : data['ch6_const_current'],
            'ch7_Gravity_Calc' : data['ch7_gravity_calc'],
            'ch7_Gravity_Base' : data['ch7_gravity_base'],
            'ch7_Const_Current' : data['ch7_const_current'],
            'ch8_Gravity_Calc' : data['ch8_gravity_calc'],
            'ch8_Gravity_Base' : data['ch8_gravity_base'],
            'ch8_Const_Current' : data['ch8_const_current'],
            'ch9_Gravity_Calc' : data['ch9_gravity_calc'],
            'ch9_Gravity_Base' : data['ch9_gravity_base'],
            'ch9_Const_Current' : data['ch9_const_current'],
            'ch10_Gravity_Calc' : data['ch10_gravity_calc'],
            'ch10_Gravity_Base' : data['ch10_gravity_base'],
            'ch10_Const_Current' : data['ch10_const_current'],
            'ch11_Gravity_Calc' : data['ch11_gravity_calc'],
            'ch11_Gravity_Base' : data['ch11_gravity_base'],
            'ch11_Const_Current' : data['ch11_const_current'],
            'ch12_Gravity_Calc' : data['ch12_gravity_calc'],
            'ch12_Gravity_Base' : data['ch12_gravity_base'],
            'ch12_Const_Current' : data['ch12_const_current'],
            'ch13_Gravity_Calc' : data['ch13_gravity_calc'],
            'ch13_Gravity_Base' : data['ch13_gravity_base'],
            'ch13_Const_Current' : data['ch13_const_current'],
            'ch14_Gravity_Calc' : data['ch14_gravity_calc'],
            'ch14_Gravity_Base' : data['ch14_gravity_base'],
            'ch14_Const_Current' : data['ch14_const_current'],
            'ch15_Gravity_Calc' : data['ch15_gravity_calc'],
            'ch15_Gravity_Base' : data['ch15_gravity_base'],
            'ch15_Const_Current' : data['ch15_const_current'],
        }    

    config_writer['VIB_Setting'] = {
            'EQPID' : data['eqpid'],
            'CHID' : data['chid'],
            'Debug_Mode_Enable' : data['debug_mode_enable'],
            'FTP_Log_Enable' : data['ftp_log_enable'],
            'FTP_Log_Raw_Enable' : data['ftp_log_raw_enable'],
            'FTP_Log_Feat_Enable' : data['ftp_log_feat_enable'],
            'FTP_Log_Buffer' : data['ftp_log_buffer'],
            'FTP_Log_Split' : data['ftp_log_split'],
            'Sampled_N' : data['sampled_n'],
            'IoT_Send_Interval' : data['iot_send_interval'],
            'Feat_T_Set' : data['feat_t_set'],
            'Feat_F_Set' : data['feat_f_set'],
            'FFeat_T_Set' : data['ffeat_t_set'],
            'FFeat_F_Set' : data['ffeat_f_set'],
            'Freq_Remove_DC' : data['freq_remove_dc'],
            'Freq_Remove_DC_Band' : data['freq_remove_dc_band'],
            'Freq_Decend_N' : data['freq_decend_n'],
            'Freq_Band_Num' : data['freq_band_num'],
            'Freq_Band_1_Center' : data['freq_band_1_center'],
            'Freq_Band_1_Range' : data['freq_band_1_range'],
            'Freq_Band_2_Center' : data['freq_band_2_center'],
            'Freq_Band_2_Range' : data['freq_band_2_range'],
            'Freq_Band_3_Center' : data['freq_band_3_center'],
            'Freq_Band_3_Range' : data['freq_band_3_range'],
            'Freq_Band_4_Center' : data['freq_band_4_center'],
            'Freq_Band_4_Range' : data['freq_band_4_range'],
            'Freq_Band_5_Center' : data['freq_band_5_center'],
            'Freq_Band_5_Range' : data['freq_band_5_range'],
            'Freq_Band_6_Center' : data['freq_band_6_center'],
            'Freq_Band_6_Range' : data['freq_band_6_range'],
            'Freq_Band_7_Center' : data['freq_band_7_center'],
            'Freq_Band_7_Range' : data['freq_band_7_range'],
            'Freq_Band_8_Center' : data['freq_band_8_center'],
            'Freq_Band_8_Range' : data['freq_band_8_range'],
            'Freq_Band_9_Center' : data['freq_band_9_center'],
            'Freq_Band_9_Range' : data['freq_band_9_range'],
            'Freq_Band_10_Center' : data['freq_band_10_center'],
            'Freq_Band_10_Range' : data['freq_band_10_range'],
        }

def AdcWrite(data):
    config_writer = ConfigParser()
    config_writer.optionxform = lambda option: option
    config_writer['COMMON'] = {
			'samplerate': data['samplerate'], 
            'use filter' : data['usefilter'],
            'cutoff' : data['cutoff'],
            'window' : data['window'],
            'taps' : data['taps'],
	} 

    if ( g_model != "ITB_TYPE3" ):
        config_writer['CHANNEL'] = {
                'CH0' : data['ch0'],
                'CH1' : data['ch1'],
                'CH2' : data['ch2'],
                'CH3' : data['ch3'],
        }
    else:
        config_writer['CHANNEL'] = {
                'CH0' : data['ch0'],
                'CH1' : data['ch1'],
                'CH2' : data['ch2'],
                'CH3' : data['ch3'],
                'CH4' : data['ch4'],
                'CH5' : data['ch5'],
                'CH6' : data['ch6'],
                'CH7' : data['ch7'],
                'CH8' : data['ch8'],
                'CH9' : data['ch9'],
                'CH10' : data['ch10'],
                'CH11' : data['ch11'],
                'CH12' : data['ch12'],
                'CH13' : data['ch13'],
                'CH14' : data['ch14'],
                'CH15' : data['ch15'],
        }
        config_writer['VOLTAGECHANNEL'] = {
                'CH0' : data['voltage'],
        }
    
    with open(path_aconfig, 'w') as configfile:
        config_writer.write(configfile)



def index(request):
    response_data = {}
    global g_model
    
    if  request.user.is_authenticated:
        try:
            f = open(path_envlist, 'r')
            datas = f.readlines()
            f.close()
        except FileNotFoundError:
            datas = "not defined"
            
        for data in datas:
            if data.startswith('MVTECH'):
                serial = data
            else:
                serial = "not defined"

        f = open(path_device, 'r')
        device = f.read()
        f.close()
        devicelist = device.split("\n")

    
        for dev in devicelist:
            if dev.startswith('model'):
                dev.replace(" ", "")
                model = dev.split("=")
                g_model = model[1].strip()
            if dev.startswith('uid'):
                dev.replace(" ", "")
                uid = dev.split("=")
            if dev.startswith('siteid'):
                dev.replace(" ", "")
                siteid = dev.split("=")
            if dev.startswith('serverUri'):
                dev.replace(" ", "")
                server = dev.split("=")


        try:
            f = open(path_iotput, 'r')
            iotputversion = f.read()
            f.close()
        except FileNotFoundError:
            iotputversion = "not defined"
        
        try:
            f = open(path_iotcap, 'r');
            iotcapversion = f.read()
            f.close()
        except FileNotFoundError:
            iotcapversion = "not defined"

        try:
            f = open(path_fpga, 'r');
            fpgaversion = f.read()
            f.close()
        except FileNotFoundError:
            fpgaversion = "not defined"
            
        response_data['username'] = request.user.username
        response_data['model'] = model[1]   
        response_data['serial'] = serial
        response_data['uid'] = uid[1]
        response_data['siteid'] = siteid[1]
        response_data['server'] = server[1]
        response_data['iotcapver'] = iotcapversion
        response_data['iotputver'] = iotputversion
        response_data['fpgaver'] = fpgaversion

        return render( request, 'home-new.html', response_data ) 

    return redirect('/user/login')

def save(request):
    response_data = {}
    response_data['error'] = '' 

    if request.user.is_authenticated:      
        response_data['ftpaddress'] = request.POST.get('ftpaddress', "10.166.101.49")
        response_data['ftpport'] = request.POST.get('ftpport', 21)
        response_data['samplerate'] = request.POST.get('samplerate', 20282)
        if int(request.POST.get('samplerate')) > 65536:
            response_data['error'] = "Wrong value of samplerate," + request.POST.get('samplerate')

        response_data['signaltype'] = request.POST.get('signaltype', 1)
        response_data['cutoff'] = request.POST.get('cutoff', 10141)
        response_data['usefilter'] = request.POST.get('usefilter', 1)
        response_data['window'] = request.POST.get('window', 3)
        if int(request.POST.get('window')) > 100:
            response_data['error'] = "Wrong value of window," + request.POST.get('window')

        response_data['taps'] = request.POST.get('taps', 64)
        if int(request.POST.get('taps')) > 100:
            response_data['error'] = "Wrong value of taps," + request.POST.get('taps')

        response_data['ch_count'] = request.POST.get('ch_count', 4)
        if int(request.POST.get('ch_count')) > 4:
            response_data['error'] = "Wrong value of CH_count," + request.POST.get('ch_count')
        response_data['ch0'] = request.POST.get('ch0', 1)
        response_data['ch1'] = request.POST.get('ch1', 1)
        response_data['ch2'] = request.POST.get('ch2', 1)
        response_data['ch3'] = request.POST.get('ch3', 1)

        response_data['busedopposite'] = request.POST.get('busedopposite', 0)
        response_data['ch0_gravity_calc'] = request.POST.get('ch0_gravity_calc', 5)
        response_data['ch0_gravity_base'] = request.POST.get('ch0_gravity_base', 5)
        response_data['ch0_const_current'] = request.POST.get('ch0_const_current', 51.5)
        response_data['ch1_gravity_calc'] = request.POST.get('ch1_gravity_calc', 5)
        response_data['ch1_gravity_base'] = request.POST.get('ch1_gravity_base', 5)
        response_data['ch1_const_current'] = request.POST.get('ch1_const_current', 51.5)
        response_data['ch2_gravity_calc'] = request.POST.get('ch2_gravity_calc', 5)
        response_data['ch2_gravity_base'] = request.POST.get('ch2_gravity_base', 5)
        response_data['ch2_const_current'] = request.POST.get('ch2_const_current', 51.5)
        response_data['ch3_gravity_calc'] = request.POST.get('ch3_gravity_calc', 5)
        response_data['ch3_gravity_base'] = request.POST.get('ch3_gravity_base', 5)
        response_data['ch3_const_current'] = request.POST.get('ch3_const_current', 51.5)
        response_data['ch4_gravity_calc'] = request.POST.get('ch4_gravity_calc', 5)
        response_data['ch4_gravity_base'] = request.POST.get('ch4_gravity_base', 5)
        response_data['ch4_const_current'] = request.POST.get('ch4_const_current', 51.5)
        response_data['ch5_gravity_calc'] = request.POST.get('ch5_gravity_calc', 5)
        response_data['ch5_gravity_base'] = request.POST.get('ch5_gravity_base', 5)
        response_data['ch5_const_current'] = request.POST.get('ch5_const_current', 51.5)
        response_data['ch6_gravity_calc'] = request.POST.get('ch6_gravity_calc', 5)
        response_data['ch6_gravity_base'] = request.POST.get('ch6_gravity_base', 5)
        response_data['ch6_const_current'] = request.POST.get('ch6_const_current', 51.5)
        response_data['ch7_gravity_calc'] = request.POST.get('ch7_gravity_calc', 5)
        response_data['ch7_gravity_base'] = request.POST.get('ch7_gravity_base', 5)
        response_data['ch7_const_current'] = request.POST.get('ch7_const_current', 51.5)
        response_data['ch8_gravity_calc'] = request.POST.get('ch8_gravity_calc', 5)
        response_data['ch8_gravity_base'] = request.POST.get('ch8_gravity_base', 5)
        response_data['ch8_const_current'] = request.POST.get('ch8_const_current', 51.5)
        response_data['ch9_gravity_calc'] = request.POST.get('ch9_gravity_calc', 5)
        response_data['ch9_gravity_base'] = request.POST.get('ch9_gravity_base', 5)
        response_data['ch9_const_current'] = request.POST.get('ch9_const_current', 51.5)
        response_data['ch10_gravity_calc'] = request.POST.get('ch10_gravity_calc', 5)
        response_data['ch10_gravity_base'] = request.POST.get('ch10_gravity_base', 5)
        response_data['ch10_const_current'] = request.POST.get('ch10_const_current', 51.5)
        response_data['ch11_gravity_calc'] = request.POST.get('ch11_gravity_calc', 5)
        response_data['ch11_gravity_base'] = request.POST.get('ch11_gravity_base', 5)
        response_data['ch11_const_current'] = request.POST.get('ch11_const_current', 51.5)
        response_data['ch12_gravity_calc'] = request.POST.get('ch12_gravity_calc', 5)
        response_data['ch12_gravity_base'] = request.POST.get('ch12_gravity_base', 5)
        response_data['ch12_const_current'] = request.POST.get('ch12_const_current', 51.5)
        response_data['ch13_gravity_calc'] = request.POST.get('ch13_gravity_calc', 5)
        response_data['ch13_gravity_base'] = request.POST.get('ch13_gravity_base', 5)
        response_data['ch13_const_current'] = request.POST.get('ch13_const_current', 51.5)
        response_data['ch14_gravity_calc'] = request.POST.get('ch14_gravity_calc', 5)
        response_data['ch14_gravity_base'] = request.POST.get('ch14_gravity_base', 5)
        response_data['ch14_const_current'] = request.POST.get('ch14_const_current', 51.5)
        response_data['ch15_gravity_calc'] = request.POST.get('ch15_gravity_calc', 5)
        response_data['ch15_gravity_base'] = request.POST.get('ch15_gravity_base', 5)
        response_data['ch15_const_current'] = request.POST.get('ch15_const_current', 51.5)

        response_data['eqpid'] = request.POST.get('eqpid', 'MVT')
        response_data['chid'] = request.POST.get('chid', 'B')
        response_data['debug_mode_enable'] = request.POST.get('debug_mode_enable', 0)
        response_data['ftp_log_enable'] = request.POST.get('ftp_log_enable', 0)        
        response_data['ftp_log_raw_enable'] = request.POST.get('ftp_log_raw_enable', 0)
        response_data['ftp_log_feat_enable'] = request.POST.get('ftp_log_feat_enable', 0)
        response_data['ftp_log_buffer'] = request.POST.get('ftp_log_buffer', 300)
        response_data['ftp_log_split'] = request.POST.get('ftp_log_split', 2)
        response_data['sampled_n'] = request.POST.get('sampled_n', 20280)
        response_data['iot_send_interval'] = request.POST.get('iot_send_interval', 0)
        response_data['feat_t_set'] = request.POST.get('feat_t_set', '11111111')
        response_data['feat_f_set'] = request.POST.get('feat_f_set', '1111111444')
        response_data['ffeat_t_set'] = request.POST.get('ffeat_t_set', '11111111')
        response_data['ffeat_f_set'] = request.POST.get('ffeat_f_set', '1111111444')
        response_data['freq_remove_dc'] = request.POST.get('freq_remove_dc', 0)
        response_data['freq_remove_dc_band'] = request.POST.get('freq_remove_dc_band', 5)
        response_data['freq_decend_n'] = request.POST.get('freq_decend_N', 5)        
        response_data['freq_band_num'] = request.POST.get('freq_band_num', 3)
        response_data['freq_band_1_center'] = request.POST.get('freq_band_1_center', 61)
        response_data['freq_band_1_range'] = request.POST.get('freq_band_1_range', 10)
        response_data['freq_band_2_center'] = request.POST.get('freq_band_2_center', 100)
        response_data['freq_band_2_range'] = request.POST.get('freq_band_2_range', 10)
        response_data['freq_band_3_center'] = request.POST.get('freq_band_3_center', 159)
        response_data['freq_band_3_range'] = request.POST.get('freq_band_3_range', 10)
        response_data['freq_band_4_center'] = request.POST.get('freq_band_4_center', 200)
        response_data['freq_band_4_range'] = request.POST.get('freq_band_4_range', 10)
        response_data['freq_band_5_center'] = request.POST.get('freq_band_5_center', 250)
        response_data['freq_band_5_range'] = request.POST.get('freq_band_5_range', 10)
        response_data['freq_band_6_center'] = request.POST.get('freq_band_6_center', 300)
        response_data['freq_band_6_range'] = request.POST.get('freq_band_6_range', 10)
        response_data['freq_band_7_center'] = request.POST.get('freq_band_7_center', 350)
        response_data['freq_band_7_range'] = request.POST.get('freq_band_7_range', 10)
        response_data['freq_band_8_center'] = request.POST.get('freq_band_8_center', 400)
        response_data['freq_band_8_range'] = request.POST.get('freq_band_8_range', 10)
        response_data['freq_band_9_center'] = request.POST.get('freq_band_9_center', 450)
        response_data['freq_band_9_range'] = request.POST.get('freq_band_9_range', 10)
        response_data['freq_band_10_center'] = request.POST.get('freq_band_10_center', 500)
        response_data['freq_band_10_range'] = request.POST.get('freq_band_10_range', 10)
   

        response_data['username'] = request.user.username
        if response_data['error'] != '' :
            return render( request, 'home.html', response_data ) 
		
        ConfigWrite(response_data)	
        return render( request, 'saved.html', response_data)

    return redirect('/user/login')


def login(request):
    response_data = {}

    if os.path.isdir('/home/iot-box') is False:
        return HttpResponse('')
    
    if request.method == "GET" :
        return render(request, 'login.html')

    elif request.method == "POST":
        login_username = request.POST.get('username', None)
        login_password = request.POST.get('password', None)

        if not (login_username and login_password):
            response_data['error']="Please, Input your id & password."
        else : 
            user = authenticate(username=login_username, password=login_password)
            if user is not None:
                dlogin(request,user)
                return redirect('/')
            else:
                response_data['error'] = "Wrong password !!"

        return render(request, 'login.html',response_data)



def logout(request):
    dlogout(request)

    return redirect('/')

    
def threstartdocker():
    global g_result

    g_result = 'docker down'
    
    os.chdir(path_work)
    run = subprocess.check_output(["docker-compose", "down"])
    time.sleep(6)

    
    g_result = 'docker up'
    time.sleep(5)


    g_result = 'complete'
    run = subprocess.check_output(["docker-compose", "up"])
    g_result = ''

    run = subprocess.check_output('sync')
    time.sleep(2)



def restartdocker(request):
    response_data = {}

    if request.user.is_authenticated:

        t = threading.Thread(target=threstartdocker)
        t.start()
        
        response_data['model'] = g_model
        return render(request, 'restartdocker.html', response_data )

        
    return redirect('/user/login') 



def reboot(request):
    response_data = {}

    if request.user.is_authenticated:
        response_data['username'] = request.user.username
        run = subprocess.check_output('sync')
        return render(request, 'reboot.html', response_data)
        
    return redirect('/user/login')

def thdown():
    run = subprocess.check_output('reboot')
    
def shutdown(request):

    if request.user.is_authenticated:
        dlogout(request)
        t = threading.Thread(target=thdown)
        t.start()
        return HttpResponse("<h1>Rebooting ...</h1>")    

    return redirect('/user/login')


def inidownload(request):
    response_data = {}
    fname = ""
    if request.user.is_authenticated:
        form = DocumentForm()
        if request.method == 'POST':
            form = DocumentForm(request.POST, request.FILES)  # Do not forget to add: request.FILES

            if form.is_valid():
                newdoc = Document(docfile=request.FILES['docfile'])
                newdoc.save()
                fname ="./media/" + request.FILES['docfile'].name
                cmd = ["mv"]
                cmd.append(fname);
                cmd.append( path_configs )
                print(cmd)               
                run = subprocess.check_output(cmd)
                
        filenames = os.listdir(path_configs)
        fileitems = []

        for filename in filenames:
            items = []
            items.append(filename)
            items.append(time.ctime(os.path.getctime( path_configs+filename )))
            fileitems.append(items)
        fileitems.sort()
        
        response_data['filetimes'] = fileitems;
        response_data['dirname'] = path_configs;
        response_data['model'] = g_model;        
        return render( request, 'inidownload.html', response_data )
        
    return redirect('/user/login')


def thswupdate(name):
    global g_result

    g_result = 'docker down'
    
    os.chdir(path_work)
    run = subprocess.check_output(["docker-compose", "down"])
    time.sleep(1)

    g_result = 'move file'    
    os.chdir(path_configurator)

    cmd = ["chmod"]
    cmd.append("+x")
    cmd.append(name)
    run = subprocess.check_output(cmd)
    time.sleep(1)
    
    cmd = ["mv"]
    cmd.append(name);
    cmd.append( path_work )
    print(cmd)
    run = subprocess.check_output(cmd)
    time.sleep(2)
    
    g_result = 'docker up'
    time.sleep(6)

    g_result = 'complete'
    os.chdir(path_work)
    run = subprocess.check_output(["docker-compose", "up"])
    g_result = ''



def swupload(request):
    if request.user.is_authenticated:
        response_data = {}

        form = DocumentForm()
        if request.method == 'POST':
            form = DocumentForm(request.POST, request.FILES)  # Do not forget to add: request.FILES

            if form.is_valid():
                newdoc = Document(docfile=request.FILES['docfile'])
                newdoc.save()

                fname ="./media/" + request.FILES['docfile'].name
                t = threading.Thread(target=thswupdate, args=(fname,))
                t.start()
                
                return redirect('/user/swupdate')

        response_data['model'] = g_model        
        return render( request, 'swupload.html', response_data )
        
    return redirect('/user/login') 

def swupdate(request):
    if request.user.is_authenticated:
        response_data = {}
        
        response_data['model'] = g_model        
        return render(request, 'swupdate.html', response_data )
        
    return redirect('/user/login')    

def swflash(request):
    value = {}
    count=request.GET.get('count', None)
    value['command']= g_result

    return render(request, 'flash.html', value )

def tempflash(request):
    if request.user.is_authenticated:
        value = {}
        temp = 0.0
        hum = 0.0
        fnd = 0
        
        count=request.GET.get('count', None)
        
        # Socket to talk to server
        context = zmq.Context()
        socket = context.socket(zmq.SUB)
        socket.connect ("tcp://localhost:6001")
        socket.setsockopt_string(zmq.SUBSCRIBE, '')
        
        for i in range(1,6):
            string = socket.recv_multipart()
            msg = string[0].decode()
            ch = json.loads(msg)
            
            msg = string[1].decode()
            dic = json.loads(msg)
        
            data = dic['data']
            data0 = data[0]
            data1 = data[1]

            meastime = dic['meas_time']
        
            t = meastime

            for key, val in data0.items():
                if key.find('temp') != -1:
                    temp = val
            for key, val in data1.items():        
                if key.find('hum') != -1:
                    hum = val
                    fnd = 1
            if fnd == 1:
                print(i, "t=", temp, "h=", hum)
                break

        
        value['command'] = [t, temp, hum]
        

        return render(request, 'flash.html', value )

    return redirect('/user/login')


def dustflash(request):
    if request.user.is_authenticated:
        value = {}
        pm1 = 0.0
        pm2p5 = 0.0
        pm4 = 0.0
        pm10 = 0.0        
        fnd = 0
        
        count=request.GET.get('count', None)
        
        # Socket to talk to server
        context = zmq.Context()
        socket = context.socket(zmq.SUB)
        socket.connect ("tcp://localhost:6001")
        socket.setsockopt_string(zmq.SUBSCRIBE, '')
        
        for i in range(1,16):
            string = socket.recv_multipart()
            msg = string[0].decode()
            ch = json.loads(msg)
            
            msg = string[1].decode()
            dic = json.loads(msg)

            meastime = dic['meas_time']
        
            data = dic['data']

            if len(data) > 3:
                data0 = data[0]
                data1 = data[1]
                data2 = data[2]
                data3 = data[3]
            
                for key, val in data0.items():
                    if key.find('pcMass-1.0') != -1:
                        pm1 = val
                for key, val in data1.items():        
                    if key.find('pcMass-2.5') != -1:
                        pm2p5 = val
                for key, val in data2.items():
                    if key.find('pcMass-4.0') != -1:
                        pm4 = val
                for key, val in data3.items():        
                    if key.find('pcMass-10') != -1:
                        pm10 = val
                        fnd = 1
                    
            if fnd == 1:
                print(i, "p1=", pm1, "p2.5=", pm2p5, "p4=", pm4, "p10=", pm10)
                break

        
        value['command'] = [meastime, pm1, pm2p5, pm4, pm10]
        

        return render(request, 'flash.html', value )

    return redirect('/user/login')


def download(request, file_id):
    file_name = path_configs + file_id

    with open(file_name, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="text/plain")
        response['Content-Disposition'] = 'attachment;filename*=UTF-8\'\'%s' % file_id
        return response
    return HttpResponse('file not found')  

def dispdust(request):
    response_data = {}

    if request.user.is_authenticated:
        config_parser = ConfigParser()
        res = config_parser.read(path_aconfig)

        response_data['ylabel'] = "PM1.0, 2.5, 4.0, 10 [um/m3]"


        response_data['model'] = g_model
        return render(request, 'dispdust.html', response_data )
        
    return redirect('/user/login')    


def disptemp(request):
    response_data = {}

    if request.user.is_authenticated:
        config_parser = ConfigParser()
        res = config_parser.read(path_aconfig)

        response_data['ylabel'] = "Temp [°C] & Hum [%RH]"


        response_data['model'] = g_model
        return render(request, 'disptemp.html', response_data )
        
    return redirect('/user/login')    

def portsave():
    data = {}
    mainCh = ["CH1", "CH2", "CH3", "CH4", "CH5", "CH6", "CH7", "CH8", "CH9", "CH10", "CH11", "CH12", "CH13", "CH14", "CH15", "CH16"]
    subCh = ["ch1", "ch2", "ch3", "ch4", "ch5", "ch6", "ch7", "ch8"] 


    devices = MyDevice.objects.all()
    devices = MyDevice.objects.order_by('mainPort', 'subPort')

    f=open(path_pconfig, 'w')

    data = ";\r\n"
    data += "; Generated config.ini file for IOT-DIGITAL\r\n"
    data += "; device : IFBOARD, SHT3x, SPS30, LK15C1\r\n"
    data += "; bus : 0-i2c, 1-rs485, 2-rs232\r\n"
    data += "; main   speed : 1=4800,2=9600,3=9600,4=19200,5=38400,6=57600,7=115200 baud\r\n"
    data += "; if(232)speed : 1=4800,2=9600,3=14400,4=19200,5=38400,6=57600,7=115200 baud\r\n"
    data += "; if(i2c)speed : 1=10,2=40,3=100,4=200,5=400,6=800,7=1000 KHz\r\n"
    data += ";\r\n"
    data += "; ex)\r\n"
    data += "; [CH1]\r\n"
    data += "; device = IFBOARD\r\n"
    data += "; speed = 7\r\n"
    data += "; bus = 2\r\n"
    data += ";\r\n"
    data += "; ch1_device = SHT3x\r\n"
    data += "; ch1_speed = 2\r\n"
    data += "; ch1_bus = 0\r\n"
    data += ";\r\n"
    f.write(data)
    
    for dev in devices:
        print(dev.mainPort, dev.subPort, dev.deviceName,)
    
        if dev.subPort == 0:
            data = "[" + mainCh[dev.mainPort-1] + "]\r\n"
            data += "device = " + dev.deviceName + "\r\n"
            data += "bus = " + str(dev.deviceBus) + "\r\n"
            data += "speed = " + str(dev.deviceSpeed) + "\r\n"
            data += "\r\n"
        else:
            data = subCh[dev.subPort-1]+'_device = ' + dev.deviceName  + "\r\n"
            data += subCh[dev.subPort-1]+'_bus = ' + str(dev.deviceBus) + "\r\n"
            data += subCh[dev.subPort-1]+'_speed = ' + str(dev.deviceSpeed) + "\r\n"
            data += "\r\n"
       
       
        f.write(data)

    f.close()


    return data


def periodconfig(request):
    f = open(path_tconfig, 'r')
    data = f.read()
    f.close()

    response_data = {'datas': data}
    response_data['username'] = request.user.username
    response_data['model'] = g_model

    return render( request, 'periodconfig.html', response_data )    

def periodsave(request):
    response_data = {}

    if request.user.is_authenticated:  
        data = request.POST.get('config', "no")

        f = open(path_tconfig, 'w')
        f.write(data)
        f.close()
    
    return render( request, 'saved.html', response_data)


def PortRead():
    data = {}
    mainCh = ["CH1", "CH2", "CH3", "CH4", "CH5", "CH6", "CH7", "CH8", "CH9", "CH10", "CH11", "CH12", "CH13", "CH14", "CH15", "CH16"]
    subCh = ["ch1", "ch2", "ch3", "ch4", "ch5", "ch6", "ch7", "ch8"] 

    mCh = 0;
    sCh = 0;
    
    mDevice = ""
    mBus = 2
    mSpeed = 7

    sDevice = ""
    sBus = 0
    sSpeed = 2
    
    config_parser = ConfigParser()
    res = config_parser.read(path_pconfig)
      
    if res:
        for mPort in mainCh:
            mDevice = config_parser.get(mPort, 'device', fallback="none")
            mBus = config_parser.get(mPort, 'bus', fallback=2)
            mSpeed = config_parser.get(mPort, 'speed', fallback=7)
            
            if mDevice=='IFBOARD':
                mCh = mainCh.index(mPort)+1
                sCh = 0

                device = MyDevice(mainPort=mCh, subPort=sCh, deviceName=mDevice, deviceBus=mBus, deviceSpeed=mSpeed )
                device.save()

                for sPort in subCh:
                    sCh = subCh.index(sPort)+1
                    sDevice = config_parser.get(mPort, sPort+'_device', fallback="none")
                    sBus = config_parser.get(mPort, sPort+'_bus', fallback=0)
                    sSpeed = config_parser.get(mPort, sPort+'_speed', fallback=2)

                    if sDevice != 'none':
                        device = MyDevice(mainPort=mCh, subPort=sCh, deviceName=sDevice, deviceBus=sBus, deviceSpeed=sSpeed )
                        device.save()
                        
            elif mDevice != 'none':
                mCh = mainCh.index(mPort)+1
                sCh = 0
                
                device = MyDevice(mainPort=mCh, subPort=sCh, deviceName=mDevice, deviceBus=mBus, deviceSpeed=mSpeed )
                device.save()
                
    
    return data

class MyDeviceList(ListView):
    model = MyDevice
    template_name = 'devices.html'
    context_object_name = 'my_devices'
    
        
def addDevice(request):
    response_data = {}

    if request.user.is_authenticated:
        mPort = request.POST.get('mainPort', "0")
        sPort = request.POST.get('subPort', "0")
        devName = request.POST.get('deviceName', "none")
        devBus = request.POST.get('deviceBus', "0")
        devSpeed = request.POST.get('deviceSpeed', "0")

        dup = MyDevice.objects.filter(mainPort=mPort, subPort=sPort)
        if not dup:
            print("add new", mPort, sPort, devName, devBus, devSpeed)
            device = MyDevice(mainPort=mPort, subPort=sPort, deviceName=devName, deviceSpeed=devSpeed, deviceBus=devBus)
            device.save()
        else:
            print("duplicate", mPort, sPort, devName, devBus, devSpeed)
            response_data['error'] = 'Duplicate device: '+str(mPort) + '-' + str(sPort) + ' ' + devName

        devices = MyDevice.objects.all()        
        devices = MyDevice.objects.order_by('mainPort', 'subPort')
        
        response_data['object_list'] = devices 
        return render(request, 'devices.html', response_data)

    return redirect('/user/login')

def devlist(request):
    response_data = {}
    
    if request.user.is_authenticated:
        devices = MyDevice.objects.all()
        devices.delete()
        data = PortRead() 
        
        devices = MyDevice.objects.order_by('mainPort', 'subPort')

        response_data['object_list'] = devices
        return render(request, 'devices.html', response_data)
        
    return redirect('/user/login')

def devlist2(request):
    response_data = {}
    
    if request.user.is_authenticated:
        devices = MyDevice.objects.all()
        
        devices = MyDevice.objects.order_by('mainPort', 'subPort')

        response_data['object_list'] = devices 
        return render(request, 'devices.html', response_data)
        
    return redirect('/user/login')

def devdelete(request, question_id):
    if request.user.is_authenticated:
        device = MyDevice.objects.get(id=question_id);

        device.delete()

        return redirect("/user/devlist2");
    
    return redirect('/user/login')

def devedit(request, question_id):
    response_data={}
    
    if request.user.is_authenticated:
        device = MyDevice.objects.get(id=question_id);

        if request.method == 'GET' :
            print("quit=", question_id)
            return render(request, 'devedit.html', {'device':device})
        else:
            mPort = request.POST.get('mainPort', '0')
            sPort = request.POST.get('subPort', '0')
            devName = request.POST.get('deviceName', "none")
            devBus = request.POST.get('deviceBus', '0')
            devSpeed = request.POST.get('deviceSpeed', '0')

            if int(mPort) < 1 or int(mPort) > 16:
                response_data['error'] = 'Over range of Main Port='+ mPort
                response_data['device']=device
                return render(request, 'devedit.html', response_data)
                
            if int(sPort) < 0 or int(sPort) > 8:
                response_data['error'] = 'Over range of Sub Port='+ sPort
                response_data['device']=device
                return render(request, 'devedit.html', response_data)

            if devName != 'IFBOARD' and devName != 'SPS30' and devName != 'SHT3x' and devName != 'LK15C1':
                response_data['error'] = 'Does not support device='+ devName
                response_data['device']=device
                return render(request, 'devedit.html', response_data)

            if int(devBus) < 0 or int(devBus) > 2:
                response_data['error'] = 'Over range of Bus='+ devBus
                response_data['device']=device
                return render(request, 'devedit.html', response_data)

            if int(devSpeed) < 1 or int(devSpeed) > 7:
                response_data['error'] = 'Over range of Speed='+ devSpeed
                response_data['device']=device
                return render(request, 'devedit.html', response_data)
                
            dup = MyDevice.objects.filter(mainPort=mPort, subPort=sPort)
            if not dup:
                if device.subPort == 0:
                    dup2 = MyDevice.objects.filter(mainPort=device.mainPort)
                    for dev in dup2:
                        dev.mainPort = mPort
                        dev.save()

                device.mainPort = mPort
                device.subPort = sPort;
                device.deviceName = devName
                device.deviceBus = devBus
                device.deviceSpeed = devSpeed

                device.save()
                    
                return redirect("/user/devlist2")
            else:
                response_data['error'] = "Duplicate port : "+str(mPort) +"-" + str(sPort) + " " + devName
                response_data['device']=device
                
                return render(request, 'devedit.html', response_data)
    
    return redirect('/user/login')

def savelist(request):
    if request.user.is_authenticated:
        portsave()
        return render( request, 'saved.html')

    return redirect('/user/login')

