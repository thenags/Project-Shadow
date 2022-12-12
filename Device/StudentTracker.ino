/**
 * Created by K. Suwatchai (Mobizt)
 *
 * Email: k_suwatchai@hotmail.com
 *
 * Github: https://github.com/mobizt/Firebase-ESP32
 *
 * Copyright (c) 2022 mobizt
 *
 */

// This example shows how to read and write database rules


#include <WiFi.h>
#include <FirebaseESP32.h>
#include "time.h"

// Provide the token generation process info.
#include <addons/TokenHelper.h>

// Provide the RTDB payload printing info and other helper functions.
#include <addons/RTDBHelper.h>

/* 1. Define the WiFi credentials */
#define WIFI_SSID "ADD USERNAME"
#define WIFI_PASSWORD "ADD PASSWORD"

// For the following credentials, see examples/Authentications/SignInAsUser/EmailPassword/EmailPassword.ino

/* 2. Define the API Key */
#define API_KEY ""

/* 3. Define the RTDB URL */
#define DATABASE_URL "" //<databaseName>.firebaseio.com or <databaseName>.<region>.firebasedatabase.app

/** 4. Define the Service Account credentials (required for token generation)
 *
 * This information can be taken from the service account JSON file.
 *
 * To download service account file, from the Firebase console, goto project settings,
 * select "Service accounts" tab and click at "Generate new private key" button
 */
#define FIREBASE_PROJECT_ID ""
#define FIREBASE_CLIENT_EMAIL ""
const char PRIVATE_KEY[] PROGMEM = "";
#define USER_EMAIL "AUTHENTICATED EMAIL HERE"
#define USER_PASSWORD "AUTHENTICATED PASSWORD HERE"
// Define Firebase Data object
FirebaseData fbdo;

FirebaseAuth auth;
FirebaseConfig config;
const char* ntpServer = "pool.ntp.org";
bool taskCompleted = false;
unsigned long sendDataPrevMillis = 0;
String studentID = "PUT STUDENT ID HERE";
unsigned long count = 0;

void setup()
{

  Serial.begin(115200);
  Serial.println();
  Serial.println();
  
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to Wi-Fi");
  Serial.println();
  Serial.print("Connected with IP: ");
  Serial.println(WiFi.localIP());
  Serial.println();

  Serial.printf("Firebase Client v%s\n\n", FIREBASE_CLIENT_VERSION);

 /* Assign the api key (required) */
  config.api_key = API_KEY;

  /* Assign the user sign in credentials */
  auth.user.email = USER_EMAIL;
  auth.user.password = USER_PASSWORD;

  /* Assign the RTDB URL (required) */
  config.database_url = DATABASE_URL;

  /* Assign the callback function for the long running token generation task */
  config.token_status_callback = tokenStatusCallback; // see addons/TokenHelper.h

  // Or use legacy authenticate method
  // config.database_url = DATABASE_URL;
  // config.signer.tokens.legacy_token = "<database secret>";

  // To connect without auth in Test Mode, see Authentications/TestMode/TestMode.ino

  //////////////////////////////////////////////////////////////////////////////////////////////
  // Please make sure the device free Heap is not lower than 80 k for ESP32 and 10 k for ESP8266,
  // otherwise the SSL connection will fail.
  //////////////////////////////////////////////////////////////////////////////////////////////

  Firebase.begin(&config, &auth);

  // Comment or pass false value when WiFi reconnection will control by your code or third party library
  Firebase.reconnectWiFi(true);

  Firebase.setDoubleDigits(5);
  configTime(0, 0, ntpServer);
Serial.println("FINISHED SETUP");
}
// Fill the dots one after the other with a color

void loop()
{
  delay(100);

  // Firebase.ready() should be called repeatedly to handle authentication tasks.

  if (Firebase.ready() && (millis() - sendDataPrevMillis > 15000 || sendDataPrevMillis == 0))
  {
    int epochTime = int(getTime());
    Serial.println(epochTime);
    sendDataPrevMillis = millis();
    // For the usage of FirebaseJson, see examples/FirebaseJson/BasicUsage/Create_Edit_Parse.ino
    FirebaseJson bssids;
    FirebaseJson rssis;
    FirebaseJsonData result; // object that keeps the deserializing result
   // rssis.toString(Serial, true); // serialize contents to serial
   //  bssids.toString(Serial, true); // serialize contents to serial
   // Serial.printf("Clearing BSSID... %s\n", Firebase.updateNode(fbdo, F("/students/224289/wapBSSIDS"), 0) ? "ok" : fbdo.errorReason().c_str());
     //  Serial.printf("Clearing RSSI... %s\n", Firebase.updateNode(fbdo, F("/students/224289/wapRSSIS"), 0) ? "ok" : fbdo.errorReason().c_str());
     
    int n = WiFi.scanNetworks();
    if (n == 0)
    {
      Serial.println("No networks found");
    }
    else
    {
      String bssidwrite = "/students/" + studentID + "/wapBSSIDS";
      String rssiwrite = "/students/" + studentID + "/wapRSSIS";
      String positionwrite = "/students/" + studentID + "/position/3";
      int j = 0;
      
      for (int i = 0; i < n; ++i) {
        //WiFi.SSID(i) == "Positioner"
        if(WiFi.SSID(i) == "Positioner"){
           bssids.add(String(j),WiFi.BSSIDstr(i));
           rssis.add(String(j),WiFi.RSSI(i));
          Serial.print(WiFi.BSSIDstr(i));
          Serial.print(" (");
          Serial.print(WiFi.RSSI(i));
          Serial.println(")");
          j++;
        }
      }
      Serial.printf("Set json... %s\n", Firebase.set(fbdo, bssidwrite, bssids) ? "ok" : fbdo.errorReason().c_str());
      Serial.printf("Set json... %s\n", Firebase.set(fbdo, rssiwrite, rssis) ? "ok" : fbdo.errorReason().c_str());
      Serial.printf("Set json... %s\n", Firebase.setInt(fbdo, positionwrite, epochTime) ? "ok" : fbdo.errorReason().c_str());
       
    }
    Serial.println();
  }
}
// Function that gets current epoch time
unsigned long getTime() {
  time_t now;
  struct tm timeinfo;
  if (!getLocalTime(&timeinfo)) {
    //Serial.println("Failed to obtain time");
    return(0);
  }
  time(&now);
  return now;
}
