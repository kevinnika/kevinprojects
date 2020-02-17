   

/*!
* @file QuadMotorDriverShield.ino
* @brief QuadMotorDriverShield.ino  Motor control program
*
* Every 2 seconds to control motor positive inversion
* 
* @author linfeng(490289303@qq.com)
* @version  V1.0
* @date  2016-4-5
*/
//#define trigPin 10
//#define echoPin 13

const int E1 = 3; ///<Motor1 Speed
const int E2 = 11;///<Motor2 Speed
const int E3 = 5; ///<Motor3 Speed


const int M1 = 4; ///<Motor1 Direction
const int M2 = 12;///<Motor2 Direction
const int M3 = 8; ///<Motor3 Direction

int x = 0;
int y = 0;
int r = 0;

//unsigned long previousTime = 0;

//bool moveMotor = false;
bool is_connected=false;
String hello; 
//int timetaken,in,cm;
void M1_advance(char Speed) ///<Motor1 Advance
{
 digitalWrite(M1,LOW); 
 analogWrite(E1,Speed);
// Serial.print("Motor 1 100 speed forward"); 
}
void M2_advance(char Speed) ///<Motor2 Advance
{
 digitalWrite(M2,HIGH);
 analogWrite(E2,Speed);
 //Serial.print("Motor 2 100 speed forward"); 
}
void M3_advance(char Speed) ///<Motor3 Advance
{
 digitalWrite(M3,LOW);
 analogWrite(E3,Speed);
 //Serial.print("Motor 3 100 speed forward"); 
}

void M1_back(char Speed) ///<Motor1 Back off
{
 digitalWrite(M1,HIGH);
 analogWrite(E1,Speed);
 //Serial.print("Motor 1 100 speed backward"); 
}
void M2_back(char Speed) ///<Motor2 Back off
{
 digitalWrite(M2,LOW);
 analogWrite(E2,Speed);
 //Serial.print("Motor 2 100 speed backward");
}
void M3_back(char Speed) ///<Motor3 Back off
{
 digitalWrite(M3,HIGH);
 analogWrite(E3,Speed);
// Serial.print("Motor 3 100 speed backward");
}

void setup() {
 for(int i=3;i<9;i++)
    pinMode(i,OUTPUT);
  
 for(int i=11;i<13;i++)
    pinMode(i,OUTPUT);

// pinMode(trigPin,OUTPUT);
// pinMode(echoPin,INPUT);

  Serial.begin(115200);//  seial monitor initialized 
 // while (!Serial);

//  previousTime = millis();
  while (!is_connected)
  {
    delay(30) ;
    if (Serial.available()>0)
    {
      hello= Serial.readString();
      if (hello="hello")
      {
        
          is_connected=true;
          Serial.print ("connected");
      }
      else 
      {
        is_connected=false;
      }
       
   
    }
  }
}

void loop() {
  if (readDataFromRPi()) {
    driveInDirection(x,y);
    Rotate(r);
  }

//  unsigned long currentTime = millis();
//  if (currentTime - previousTime > 50) {
//    previousTime = currentTime;
//    readSensor();
//  }

}

bool readDataFromRPi () { 
  if (Serial.available() > 2) {
    r = (int8_t) Serial.read();
    x = (int8_t) Serial.read();
    y = (int8_t) Serial.read();
    return true;
  }
  return false;
}

void driveInDirection(float newX, float newY) {
  //  delay(3);
    float x = newX;
    float y = newY;
  
    float theta = atan2(y,x);
    float mag = sqrt((x*x) + (y*y));
    float vx = mag * cos(theta);
    float vy = mag * sin(theta);
 
  
    float w1 = -vx;
    float w2 = 0.5 * vx - sqrt(3)/2 * vy;
    float w3 = 0.5 * vx + sqrt(3)/2 * vy;
   
  
    // Get largest w value
 //   float wSet[] = {w1, w2, w3};
 //   float largestValue = 0.0;
  
  //  for (int i = 0; i < 3; i++)
 //   {
  //    if(abs(wSet[i]) > largestValue)
 //     {
  //      largestValue = abs(wSet[i]);
  //    }
  // }
  
  //  float speedCoef = (float)147.0 / largestValue;

  
  //  w1 = w1 * speedCoef;
  //  w2 = w2 * speedCoef;
  //  w3 = w3 * speedCoef; 

    if (x ==0 && y == 0)
     {
      w1 = 0;
      w2 = 0;
      w3 = 0;
    }

    
    w1 = constrain(w1, -110, 110);
    w2 = constrain(w2, -110, 110);
    w3 = constrain(w3, -110, 110);

    boolean w1_ccw = w1 < 0 ? true : false;
    boolean w2_ccw = w2 < 0 ? true : false;
    boolean w3_ccw = w3 < 0 ? true : false;
 
   
    byte w1_speed = (byte) map(abs(w1), 0, 110, 0, 255);
    byte w2_speed = (byte) map(abs(w2), 0, 110, 0, 255);
    byte w3_speed = (byte) map(abs(w3), 0, 110, 0, 255);

    if (w1_ccw== 1)
    {
      M1_back(w1_speed);
    }
    else 
    {
      M1_advance(w1_speed);
    }
   
    
    if (w2_ccw== 1)
    {
      M2_back(w2_speed);
    }
    else 
    {
      M2_advance(w2_speed);
    }
    
    if (w3_ccw== 1)
    {
      M3_back(w3_speed);
    }
    else 
    {
      M3_advance(w3_speed);
    }
    

    
  }

 void Rotate(int newr){
    if (newr==1){
    float w1=70;
    float w2=70;
    float w3=70;
    
    byte w1_speed = (byte) map(abs(w1), 0, 110, 0, 255);
    byte w2_speed = (byte) map(abs(w2), 0, 110, 0, 255);
    byte w3_speed = (byte) map(abs(w3), 0, 110, 0, 255);
    
    
    M1_advance(w1_speed);
    M2_advance(w1_speed);
    M3_advance(w1_speed);
    
    }
    
 }

 // void printMotorSpeed(byte motorSpeed, int motor)
//{
 //   Serial.print("Motor");
 //   Serial.print(motor);
  //  Serial.print(": ");
  //  Serial.println(motorSpeed); 
  //}

 void write_i8(int8_t num)
{
  Serial.write(num);
}

int8_t read_i8()
{
  wait_for_bytes(1, 100); // Wait for 1 byte with a timeout of 100 ms
  return (int8_t) Serial.read();
}

void wait_for_bytes(int num_bytes, unsigned long timeout)
{
  unsigned long startTime = millis();
  //Wait for incoming bytes or exit if timeout
  while ((Serial.available() < num_bytes) && (millis() - startTime < timeout)){}
}

//void readSensor(){
//
//   digitalWrite(trigPin,HIGH);
//   delay(5);
//   digitalWrite(trigPin,LOW);
//
//   timetaken =pulseIn(echoPin,HIGH);
//   digitalWrite(echoPin,LOW);
//
//   
//   cm= (timetaken/29)/2;
//   Serial.println(cm);
   //int16_t pm = cm; 
   //Serial.write(pm); 
//}
