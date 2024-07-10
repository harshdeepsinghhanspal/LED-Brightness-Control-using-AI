int ledPin = 11;  // PWM pin to which the LED is connected

void setup() {
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
}

void loop() {
  if (Serial.available()) {
    int brightness = Serial.read();
    analogWrite(ledPin, brightness);
  }
}
