#include <Arduino_APDS9960.h>

void setup() {
  if (!APDS.begin()) {
    Serial.println("Could not detect gesture sensor");
  }
}

void loop() {
   if (APDS.gestureAvailable()) {
    int gesture = APDS.readGesture();

    switch (gesture) {
      case GESTURE_UP:
        Serial.println("Up");
        break;

      case GESTURE_DOWN:
        Serial.println("Down");
        break;

      case GESTURE_LEFT:
        Serial.println("Left");
        break;

      case GESTURE_RIGHT:
        Serial.println("Right");
        break;

      default:
        break;
    }

}
