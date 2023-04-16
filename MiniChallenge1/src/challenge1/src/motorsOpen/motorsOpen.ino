#include <ros.h>
#include <std_msgs/Float32.h>
#define PWM 4
#define PWM2 2
#define INPUT_MOTOR1 18 //Derecho
#define INPUT_MOTOR2 15 //Derecho
#define INPUT_MOTOR3 13 //Izquierdo
#define INPUT_MOTOR4 14 //Izquierdo

ros::NodeHandle motor;

void pwmCall(const std_msgs::Float32 &pwmMsg){
 ledcWrite(0, abs((int)(pwmMsg.data) * 255));


 if(pwmMsg.data > 0){
   digitalWrite(INPUT_MOTOR2, 0);
   digitalWrite(INPUT_MOTOR1, 1);
   digitalWrite(INPUT_MOTOR3, 0);
   digitalWrite(INPUT_MOTOR4, 1);
 }
 else{
   digitalWrite(INPUT_MOTOR1, 0);
   digitalWrite(INPUT_MOTOR2, 1);
   digitalWrite(INPUT_MOTOR3, 1);
   digitalWrite(INPUT_MOTOR4, 0);   
 }
}


ros::Subscriber<std_msgs::Float32> sub("/pwm", pwmCall);


void setup(){
 ledcSetup(0, 980, 8);
 pinMode(INPUT_MOTOR1, OUTPUT);
 pinMode(INPUT_MOTOR2, OUTPUT);
 pinMode(PWM, OUTPUT);
 pinMode(INPUT_MOTOR3, OUTPUT);
 pinMode(INPUT_MOTOR4, OUTPUT);
 pinMode(PWM2, OUTPUT);
 ledcAttachPin(PWM, 0);
 ledcAttachPin(PWM2, 0);

 motor.initNode();
 motor.subscribe(sub);
}


void loop() {
 motor.spinOnce();
 delay(100);
}