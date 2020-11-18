# from devices import check
import os
import time
import paho.mqtt.client as mqtt
import json
from django.shortcuts import render
from .models import Devices
from django.contrib.auth.decorators import login_required


@login_required(login_url="/accounts/login")
def status(request):
    device = Devices.objects.raw(
        'SELECT id as id, name as name, status as status from devices_devices where name="posJed"')
    user = request.user
    status = "Connected"
    # while True:
    #     host = '10.11.12.249'
    #     HOST_UP = True if os.system("ping -c 2 " + host.strip(";")) is 0 else False
    #     time.sleep(2)
    #     status = ""
    #     if HOST_UP == True:
    #         status = "Connected"
    #         break
    #     elif HOST_UP == False:
    #         status = "Disconnected"
    #         break

    client = mqtt.Client()
    # client.on_connect = on_connect
    client.on_message = on_message
    client.connect("127.0.0.1", 1883, 60)
    client.loop_start()
    client.subscribe("dispenser")
    # client.subscribe([("dispenser"), ("capturer")])
    dispenser_entrance
    dispenser_exit
    capturer_entrance
    capturer_exit

    context = {
        'status': status,
        # 'sub_message':sub_message,
        'user': user,
        'dispenser_entrance': dispenser_entrance,
        'dispenser_exit': dispenser_exit,
        'capturer_entrance': capturer_entrance,
        'capturer_exit': capturer_exit,

    }

    return render(request, 'devices/status.html', context)


@login_required(login_url="/accounts/login")
def trigger_devices(request):
    return render(request, 'devices/trigger_devices.html')


dispenser_entrance = ""
dispenser_exit = ""
capturer_entrance = ""
capturer_exit = ""


def on_message(client, userdata, msg):
    # data_for = "{'" + str(msg.payload) + "', " + str(msg.topic) + "}"
    # print(str(msg.payload))
    # global glob
    pay = msg.payload
    # print(msg.topic)
    # ad = yaml.safe_load(pay)
    # s = json.dumps(ad, indent=4, sort_keys=True)
    global dispenser_entrance
    global dispenser_exit
    global capturer_entrance
    global capturer_exit
    global sub_message
    sub_message = str(pay.decode("utf-8", "ignore"))
    jsonData = json.loads(sub_message)
    dispenser_entrance = jsonData['dispenser_entrance']
    dispenser_exit = jsonData['dispenser_exit']
    capturer_entrance = jsonData['capturer_entrance']
    capturer_exit = jsonData['capturer_exit']
    print(jsonData['dispenser_entrance'])
    # glob = s
    # print(glob)
    # print(s)


def sub():
    client = mqtt.Client()
    # client.on_connect = on_connect
    client.on_message = on_message
    client.connect("127.0.0.1", 1883, 60)
    client.loop_start()
    client.subscribe("test")
