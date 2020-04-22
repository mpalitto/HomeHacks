/*
NodeMCU used as current draw monitor
A0 is the analog input
on board LED blinking to show it is not dead
Connect to WIFI network
and it sends to local server by socket
*/

#include <ESP8266WiFi.h>
//#include <PubSubClient.h>
#define LED_BUILTIN 2

// Update these with values suitable for your network.
const char* ssid = "PALITTO-BONCRISTIANO";
const char* password = "scalaEapt11";
const char* host = "192.168.1.77";  // Server IP
const int   port = 12345;           // Server Port
WiFiClient espClient;
long lastMsg = 0;
// String msg;
char msg[75];
int value = 0;
int current = 0;
int led = 0;
int maxx = 0;
String receiverName = "nodeMCU-currentSensor-1: ";
const int analogInPin = A0;  // ESP8266 Analog Pin ADC0 = A0
int sensorValue = 0;  // value read from the pot
int maxValue = 0; //maxsensorvalue


void setup_wifi() {
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);
  int led=0;
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
    if (led == 0) {
      digitalWrite(LED_BUILTIN, HIGH);   // Turn the LED on (Note that LOW is the voltage level
      led = 1;
    } else {
      digitalWrite(LED_BUILTIN, LOW);   // Turn the LED on (Note that LOW is the voltage level
      led = 0;
    }
  digitalWrite(LED_BUILTIN, HIGH);   // Turn the LED on (Note that LOW is the voltage level
  }

  randomSeed(micros());

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

//---------------------
void setSocket() {

    Serial.println("Setting UP SOCKET connection");   

    if (WiFi.status()!= WL_CONNECTED){   //Check WiFi connection status
      setup_wifi();
      delay(1000);
      Serial.println("WiFi connection SUCCESSFUL");   
    }
    
    if (espClient.connect(host, port)) {
      Serial.println(receiverName + " socket connection" + " to " + host + ":" + port + " was Successfull!");
    } else {
      Serial.println("connection failed");
      return;    
    } 
}
//---------------------

void setup() {
  pinMode(BUILTIN_LED, OUTPUT);     // Initialize the BUILTIN_LED pin as an output
  Serial.begin(115200);
  setSocket();
}

void loop() {


  long now = millis();
  // read the analog in value
  sensorValue = analogRead(analogInPin);
  //Serial.print(now - lastMsg);
  //Serial.print(" : ");
  //Serial.println(sensorValue);
  if (maxValue < sensorValue) { maxValue = sensorValue; }

  if (now - lastMsg > 2000) {
    lastMsg = now;

    //Verify connection is still in place, if not reconnect
    if (!espClient.connected()) {
      espClient.stop();
      setSocket();   
    }

    //sensorValue = analogRead(analogInPin);
    //++value;
    snprintf (msg, 75, "%ld", maxValue);
    Serial.print("Sent message: ");
    Serial.println(msg);
    espClient.print(receiverName + msg);
    maxValue = 0;
  }
  delay(10);
}
//---------------------
