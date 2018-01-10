char inChar;
const char Halt = 'H';

const char CW25 = 'A';
const char CW50 = 'B';
const char CW75 = 'C';
const char CW100 = 'D';

const char CCW25 = 'Z';
const char CCW50 = 'Y';
const char CCW75 = 'X';
const char CCW100 = 'W';

//const chars are assigned as the protocol set up between host pc and bluetooth device

void setup() {
 Serial.begin(9600);

 pinMode(3,OUTPUT);
 pinMode(5,OUTPUT);
 pinMode(13,OUTPUT);
 // pin 3 and 5 are the two pins that connect to the L293D
}

void loop() {
  //Serial.print(inChar);
  //Serial.print("\n");
  if (inChar == Halt){
    analogWrite(3,0);
    analogWrite(5,0);
    digitalWrite(13,LOW);
  }
  else{
    switch (inChar){
      case CW25:
        analogWrite(3,64);//first parameter of analogWrite is the pin, seconds param is pwm duty cycle, 0-255
        digitalWrite(5,LOW);
        break;
       case CW50:
        analogWrite(3,128);
        digitalWrite(5,LOW);
        //bluetoothReset();
        break;
       case CW75:
        analogWrite(3,191);
        digitalWrite(5,LOW);
        break;
       case CW100:
        analogWrite(3,255);
        digitalWrite(5,LOW);
        break;
       case CCW25:
        analogWrite(5,64);
        digitalWrite(3,LOW);
        break;
       case CCW50:
        analogWrite(5,128);
        digitalWrite(3,LOW);
        break;
       case CCW75:
        analogWrite(5,191);
        digitalWrite(3,LOW);
        break;
        case CCW100:
        analogWrite(5,255);
        digitalWrite(3,LOW);
        break;
    } 
  }
}

void serialEvent(){
  digitalWrite(13,HIGH);
  inChar = Serial.read();
  Serial.write("O");
}
