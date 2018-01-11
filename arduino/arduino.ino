// Bluetooth Motor Controller for Astrophotography Telescope.
// Version 2.0
// Author: Nico van Zyl
// 11.1.18

// HC-06 Bluetooth module connected to Arduino Nano on RX and TX pins.
// Motor will be driven with L293D dual H-brige motor driver.
// L293D connected to Nano on digital pins 3 and 5.


// inChar will store the incoming byte before processing.
// H will be imediately stop
char inChar;

const char Commands [] = {'A','B','C','D','Z','Y','X','W','H'};
const int pwmVals [] = {64,128,191,255};
const char ReceivedByte = 'O';
// const chars are assigned as commands for talking between host pc and bluetooth device.
// MUST be set up exactly the same on pc side.

/*
const char Halt = 'H';

// Four chars used for one direction, clockwise.
const char CW25 = 'A';
const char CW50 = 'B';
const char CW75 = 'C';
const char CW100 = 'D';

// Another four used for counter-clockwise.
const char CCW25 = 'Z';
const char CCW50 = 'Y';
const char CCW75 = 'X';
const char CCW100 = 'W';
*/




void setup() {
 Serial.begin(9600);

 pinMode(3,OUTPUT);
 pinMode(5,OUTPUT);
 pinMode(13,OUTPUT);
 // pin 13, which is also the onboard LED, will be used as a visual indicator.
}

void loop() {
 //For loop runs through the list of known commands, if it is known, associated PWM value is passed to appropriate direction function.
  for (int i =0; i < sizeof(Commands)-1;i++){
    if (inChar == Commands[i]){
      if (Commands[i]=='H'){
        Halt();
      }
      else if (i<4){
        Clockwise(pwmVals[i]);
      }
      else if (i<8 && i>3){
        CounterClockwise(pwmVals[i-4]);
      }
    }
  }
  //Serial.print(inChar);
  //Serial.print("\n");
  // ^ used for serial debugging, although interfered with pc side since this would also write to the Bluetooth module.
/*
  // Stop condition first to prevent and startup jitter.

  if (inChar == Halt){
    //
    analogWrite(3,0);
    analogWrite(5,0);
    digitalWrite(13,LOW);
  }
  else{
    switch (inChar){
     
      // analogWrite will output PWM
      // First parameter of analogWrite is the pin, seconds param is PWM duty cycle, 0-255 or 0%-100%
      // The duty cycle values are the full range, incrementing in 25% steps.
      case CW25:
        analogWrite(3,64);
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
      // Pins 3 and 5 change functions so that PWM signal applied to opposite poles of motor, allowing change of direction.
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
*/
}

void Halt(){
  analogWrite(3,0);
  analogWrite(5,0);
  digitalWrite(13,LOW);
}

void Clockwise(int pwm){
  analogWrite(3,pwm);
  digitalWrite(5,LOW);
}

void CounterClockwise (int pwm){
  analogWrite(5,pwm);
  digitalWrite(3,LOW);
}

// serialEvent is an interupt which is called when the recieve buffer gets a byte.
void serialEvent(){
  digitalWrite(13,HIGH);
  inChar = Serial.read();
  Serial.write(ReceivedByte);
  // Handshake with pc to confirm that the byte was successfully recieved and read.
}
