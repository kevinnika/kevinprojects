
import paho.mqtt.client as mqtt
import serial
import time
import struct
import ticktock

# MQTT constants

# local implementation dependent/ ip address of broker
mqtt_server_host = "10.3.141.1"
# default port for MQTT
mqtt_server_port = 1883

#below are all the topics recieved/sent to broker defined in a varible.
addr_car_xy   = "/wifi-py-rpi-car-controller/car/XY"
addr_dash_xy  = "/wifi-py-rpi-car-controller/dash/XY"
addr_rotate="/wifi-py-rpi-car-controller/system/rotate"
addr_sys_startexit = "/wifi-py-rpi-car-controller/system/startexit"

ser = serial.Serial('/dev/ttyACM0',115200)#opening the serial port to allow for communication with arduino

class car_controller (object):
    def __init__ (self):
        self.queue_controller = ticktock.qController (self, 0.1) # 0.1 = tenth of a second
        
        self.latest_position = "0 0" #variable initialised to store x,y coordiantes from website 
        self.rotate="N"  #variable inistialise to change depenig on rotation state on the website 

       
        
        # ----
        return

    def tock (self, data):
        # This function is called periodically every 0.1 seconds can be changed by changing value sent to qController
        print ('tock: latest position = ' + self.latest_position) #printing the value of x,y from website. Used for debbugging purposes 
        client.publish (addr_car_xy, self.latest_position) #sending x,y coordinates recived from website back to the website through the broker for feedback
       
        sending_to_ard()#runs this function that sends x,y coordiantes recvied from website to arduino

        # ----
        return True

    def event (self, name, value):
        # This is command is called for within the program and has a higher priority in the queue then tock so runs more urgently when called
        print ('event: name=' + name + ', value=' + value) #prints the name and value passed through to this function when called which in this case is the topic and message
        if name == addr_dash_xy: #if statement checking what the topic received was and if it is xy coordiante then next bit of code runs
            self.latest_position = value #stores the value of xy recived from wesite to self.latest_position varible
            self.rotate="N" #sets the rotation state to N or not rotating in this case
        if name== addr_rotate: #if topic recived was for rotation then this code runs 
            self.rotate=value       #sets value recived from website to self.rotate can be either "Y" or "N"
            self.latest_position= "0 0" #sets the xy coordiantes recived to 0 if rotate has been received 
        
        
        # ----
        return True


    def command (self, name, value):
        self.queue_controller.event (name, value)  #when called sends the topic and message from the mqtt here and places it in the event queue to be processed
        return

    def stop (self):
        self.queue_controller.stop ()  #when called stops the ticktock program thus also stopping this one.
        return

    def run (self):
        self.queue_controller.run () #when called starts the ticktock while loop which keeps this running until that stops 
        return

# MQTT callbacks

def on_connect (client, car, flags, rc):        #this is called when client connection to broker is confirmed 
    print ("MQTT: on_connect: response code = " + str (rc) + ", flags = " + str (flags)) #prints the connection to mqtt used for debugging purposes 

    #python client subscribing to topics it want to recive messages on from the mqtt broker/website
    client.subscribe (addr_sys_startexit) #topic used to start and stop the car or confirm one or the other 
    client.subscribe (addr_dash_xy)  #topic that contains x,y coordiantes from website
    client.subscribe (addr_rotate)   #topic that contains the rotate state from website

def on_message (client, car, msg):  #this is called when broker sends a message to the python client 
    print ("topic [" + msg.topic + "] -> data [" + msg.payload + "]") #prints the topic name and message 
        
    if msg.topic == addr_sys_startexit: #checks to see what topic has been recived and if the startexit one then next bit of code is run 
        if msg.payload == "P": #if message from that topic was "P" run next bit
            car.stop()         #runs the stop function in the car_controller class which stops the ticktock loop thus ending this program 
            client.publish(addr_sys_startexit,"C") #if it has exited send a confirmation of this to the broker/website 
                          
    else:
            car.command (msg.topic, msg.payload) #if a diffrent topic to the one above is recived then run the command function from car_controller class that processes the information recived and assigns variables to it 
        
        
def sending_to_ard(): #function used to send data to arduino through serial communication 
     x,y= self.latest_position.split() #string being split in order to get x,y coordiantes seprate

     numberx=int(float(x)*127)        #turning x and y from a string to a int with range -127 to 127 to send as byte form
     numbery= int(float(y)*127)

     if self.rotate=="Y":     #if rotate state is Y/yes/true then assign it a value of 1 otherwise its 0
            r=1
     else:
            r=0

        if ser.isOpen():  #runs next bit of code that sends data to arduino only if the port for the python and arduino to communicate is open
            
               numberr_byte= struct.pack('<b', r)         #encoding all the values into byte forms so that they are easier /faster when it comes to sending to arduino 
               numberx_byte= struct.pack('<b', numberx)
               numbery_byte= struct.pack('<b', numbery)   #as serial communication works one byte at a time 

               ser.write(numberr_byte)    #sending the values recived from website to control the robot to the arduino in byte form
               ser.write(numberx_byte)
               ser.write(numbery_byte)
                
    
def connect_to_ard(): #called at the start of the program to initalise communication with arduino 
   ## is_connected= False
   # while not is_connected:
    #print("waiting for arduino...")
    
    time.sleep(5)      #timedelay to allow for arduino and pi serial port to be open and active 
    ser.write("hello") #writing a string to arduino to confirm that the connection has been made to arduino can continue with its code 
    time.sleep(5)      #ensures that arduino recives that message and has time to process it and start its program 
 
    

if __name__ == "__main__": #ran when this program is initally executed 
    connect_to_ard () #connects to arduino as soon as the program starts
    car = car_controller () #assigning the car_controller class to car
    
    client = mqtt.Client (client_id='car', clean_session=True, userdata=car, protocol=mqtt.MQTTv31) #creating a client instance for the broker so that it can coonect to it as a client
    client.on_connect = on_connect  #if client is connected or connection confirmed then on_connect function is run
    client.on_message = on_message   #if client recives a message from the broker it runs the on_message function 

    client.connect (mqtt_server_host, mqtt_server_port, 60) # ping once a minute
    client.publish(addr_sys_startexit,"A") #sends a message to broker confirming that this program has started 

    client.loop_start () #starts the client loop in the background and as long as this program is running as is the cllient part of it 
    car.run () #starts the car controller class which runs it __init__ function and starts ticktock
    
