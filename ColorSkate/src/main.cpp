#include "FastLED.h"
#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>
#include <ESP8266mDNS.h>

void startWiFi();


// LED
#define NUM_LEDS 60
#define DATA_PIN 6
CRGB leds[NUM_LEDS];

// WIFI
ESP8266WiFiMulti wifiMulti;       // Create an instance of the ESP8266WiFiMulti class, called 'wifiMulti'

// HOTSPOT
const char *ssid = "colorskate"; // The name of the Wi-Fi network that will be created
const char *password = "kalkoen";   // The password required to connect to it, leave blank for an open network

// mDNS
const char* mdnsName = "esp8266"; // Domain name for the mDNS responder

void setup() {

  Serial.begin(115200);
  delay(10);
  Serial.println('\n');
  Serial.println("Setup started");
  Serial.println('\n');

  // LED
  Serial.println(F("    configuring led's"));
  FastLED.addLeds<NEOPIXEL, DATA_PIN>(leds, NUM_LEDS);
  Serial.println(F("    -- leds configured"));

  startWiFi();                 // Start a Wi-Fi access point, and try to connect to some given access points. Then wait for either an AP or STA connection

}

void loop() {
     for(int dot = 0; dot < NUM_LEDS; dot++) {
         leds[dot] = CRGB::Blue;
         FastLED.show();
         // clear this led for the next time around the loop
         leds[dot] = CRGB::Black;
         delay(30);
     }
 }


void startWiFi() { // Start a Wi-Fi access point, and try to connect to some given access points. Then wait for either an AP or STA connection
  WiFi.softAP(ssid, password);             // Start the access point
  Serial.print("Access Point \"");
  Serial.print(ssid);
  Serial.println("\" started\r\n");

  wifiMulti.addAP("Avenue Belle Vue", "Westfield19");   // add Wi-Fi networks you want to connect to

  Serial.println("Connecting");
  while (wifiMulti.run() != WL_CONNECTED && WiFi.softAPgetStationNum() < 1) {  // Wait for the Wi-Fi to connect
    delay(250);
    Serial.print('.');
  }
  Serial.println("\r\n");
  if(WiFi.softAPgetStationNum() == 0) {      // If the ESP is connected to an AP
    Serial.print("Connected to ");
    Serial.println(WiFi.SSID());             // Tell us what network we're connected to
    Serial.print("IP address:\t");
    Serial.print(WiFi.localIP());            // Send the IP address of the ESP8266 to the computer
  } else {                                   // If a station is connected to the ESP SoftAP
    Serial.print("Station connected to ESP8266 AP");
  }
  Serial.println("\r\n");
}
