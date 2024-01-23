/*********
  Parts from: Rui Santos
              Complete project details at https://randomnerdtutorials.com  
  

*********/

#include <WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>
#include "FreqCountESP.h"
#include <string.h>
#include "tab\arduino_secrets.h"
#include "settings\commands.h"

// Replace the next variables with your SSID/Password combination
const char* ssid = SECRET_SSID;
const char* password = SECRET_PASS;

// Add your MQTT Broker IP address, example:
//const char* mqtt_server = "192.168.1.144";
const char* mqtt_server = MQTT_IP_ADDR;

// MQTT Topics
char topic_sensor[64] = "sensor/";
char topic_susbcribed[64] = "sensor/";
//TODO: Add UUID as MAC address?
// Identification
char UUID[9] = "1";

// WiFi init
WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;

// Delay time for next automatic send in ms
long delayAutoSend = 50000;

// Status LED 
const int ledPin = 4;
const int moistureSensorOnOff = 5;

// Frequency input
int inputPin = 14;
int timerMs = 1000; // Sample time

void setup() {
  Serial.begin(115200);

  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);

  FreqCountESP.begin(inputPin, timerMs);

  pinMode(ledPin, OUTPUT);
  pinMode(moistureSensorOnOff, OUTPUT);
  digitalWrite(ledPin, HIGH);

  strcat(topic_sensor, UUID);
  strcat(topic_sensor, "/");
  strcat(topic_susbcribed, UUID);
  strcat(topic_susbcribed, "/#");
}

void sendHumidityFrequency(){
  digitalWrite(moistureSensorOnOff, HIGH);
  Serial.println("Turning moisture sensor on and measure");
  delay(2300);
  uint32_t frequency = FreqCountESP.read();
  digitalWrite(moistureSensorOnOff, LOW);
  
  char payload[32] = { 0 };
  sprintf(payload, "%d", frequency);
  Serial.print("Sending frequency payload: ");
  Serial.println(payload);

  char data_topic[64] = { 0 };
  sprintf(data_topic, "%sdata/hum", topic_sensor);
  Serial.print("Sending on topic: ");
  Serial.println(data_topic);

  client.publish(data_topic, payload);
}

void sendFailMessage(const char* msg){
  char errString[32];
  sprintf(errString, "error:%s", msg);
  Serial.println(errString);
  client.publish(topic_sensor, errString);
}

void setup_wifi() {
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* message, unsigned int length) {
  Serial.print("Message arrived on topic: ");
  Serial.print(topic);
  Serial.print(". Message: ");
  String messageTemp;
  char msgBuffer[64] = { 0 };
  // I keep message temp here for longer messages then expected
  for (int i = 0; i < length; i++) {
    Serial.print((char)message[i]);
    messageTemp += (char)message[i];
    if (i < 64){
      msgBuffer[i] = (char)message[i];
    }
  }
  Serial.println();

  // Feel free to add more if statements to control more GPIOs with MQTT
  char cmd_topic[64] = { 0 };
  sprintf(cmd_topic, "%scmd", topic_sensor);
  Serial.print("cmd topic is: ");
  Serial.println(cmd_topic);
  
  if (!strcmp(topic, cmd_topic)) {
    Serial.print("Strcmp was good. Message: ");
    Serial.println(msgBuffer);
    if(!strcmp(msgBuffer, GET_HUMIDITY_DATA)){
      uint8_t maxErrCnt = 20;
      uint8_t errCnt;
      for(errCnt = 0; errCnt < maxErrCnt; errCnt ++){
        if (FreqCountESP.available()){
          sendHumidityFrequency();
          blinkLED();
          break;
        }else{
          errCnt += 1;
          Serial.print("Reading failed. Waiting 2 seconds before retry. Already tried: ");
          Serial.println(errCnt);
          delay(2000);
        }
      }
      if(errCnt == maxErrCnt){
        sendFailMessage("Reading failed!");
      }
    }
  }
}



void blinkLED(){
  digitalWrite(ledPin, HIGH);
  delay(300);
  digitalWrite(ledPin, LOW);
  delay(300);
  digitalWrite(ledPin, HIGH);
  delay(300);
  digitalWrite(ledPin, LOW);
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect("ESP8266Client")) {
      Serial.println("connected");
      // Subscribe
      client.subscribe(topic_susbcribed);
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  long now = millis();
  if (now - lastMsg > delayAutoSend) {
    lastMsg = now;
    if (FreqCountESP.available())
    {
      sendHumidityFrequency();
    }else{
      Serial.println("No frq availaible.");
    }
  }
}