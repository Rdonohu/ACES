#include <Wire.h>
#include <MPU6050.h>

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

  delay(50);

}
