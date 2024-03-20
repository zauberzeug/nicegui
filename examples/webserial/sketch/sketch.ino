const int BUTTON = 12;
const int LED = 13;

int lastButtonState = HIGH;

void setup()
{
  pinMode(BUTTON, INPUT_PULLUP);
  pinMode(LED, OUTPUT);
  Serial.begin(115200);
}

void loop() {
  if (Serial.available() > 0) {
    switch (Serial.read()) {
      case '1':
        digitalWrite(LED, HIGH);
        break;
      case '0':
        digitalWrite(LED, LOW);
        break;
    }
  }

  int buttonState = digitalRead(BUTTON);
  if (lastButtonState != buttonState) {
    Serial.println(buttonState == LOW ? "LOW" : "HIGH");
    delay(50); // avoid bouncing
  }
  lastButtonState = digitalRead(BUTTON);
}
