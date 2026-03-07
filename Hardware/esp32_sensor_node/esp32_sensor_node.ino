#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>

// =============================================
// CHANGE THESE TO YOUR VALUES
// =============================================
const char* WIFI_SSID     = "OnePlus Nord2 5G";
const char* WIFI_PASSWORD = "helloworld2";

// Raspberry Pi's IP on your local network
// Find it by running: hostname -I   on the Pi
const char* RPI_ENDPOINT = "http://192.168.60.234:5002/api/sensor-data";

// =============================================
// SENSOR PINS — match your wiring
// =============================================
#define DHT_PIN      4       // DHT11 data pin → GPIO4
#define DHT_TYPE     DHT11
#define SOIL_PIN     34      // YL-69 analog out → GPIO34
#define LIGHT_PIN    35      // Grove Light analog → GPIO35

DHT dht(DHT_PIN, DHT_TYPE);

// Send data every 10 seconds
const unsigned long SEND_INTERVAL = 10000;
unsigned long lastSend = 0;

void setup() {
  Serial.begin(115200);
  dht.begin();

  // Connect to WiFi
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  Serial.println("Connected! IP: " + WiFi.localIP().toString());
}

void loop() {
  if (millis() - lastSend < SEND_INTERVAL) return;
  lastSend = millis();

  // ---- Read DHT11 (temperature + humidity) ----
  float temperature = dht.readTemperature();
  float humidity    = dht.readHumidity();

  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("ERROR: DHT11 read failed, skipping...");
    return;
  }

  // ---- Read YL-69 Soil Moisture ----
  // ESP32 ADC range: 0-4095
  // Dry soil = high value, Wet soil = low value
  int soilRaw = analogRead(SOIL_PIN);
  float soilMoisture = map(soilRaw, 4095, 0, 0, 100);
  soilMoisture = constrain(soilMoisture, 0, 100);

  // ---- Read Grove Light Sensor ----
  int lightRaw = analogRead(LIGHT_PIN);
  float solarOutput = map(lightRaw, 0, 4095, 0, 1000);

  // ---- Build JSON payload ----
  String json = "{";
  json += "\"temperature\":" + String(temperature, 1) + ",";
  json += "\"humidity\":"    + String(humidity, 1) + ",";
  json += "\"soil\":"        + String(soilMoisture, 1) + ",";
  json += "\"solar_output\":" + String(solarOutput, 0) + ",";
  json += "\"light_raw\":"   + String(lightRaw);
  json += "}";

  Serial.println("Sending: " + json);

  // ---- POST to Raspberry Pi ----
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(RPI_ENDPOINT);
    http.addHeader("Content-Type", "application/json");

    int code = http.POST(json);

    if (code > 0) {
      Serial.println("OK: " + String(code) + " " + http.getString());
    } else {
      Serial.println("FAIL: " + http.errorToString(code));
    }
    http.end();
  } else {
    Serial.println("WiFi lost! Reconnecting...");
    WiFi.reconnect();
  }
}