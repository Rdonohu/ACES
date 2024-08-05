#include <Wire.h>
#include <MPU6050.h>
#include <IRremote.h>
#define IR_RECEIVE_PIN 3

#define IR_BUTTON_1 16
#define IR_BUTTON_2 17
#define IR_BUTTON_3 18


MPU6050 mpu;

const float thresh = 1.1;

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


  //Send message if acceleration is greater than threshold
  if(abs(axG) > thresh || abs(ayG) > thresh || abs(azG) > thresh){
    Serial.println("Bump Detected!");
  }
  if (IrReceiver.decode()) {
    IrReceiver.resume();
    int command = IrReceiver.decodedIRData.command;
    switch (command){

      case IR_BUTTON_1: {
       Serial.println(1);
       break;
      }
      case IR_BUTTON_2: {
       Serial.println(2);
       break;
      }
      case IR_BUTTON_3: {
       Serial.println(3);
       break;
      }
    }
  }
  delay(50);

}
