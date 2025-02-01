#include <WiFi.h>
#include <WiFiUdp.h>
#include <ArduinoOTA.h>
#include <I2S.h>

// Wi-Fi Configuration
const char* ssid = "Fioptics05090"; 
const char* password = "GLB44TUGXR"; 
const char* desiredIPPrefix = "192.168.";  

WiFiUDP udp;
const char* receiverIP = "192.168.200.40";  // Change this to your PC's IP
const int receiverPort = 5005;

#define SAMPLES 64 // Must be a power of two

void setupWiFi() {
    Serial.print("Connecting to Open WiFi Network...");
    WiFi.begin(ssid, password);

    int attempts = 0;
    while (WiFi.status() != WL_CONNECTED || !checkIPAddress()) {
        delay(500);
        Serial.print(".");
        attempts++;

        if (attempts > 60) {  // 30-second timeout
            Serial.println("\nWi-Fi connection failed. Restarting...");
            ESP.restart();
        }
    }

    Serial.println("\nConnected to WiFi!");
    Serial.print("ESP32 IP Address: ");
    Serial.println(WiFi.localIP());

    ArduinoOTA.setHostname("ESP32-Nano");
    ArduinoOTA.begin();
}

// Check if IP is in the correct range
bool checkIPAddress() {
    return WiFi.localIP().toString().startsWith(desiredIPPrefix);
}

void setup() {
    Serial.begin(115200);
    setupWiFi();

    if (!I2S.begin(I2S_PHILIPS_MODE, 16000, 32)) {
        Serial.println("Failed to initialize I2S!");
        while (1);
    }
}

void loop() {
  ArduinoOTA.handle();  
  int32_t raw_samples[SAMPLES];  // Store raw I2S 32-bit samples
  int16_t processed_samples[SAMPLES];  // Processed 16-bit samples
  // Read I2S samples
  for (int i = 0; i < SAMPLES; i++) {
    int32_t sample = 0;
      while ((sample == 0) || (sample == -1)) {
        sample = I2S.read();
      }
      raw_samples[i] = sample;
  }

  // Compute mean value for normalization
  float meanval = 0;
  for (int i = 0; i < SAMPLES; i++) {
      meanval += raw_samples[i];
  }
  meanval /= SAMPLES;

  // Normalize and convert to int16_t (reduce packet size)
  for (int i = 0; i < SAMPLES; i++) {
      processed_samples[i] = (int16_t)((raw_samples[i] - (int32_t)meanval) >> 14);
// Convert 18-bit signed
  }

  // Send processed samples over UDP
  udp.beginPacket(receiverIP, receiverPort);
  udp.write((uint8_t*)processed_samples, SAMPLES * sizeof(int16_t));  // Send as raw bytes
  udp.endPacket();
  delay(100);  // Adjust if needed for real-time streaming

  float maxsample, minsample;
  minsample = 100000;
  maxsample = -100000;
  for (int i=0; i<SAMPLES; i++) {
    minsample = min(minsample, (float)raw_samples[i]);
    maxsample = max(maxsample, (float)raw_samples[i]);
  }
  Serial.println(maxsample - minsample);
}
