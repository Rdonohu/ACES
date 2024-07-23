// C++ code
//

int ledPin = 8;
int superPin = 4;
int buzzPin = 11;
int buttPin = 2;
int goodPin = 6;
String secMessage = "";
void setup()
{
  Serial.begin(9600);
  Serial.println("Bazinga");
  pinMode(ledPin, OUTPUT);
  pinMode(buzzPin, OUTPUT);
  pinMode(superPin, OUTPUT);
  pinMode(goodPin, INPUT_PULLUP);
  pinMode(buttPin, INPUT_PULLUP);
}

void loop()
{
  if(digitalRead(buttPin) == 0){
    //Serial.println("Yeah");
  	digitalWrite(buzzPin, HIGH);
    tone(superPin, 1000, 400);
    unlock(true);
  }else if(digitalRead(goodPin) == 0){
  	digitalWrite(ledPin, HIGH);
  	unlock(false);
  }else{
  	digitalWrite(ledPin, LOW);
    digitalWrite(buzzPin, LOW);
  }
}

void unlock(bool crime){
  if(crime){
   //Serial.println("You broke into the car! *you die*");
    changeSecMessage("You broke into the car! *you die*");
  }else{
   //Serial.println("Welcome to your Jaguar Vehicle..!");
   changeSecMessage("Welcome to your Jaguar Vehicle..!");
  }
}

void changeSecMessage(String s){
  if(secMessage != s){
    secMessage = s;
    Serial.println(secMessage);
  }
}