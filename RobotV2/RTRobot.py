from RTSim import RTSim



def find_mid_points(p1, p2):
    x1, y1 = p1
    x2, y2 = p2

    return ((x1 + x2)/2, (y1 + y2)/2)

class RTRobot(RTSim):

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

        self.obstacles = self._barriers[4:8]        # unique barriers defined from line 4 to 8 for the first and third barrier
        self.inner_obstacles = self._barriers[8:]   # unique barrier for the middle part

        self.left_top_line = self.obstacles[0][:2]    # defining the top line of left barrier (x,y)
        self.left_bottom_line = self.obstacles[1]     # defining bottom line of left barrier (x,y,w,h)
                    
        self.right_top_line = self.obstacles[2][:2]      # defining the top line of right barrier(x,y)
        self.right_bottom_line = self.obstacles[3]       # defining the bottom line of right barrier (x,y,w,h)

        self.inner_right_line =self.inner_obstacles[0]   #defining the right inner obstacle 
        self.inner_left_line =self.inner_obstacles[1]
         
        self.left_positionY=self.left_bottom_line[3]-5 #height subtracted by 5 gives the y cooridante of the bottom lines intersection bit
        self.right_positionY=self.right_bottom_line[3]-5 #same thing but for right hand barrier

        #finding the mid point of the gap in the left and right barriers to help with movement of robot
        #function to find mid point at beginning of code
        self.first_mid_point = find_mid_points(self.left_top_line, (self.left_bottom_line[0],self.left_positionY))
        self.second_mid_point = find_mid_points(self.right_top_line, (self.right_bottom_line[0],self.right_positionY))
        
    def loop(self):
        # loop() is called repeatedly

        angle= 180                 #variable defined to use for sonar angle 

        posX= self._position[0,0]  #x coordinate of robot
        posY=self._position[0,1]   #y coordinate of robot

        # For example:
        currentTime = self.millis() / 1000
      
        self.position = self.get_GPS()        # roughly where we are
        self.orientation = self.get_compass() # which direction we're looking

        
        if currentTime > 0.1:
            self.ping_send()                  # it won't actually send more often than every 0.1
            self.set_ping_angle(angle+30)     #sonar angle is constanstly to the top right of the robot, the same direction its moving
           
        
        
        if posX>self.first_mid_point[0]- 0.2  and posX<self.first_mid_point[0]:   #incase the robot gets stuck on the bottom line of the left barrier, -0.2 to take into account the width of the barrier 
            self.set_ping_angle(angle+90)                                          
                                                                                               
        if posX<self.second_mid_point[0] and posX>self.second_mid_point[0]-0.2:  #same as before but for second barrier  
            self.set_ping_angle(angle+90)

        if posY>self.inner_right_line[1] and posX>self.inner_right_line[0]-0.2 and posX<self.inner_right_line[0]: #just incase robot gets stuck in the inner obstacle(not really needed for my student number but added it in incase barriers would change)
            self.set_ping_angle(angle+90)

        if posX<=-4.77 or posX>=4.77 or posY<=-4.77 or posY>=4.77:            #for the rare cases the robot gets stuck on the overall barriers                              
            self.set_ping_angle(self.orientation+180)                         #sets sonar angle to where the robot is facing(+180 since it moves backwards the whole time)



    def ping_receive(self, distance):
        
        angle= 180
        posX= self._position[0,0] #x coordinate of robot 
        posY=self._position[0,1]  #y coordinate of robot
        # response to an self.ping_send()
        
        # For example:
        self.last_ping_time = self.millis()  # the last time we received a ping [in milliseconds]
        self.last_ping_distance = distance   # distance measured (-ve if no echo)

        if distance >= 0:                    # a -ve distance implies nothing seen
                    print('position=(', self.position[0], ',', self.position[1], '),orientation=', self.orientation, '; distance=', distance, sep='')
            
                    self.set_wheel_speeds(-124, -30)                                                                            #makes the robot turn left everytime sonar detects a barrier/wall
                    if posX>self.second_mid_point[0] and posY>self.right_positionY and self.target[1]<self.second_mid_point[1]: #change the robot direction based on target so it can hit the target
                         self.set_wheel_speeds(130, 80)                                                                         #makes the robot turn back, to the left
                         

                    if posY>self.inner_right_line[1] and posX>self.inner_left_line[0]and posX<self.inner_right_line[0]:         #added just incase the robot hits the inner obstacle will still moves towards the correct direction
                         self.set_wheel_speeds(80, 120)                                                                         #makes the robot turn back, to the right

                    if posX>self.first_mid_point[0]- 0.2  and posX<self.first_mid_point[0]: #makes the robot go back when at the first obstacle and sonar detects a barrier
                        self.set_wheel_speeds(80, 120)

                    if posX<self.second_mid_point[0] and posX>self.second_mid_point[0]-0.25: #makes the robot go back when at the second obstacle and sonar detects a barrier
                        self.set_wheel_speeds(80, 120)

                    if posX<=-4.77 or posX>=4.77 or posY<=-4.77 or posY>=4.77:  #makes the robot go back when at the outer walls and sonar detects a barrier
                        self.set_wheel_speeds(80, 127)
         

        if distance<0: #nothing seen from sonar so no barriers/walls detected
                   self.set_wheel_speeds(-102, -127)  #robot moving toward the right where the sonar angle should be

                   if posX>self.second_mid_point[0] and posY>self.right_positionY and self.target[1]>self.second_mid_point[1]:  #added to make it faster for robot to reach target
                       self.set_wheel_speeds(-120, -127) #coming out of the second obstacle, the robot is not turning to the right as much as target is in the top left


                 

     

                    
             

            
            
               
           

        

        
        
            
            
            
            
