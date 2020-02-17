from RTSim import RTSim

class RTRobot(RTSim):
    """
    RTRobot Controller for RTSim real-time robot simulation.
    https://github.com/FJFranklin/wifi-py-rpi-car-controller/tree/master/RTSim
    """
    

    def __init__(self, seconds):
        # usage: RTRobot (seconds)
        RTSim.__init__(self, seconds)

    def setup(self):
        # setup() is called once at the beginning

        # This is the Python version of the MEC3014 Courswork 'Matlab Robot':
        # Replace the number in the following line with your Student ID
        self.reset_barriers(150450014)
        self.target = self.get_target()       # where we're trying to get to

        # For example:
        self.last_ping_time = 0               # see ping_receive()
        self.last_ping_distance = -1

        
        
       
    def loop(self):
        # loop() is called repeatedly
        angle= 180
        # For example:
        currentTime = self.millis() / 1000
        
        
         
        self.position = self.get_GPS()        # roughly where we are
        self.orientation = self.get_compass() # which direction we're looking


        posX= self.position[0]   #x coordinate of robot
        posY=self.position[1]    #y coordinate of robot
        
        if currentTime > 0.1:
            self.set_ping_angle(angle+45)   #ping angle at right to 45 degrees same direction as robot is moving 
            self.ping_send()                 # it won't actually send more often than every 0.1s
            if self.target[1]>posY and posX>self.target[0]-1:      #if target is above the robot change ping angle so its more towards it 
               self.set_ping_angle(angle+20)
            


       

        if (posX<-4.75 or posX>=4.75 or posY<-4.75 or posY>=4.75) and (self.orientation<90 and self.orientation>270):            #in the rare cases it get stuck on the outside borders change ping angle to face wall 
            self.set_ping_angle(self.orientation+180)

        if (posX<-4.75 or posX>=4.75 or posY<-4.75 or posY>=4.75) and (self.orientation>90 and self.orientation<270):            #same as the other one but in a different orientation(up)
            self.set_ping_angle(self.orientation)

        
            

    def ping_receive(self, distance):
        angle=180
        posX= self.position[0]      
        posY=self.position[1]       
        # response to an self.ping_send()
       
       
        # For example:
        self.last_ping_time = self.millis()  # the last time we received a ping [in milliseconds]
        self.last_ping_distance = distance   # distance measured (-ve if no echo)
        
        if distance >= 0:                    # a -ve distance implies nothing seen
            print('position=(', self.position[0], ',', self.position[1], '),orientation=', self.orientation, '; distance=', distance, sep='')
            self.set_wheel_speeds(-100, -30) #turn left when ping detects barrier
        
            if posX<-4.75 or posX>=4.75 or posY<-4.75 or posY>=4.75:   #turn back when hitting the outside barriers 
               self.set_wheel_speeds(80,110)

         

        if distance<0:
            self.set_wheel_speeds(-105, -125)    #turn right when ping doesnt detect barrier. This could be changed to (-100,-125) for sharper turns and will still work.
            if self.target[1]>posY and posX>self.target[0]-1: #if target is above the robot change wheel speed so that it moves towards it.
               self.set_wheel_speeds(-120, -125)
              
        
    
             

            
            
               
           

        

        
        
            
            
            
            
