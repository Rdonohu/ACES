#include <Wire.h>
#include <MPU6050.h>
#include <IRremote.h>

#define IR_RECEIVE_PIN 3
#define IR_BUTTON_1 16
#define IR_BUTTON_2 17
#define IR_BUTTON_3 18
#define IR_BUTTON_4 20
#define RED_PIN 11
#define GREEN_PIN 10
#define BLUE_PIN 9


MPU6050 mpu;

const float thresh = 1.1;
String incomingString;
bool lockState = false;
bool policeState = false;
unsigned long IRtransmission = 0 ;

void setup() {
  Serial.begin(9600);
  Wire.begin();
  mpu.initialize();

  if(!mpu.testConnection()){
    Serial.println("Connection Failed");
    while(1);
  } else {
    Serial.println("Connected!");
    
  }
  IrReceiver.begin(IR_RECEIVE_PIN);
  pinMode(RED_PIN, OUTPUT);
  pinMode(BLUE_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  setColor(255,0,255);
}

void loop() {
  //Read accelerometer values
  int16_t ax, ay, az;
  mpu.getAcceleration(&ax, &ay, &az);

  //convert acceleration to Gs
  float axG = ax / 16384.0;
  float ayG = ay / 16384.0;
  float azG = az / 16384.0;

  if (lockState) {
    //Send message if acceleration is greater than threshold
    if(abs(axG) > thresh || abs(ayG) > thresh || abs(azG) > thresh){
      Serial.print("BreakIn");
      delay(500);
    }
  }
  
  if (IrReceiver.decode()) {
    
    int command = IrReceiver.decodedIRData.command;
    switch (command){

      case IR_BUTTON_1: {
       Serial.print("ALock");
       break;
      }
      case IR_BUTTON_2: {
       Serial.print("Start");
       break;
      }
      case IR_BUTTON_3: {
       Serial.print("Alarm");
       break;
      }
      case IR_BUTTON_4: {
       Serial.print("Police");
       break;
      }
    }
    delay(400);
    IrReceiver.resume();
  }



  if (Serial.available() > 0) {
    incomingString = Serial.readString(); // read the incoming byte:
    if (strstr(incomingString.c_str(),  "unlock") != NULL) {
      lockState = false;
    } else if (strstr(incomingString.c_str(),  "lock")!= NULL) {
      lockState = true;
    }
    else if (strstr(incomingString.c_str(),  "POPO")!= NULL) {
      policeState = true;
  }
    else if (strstr(incomingString.c_str(),  "NOP")!= NULL) {
      policeState = false;
      setColor(255,0,255);
  }
  }
  if (policeState) {
    setColor(255,0,0);
    delay(200);
    setColor(0,0,255);
    delay(200);
  }
  

}

void setColor(int red, int green, int blue){
  digitalWrite(RED_PIN, red);
  digitalWrite(GREEN_PIN, green);
  digitalWrite(BLUE_PIN, blue);
}
