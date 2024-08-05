#include <Wire.h>
#include <MPU6050.h>
#include <IRremote.h>

#define IR_RECEIVE_PIN 3
#define IR_BUTTON_1 16
#define IR_BUTTON_2 17
#define IR_BUTTON_3 18


MPU6050 mpu;

const float thresh = 1.1;
String incomingString;
bool lockState = false;

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
    IrReceiver.resume();
    int command = IrReceiver.decodedIRData.command;
    switch (command){

      case IR_BUTTON_1: {
       Serial.print(1);
       break;
      }
      case IR_BUTTON_2: {
       Serial.print(2);
       break;
      }
      case IR_BUTTON_3: {
       Serial.print(3);
       break;
      }
    }
  }



  if (Serial.available() > 0) {
    incomingString = Serial.readString(); // read the incoming byte:
    if (strstr(incomingString.c_str(),  "unlock") != NULL) {
      lockState = false;
    } else if (strstr(incomingString.c_str(),  "lock")!= NULL) {
      lockState = true;
      Serial.print(lockState);
    }
  }
   



  delay(50);

}
