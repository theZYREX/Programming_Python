const int PIN_LED = 13;

void runSnakePattern(int base_delay) {
  int delays[] = {base_delay / 4, base_delay / 2, base_delay, base_delay / 2};
  
  for (int i = 0; i < 4; i++) {
    digitalWrite(PIN_LED, HIGH);
    delay(delays[i]);
    digitalWrite(PIN_LED, LOW);
    delay(100);
  }
}

void handleCommand(String cmd) {
  cmd.trim();

  if (cmd == "LED_ON") {
    digitalWrite(PIN_LED, HIGH);
    Serial.println("OK");

  } else if (cmd == "LED_OFF") {
    digitalWrite(PIN_LED, LOW);
    Serial.println("OK");

  } else if (cmd == "STATUS") {
    Serial.println(digitalRead(PIN_LED) == HIGH ? "STATUS:ON" : "STATUS:OFF");

  } else if (cmd.startsWith("BLINK ")) {
    String params = cmd.substring(6);
    int spaceIdx = params.indexOf(' ');

    if (spaceIdx == -1) {
      Serial.println("ERROR:INVALID_PARAM");
      return;
    }

    int on_ms  = params.substring(0, spaceIdx).toInt();
    int off_ms = params.substring(spaceIdx + 1).toInt();

    if (on_ms <= 0 || off_ms < 0) {
      Serial.println("ERROR:INVALID_PARAM");
      return;
    }

    digitalWrite(PIN_LED, HIGH);
    delay(on_ms);
    digitalWrite(PIN_LED, LOW);
    if (off_ms > 0) delay(off_ms);
    Serial.println("OK");

  } else if (cmd.startsWith("SNAKE ")) {
    String param = cmd.substring(6);
    int base_delay = param.toInt();

    if (base_delay <= 0) {
      Serial.println("ERROR:INVALID_PARAM");
      return;
    }
    
    runSnakePattern(base_delay);
    Serial.println("OK");

  } else {
    Serial.println("ERROR:UNKNOWN_CMD");
  }
}

void setup() {
  pinMode(PIN_LED, OUTPUT); 
  Serial.begin(9600);       
  Serial.println("READY");
}

void loop() {
 
  if (Serial.available()) {
    
    String cmd = Serial.readStringUntil('\n');
    handleCommand(cmd); 
  }
}
