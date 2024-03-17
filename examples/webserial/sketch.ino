const int BUTTON = 2;
const int LED = 3;

int buttonPressCount = 0;

void setup()
{
  pinMode(BUTTON, INPUT);
  pinMode(LED, OUTPUT);
  Serial.begin(115200);
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

  if (digitalRead(BUTTON) == HIGH) {
    buttonPressCount++;
    Serial.println(buttonPressCount);
    delay(50); // avoid bouncing
  }
}
