void setup() {
  pinMode(A0, INPUT);
  Serial.begin(9600);
  pinMode(2, OUTPUT);
}

void loop() {
  int sensorValue = analogRead(A0);
  int heartRate = map(sensorValue, 0, 1023, 0, 140);
  digitalWrite(2,LOW);
  Serial.print("HR:");
  Serial.println(heartRate);

  delay(1000);

  if (Serial.available() > 0) {
    String request = Serial.readStringUntil('\n');
    if (heartRate < 65 || heartRate > 135){
      digitalWrite(2, HIGH);
      delay(2000);
      digitalWrite(2, LOW);
    } 
  }
}
