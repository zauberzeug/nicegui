const int BUTTON = 2;
const int LED = 3;

// Variables will change:
int buttonState = 0;        // current state of the button
int lastButtonState = 0;    // previous state of the button

void  setup()
{
  pinMode(BUTTON, INPUT);
  pinMode(LED, OUTPUT);
  Serial.begin(9600);
}


void loop() {

  if (Serial.available() > 0) {
    char received = Serial.read();
    switch (received) {
      case '1':
        digitalWrite(LED, HIGH);
        break;
      case '0':
        digitalWrite(LED, LOW);
        break;
    }
  }

  // read the pushbutton input pin
  buttonState = digitalRead(BUTTON);

  // compare the buttonState to its previous state
  if (buttonState != lastButtonState) {
    // if the state has changed, increment the counter
    if (buttonState == HIGH) {
      // if the current state is HIGH then the button went from off to on
      Serial.println("1");
    } else {
      // if the current state is LOW then the button went from on to off
      // Serial.println("off");
    }
    // Delay a little bit to avoid bouncing
    delay(50);
  }
  // save the current state as the last state, for next time through the loop
  lastButtonState = buttonState;
}




