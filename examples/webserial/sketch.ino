#include <Adafruit_Arcada.h>

Adafruit_Arcada arcada;
String inData;

void timercallback(void) {
  Serial.println(arcada.readLightSensor());
}

void setup() {  
  Serial.begin(9600);
  arcada.arcadaBegin();
}

void loop() {
    while (Serial.available() > 0)
    {
        char recieved = Serial.read();
        inData += recieved; 

        // Process message when new line character is recieved
        if (recieved == '\n')
        {
            //Serial.print("Arduino Received: ");
            //Serial.println(inData);
            switch (inData[0]) {
              case 'f':
                arcada.timerCallback(inData.substring(1).toFloat(), timercallback);                
                break;

              case '1': //LED on
                for(int32_t i=0; i< arcada.pixels.numPixels(); i++) {
                  arcada.pixels.setPixelColor(i, arcada.pixels.Color(25, 25, 100));
                }
                arcada.pixels.show();
                break;

              case '0': //LED off
                for(int32_t i=0; i< arcada.pixels.numPixels(); i++) {
                  arcada.pixels.setPixelColor(i, arcada.pixels.Color(0, 0, 0));
                }
                arcada.pixels.show();
                break;
            }
            inData = ""; // Clear recieved buffer
        }
    }
}
