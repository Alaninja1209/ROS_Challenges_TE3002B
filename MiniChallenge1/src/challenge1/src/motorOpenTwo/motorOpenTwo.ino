#include <ros.h>
#include <std_msgs/Float32.h>
#include <geometry_msgs/Twist.h>
#define PWM 4
#define PWM2 2
#define INPUT_MOTOR1 18 //Derecho
#define INPUT_MOTOR2 15 //Derecho
#define INPUT_MOTOR3 13 //Izquierdo
#define INPUT_MOTOR4 14 //Izquierdo

ros::NodeHandle motor;
void moveCar(const geometry_msgs::Twist &twistMsg){
 const float wheelbase=19.4/100;
 float V=twistMsg.linear.x;
 float W=twistMsg.angular.z;


 float rightWheelVel=V-wheelbase*W;
 float lefWheelVel=V+wheelbase*W;

 ledcWrite(0, abs((int)(rightWheelVel) * 255));
 ledcWrite(1, abs((int)(lefWheelVel) * 255));


 if(rightWheelVel < 0){
   digitalWrite(INPUT_MOTOR2, 0);
   digitalWrite(INPUT_MOTOR1, 1);

 }
 else{
   digitalWrite(INPUT_MOTOR1, 0);
   digitalWrite(INPUT_MOTOR2, 1);
 
 }
  if(lefWheelVel < 0){

   digitalWrite(INPUT_MOTOR3, 0);
   digitalWrite(INPUT_MOTOR4, 1);
 }
 else{
   digitalWrite(INPUT_MOTOR4, 0); 
   digitalWrite(INPUT_MOTOR3, 1);
     
 }
 
}

ros::Subscriber<geometry_msgs::Twist> sub("/cmd_vel", moveCar);
void setup(){
 ledcSetup(0, 980, 8);
 pinMode(INPUT_MOTOR1, OUTPUT);
 pinMode(INPUT_MOTOR2, OUTPUT);
 pinMode(PWM, OUTPUT);
 pinMode(INPUT_MOTOR3, OUTPUT);
 pinMode(INPUT_MOTOR4, OUTPUT);
 pinMode(PWM2, OUTPUT);
 ledcAttachPin(PWM, 0);
 ledcAttachPin(PWM2, 1);

 motor.initNode();
 motor.subscribe(sub);
}


void loop() {
 motor.spinOnce();
 delay(100);
}