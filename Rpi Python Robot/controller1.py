import paho.mqtt.client as mqtt
import time
import os
mqtt_server_host = "10.3.141.1"
mqtt_server_port = 1883


addr_sys_startexit= "/wifi-py-rpi-car-controller/system/startexit"

def on_connect (client, userdata,flags, rc):
    print ("Connected, response code = " + str (rc))
    client.subscribe (addr_sys_startexit)

def on_message (client, userdata, msg):
    print ("topic [" + msg.topic + "] -> data [" + msg.payload + "]")
    if msg.topic == addr_sys_startexit:
        if msg.payload == "S":
            
            os.system("python2 /home/pi/Desktop/carRotate.py")
            

#client = mqtt.Client (client_id='controller', clean_session=True, userdata=None, protocol=mqtt.MQTTv31)
#client.on_connect = on_connect
#client.on_message = on_message

#client.connect (mqtt_server_host, mqtt_server_port, 60)
#client.loop_forever ()
            

client = mqtt.Client (client_id='controller', clean_session=True, userdata=None, protocol=mqtt.MQTTv31)
client.on_connect = on_connect
client.on_message = on_message

client.connect (mqtt_server_host, mqtt_server_port, 0.1) # ping once a minute
client.loop_forever ()
