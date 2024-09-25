#include <SPI.h>
#include <WiFiNINA.h>
#include <ArduinoJson.h>

// Update with your network credentials
char ssid[] = "your_wifi_ssid";
char pass[] = "your_wifi_password";

// API endpoint
char server[] = "your-api-endpoint.amazonaws.com";

// Device ID
const char* deviceId = "arduino-uno-001";

WiFiClient client;

void setup() {
  Serial.begin(9600);
  while (!Serial);

  // Connect to WiFi network
  Serial.print("Connecting to ");
  Serial.println(ssid);
  if (WiFi.begin(ssid, pass) != WL_CONNECTED) {
    Serial.println("Failed to connect to WiFi");
    while (true);
  }
  Serial.println("Connected to WiFi");
}

void loop() {
  // TODO: Implement actual sensor readings
  float temperature = 25.0; // Placeholder value
  float humidity = 50.0;    // Placeholder value

  // Construct JSON payload
  StaticJsonDocument<200> jsonDoc;
  jsonDoc["device_id"] = deviceId;
  jsonDoc["timestamp"] = "2023-10-15T14:30:00Z"; // Replace with actual timestamp
  jsonDoc["temperature"] = temperature;
  jsonDoc["humidity"] = humidity;

  char payload[256];
  serializeJson(jsonDoc, payload);

  // Send HTTP POST request
  if (client.connectSSL(server, 443)) {
    client.println("POST /dev/sensor-data HTTP/1.1");
    client.print("Host: ");
    client.println(server);
    client.println("Content-Type: application/json");
    client.print("Content-Length: ");
    client.println(strlen(payload));
    client.println();
    client.println(payload);

    // Read response
    while (client.connected()) {
      String line = client.readStringUntil('\n');
      if (line == "\r") {
        break;
      }
    }
    client.stop();
    Serial.println("Data sent successfully");
  } else {
    Serial.println("Connection failed");
  }

  delay(5000); // Send data every 5 seconds
}