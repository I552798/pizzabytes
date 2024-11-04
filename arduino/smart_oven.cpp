#include "Display.h" 
#include "DHT11.h"

/* Initialisations */
// Potentiometer 
const int potMeter = A0; 

// Buttons 
const int rightButton = 8;
const int leftButton = 9;

//  LEDs 
const int redLed = 4;
const int greenLed = 5;

// Buzzer
const int buzzer = 3;

// Light sensor
int lightSensor = A2;


/* Variables */
int currentTemp = 0;

// Timer variables
int countdownTime = 0; 
unsigned long previousMillis = 0;
int interval = 1000; 
int countdownStart;
bool timerActive;

// Potentiometer variables
int lastPotValue = 0;
const int potThreshold = 10;


/* Clear display, initialise pin modes and start serial communication */
void setup() {
  Serial.begin(9600); 
  Display.clear(); 
  pinMode(redLed, OUTPUT); 
  pinMode(rightButton, INPUT_PULLUP);
  pinMode(leftButton, INPUT_PULLUP);
  pinMode(buzzer, OUTPUT);
  pinMode(lightSensor, INPUT);
}


/* Function to adjust and display temperature based on button presses */
void temperature(){
  Display.show(currentTemp);
  // Increase temperature by 10 if the right button is pressed, max temperature = 400
  if(digitalRead(rightButton) == LOW && currentTemp < 400){
    currentTemp += 10;
  }
  // Decrease temperature by 10 if the right button is pressed
  if(digitalRead(leftButton) == LOW && currentTemp > 0){
    currentTemp -= 10;
  }
  delay(200); // Delay for button debounce
}


/* Function to activate the buzzer */
void buzzer_noise(){
  tone(buzzer, 50);
  delay(500);
  noTone(buzzer);
}


/* Function to format the parameter value as MM:SS (Minutes and Seconds) and show it on the display */
int format_time (int value){
  int minutes = value / 60;
  int seconds = value % 60;
  return minutes * 100 + seconds;
}


/* Function to manage the countdown timer */
void timer() {
  unsigned long currentMillis = millis();
  // Check if 1 second has passed since the last update and the countdown is still running
  if (currentMillis - previousMillis >= interval && countdownTime > 0) {
    previousMillis = currentMillis; 
    countdownTime--; 
    Display.show(format_time(countdownTime)); 
    digitalWrite(redLed, HIGH);
  }
  if (countdownTime == 0) {
    Serial.println("Ready");
    digitalWrite(redLed, LOW); 
    digitalWrite(greenLed, HIGH); 
    //buzzer_noise();
    delay(2000); 
    digitalWrite(greenLed, LOW);
    timerActive = false;
    countdownTime = countdownStart;
    Display.show(countdownStart);
  }
}


/* Function to read multiple values and return their average to reduce noise */
int smoothPotValue() {
    int smoothedValue = 0;
    for (int i = 0; i < 10; i++) {
        smoothedValue += analogRead(potMeter);
    }
    return smoothedValue / 10; // Average of the readings
}


/* Main loop to read potentiometer, handle temperature adjustment, and start the timer */
void loop(){
  int potValue = smoothPotValue(); 
  potValue = map(potValue, 0, 1023, 0, 1800); // Map potentiometer value from 0-1023 to 0-1800 seconds (30 minutes)
  if(potValue == 0){
    temperature();
    countdownTime = 0;
  }
  else {
    // Check if the potentiometer reading has changed by the specified threshold
    if(abs(potValue - lastPotValue) > potThreshold){
      if(potValue > lastPotValue && countdownTime < 1800){  
        countdownTime += 10;
      } 
      else if(potValue < lastPotValue && countdownTime > 0){  
        countdownTime -= 10;  
      }
      Display.show(format_time(countdownTime));
      lastPotValue = potValue;
      countdownStart = countdownTime;
    }

    // If the left button is pressed, start the countdown timer
    if(digitalRead(leftButton) == LOW){
      timerActive = true;
      delay(300); // Delay for button debounce
      while(countdownTime && timerActive){
        timer();
        float brightness = analogRead(lightSensor);
        // If the left button is pressed again, break the loop
        if(digitalRead(leftButton) == LOW /*|| brightness > 800*/){
          // Debugging
          Serial.println("Process terminated");
          digitalWrite(redLed, LOW);
          countdownTime = countdownStart;
          Display.show(format_time(countdownStart));
          delay(300);
          break; // >:3
        }
      }
    }
  }
}
