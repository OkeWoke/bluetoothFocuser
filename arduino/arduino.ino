// Bluetooth Motor Controller for Astrophotography Telescope.
// Version 2.1
// Author: Nico van Zyl
// 12.1.18

// HC-06 Bluetooth module connected to Arduino Nano on RX and TX pins.
// Motor will be driven with L293D dual H-brige motor driver.
// L293D connected to Nano on digital pins 3 and 5.
// Speed of the motor is controlled with Pulse Width Modulation of pins 3 or 5.

// inChar will store the incoming byte before processing.
char inChar;

// const chars are assigned as commands for talking between host pc and bluetooth device.
// must be set up EXACTLY the same on pc side.
const char Commands [] = {'A','B','C','D','Z','Y','X','W'};

// The duty cycle values are the full range of 0-255, incrementing in 25% steps.
const int pwmVals [] = {64,128,191,255};

// O will act as a handshake acknowledge.
const char ReceivedByte = 'O';

// H will be imediate stop.
const char HChar = 'H';


void setup() {
 Serial.begin(9600);

 pinMode(3,OUTPUT);
 pinMode(5,OUTPUT);
 pinMode(13,OUTPUT);
 // pin 13, which is also the onboard LED, will be used as a visual indicator.
}

void loop() {
 //For loop runs through the list of known commands, if it is known, associated PWM value is passed to appropriate direction function.
  if (inChar == 'H'){
    Halt();
  }
  else{
    for (int i =0; i < sizeof(Commands)-1;i++){
      if (inChar == Commands[i]){
        if (i<4){
          Clockwise(pwmVals[i]);
        }
        else if (i<7 && i>3){
          CounterClockwise(pwmVals[i-4]);
        }
      }
    }
  }
}

void Halt(){
  analogWrite(3,0);
  analogWrite(5,0);
  digitalWrite(13,LOW);
}

// analogWrite will output PWM signal.
// First parameter of analogWrite is the pin, seconds param is PWM duty cycle, 0-255 or 0-100%.
void Clockwise(int pwm){
  analogWrite(3,pwm);
  digitalWrite(5,LOW);
}

// Pins 3 and 5 change functions so that PWM signal applied to opposite poles of motor, allowing change of direction.
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
