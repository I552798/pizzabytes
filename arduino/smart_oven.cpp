#include "Display.h" 

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


/* Variables */
// Initialise initial temperature at 0
int currentTemp = 0;

// Timer variables
int countdownTime; // // Countdown start time 
unsigned long previousMillis = 0; // For timing the countdown
int interval = 1000;  // Interval of 1 second for countdown

// Potentiometer variables
int lastPotValue;


/* Clear display, initialise pin modes and start serial communication */
void setup() {
  Serial.begin(9600); // Start serial communication for debugging
  Display.clear(); // Clear display at startup
  pinMode(redLed, OUTPUT); // Set red redLed as output
  // Set button inputs with pull-up resistors
  pinMode(rightButton, INPUT_PULLUP);
  pinMode(leftButton, INPUT_PULLUP);
  // Set buzzer os output
  pinMode(buzzer, OUTPUT);
}


/* Function to adjust and display temperature based on button presses */
void temperature(){
  Display.show(currentTemp); // Display current temperature value
  // Increase temperature by 10 if the right button is pressed
  if(digitalRead(rightButton) == LOW && currentTemp < 400){
    currentTemp += 10;
    // Debugging
    Serial.print("Current temperature: ");
    Serial.println(currentTemp);
  }
  // Decrease temperature by 10 if the right button is pressed
  if(digitalRead(leftButton) == LOW && currentTemp > 0){
    currentTemp -= 10;
    // Debugging
    Serial.print("Current temperature: ");
    Serial.print(currentTemp);
    Serial.print("°C");
  }
  delay(200); // Delay for button debounce
}


/* Function to activate the buzzer */
void buzzer_noise(){
  tone(buzzer, 50); // Send 50Hz sound signal
  delay(500); // Wait for 1 sec
  noTone(buzzer); // Stop sound
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
    previousMillis = currentMillis;  // Update the previousMillis to current time
    countdownTime--; // Decrease the countdown time
    Display.show(format_time(countdownTime)); // Display the updated and formatted countdown time
    digitalWrite(redLed, HIGH); // Keep the red LED on while the timer is active
    // Debugging
    Serial.print("Time left: ");
    Serial.print(countdownTime / 60);
    Serial.print(" minutes and ");
    Serial.print(countdownTime % 60);
    Serial.println(" seconds");
  }
  // If the countdown has finished
  if (countdownTime == 0) {
    // Debugging
    Serial.println("Oven OFF");
    digitalWrite(redLed, LOW); // Turn of red LED
    digitalWrite(greenLed, HIGH); // Turn on green LED to indicate that the countdown has finished
    //buzzer_noise();
    delay(4000); // Wait 4 seconds before turning off the green LED 
    digitalWrite(greenLed, LOW); // Green LED off
    Display.clear(); // Clear the display once the countdown is done
  }
}


/* Main loop to read potentiometer, handle temperature adjustment, and start the timer */
void loop(){
  int potValue = analogRead(potMeter); // Read and save analog value from potentiometer
  potValue = map(potValue, 0, 1023, 0, 900); // Map potentiometer value from 0-1023 to 0-900 seconds (15 minutes)

  // If the potentiometer value is 0, allow temperature adjustments
  if(potValue == 0){
    temperature(); // Call temperature function to adjust and display temperature
  }
  else {
    countdownTime = potValue; // Set the countdown timer based on potentiometer value
    if (lastPotValue != potValue){
      lastPotValue = potValue;
      // Debugging
      Serial.print("Current timer value: ");
      Serial.print(countdownTime / 60);
      Serial.print(" minutes and ");
      Serial.print(countdownTime % 60);
      Serial.println(" seconds");
    }
    Display.show(format_time(countdownTime)); // Display the current countdown value in MM:SS format
    delay(200); // Short delay to avoid quick changes

    // If the left button is pressed, start the countdown timer
    if(digitalRead(leftButton) == LOW){
      // Debugging
      Serial.println("Oven ON");
      delay(300); // Delay for button debounce
      // Run the timer until countdown reaches 0
      while(countdownTime){
        timer(); // Call timer function to decrease and display countdown time

        // If the left button is pressed again, break the loop
        if(digitalRead(leftButton) == LOW){
          // Debugging
          Serial.println("Oven process terminated");
          digitalWrite(redLed, LOW);
          delay(300);
          break; // >:3
        }
      }
    }
  }
}
