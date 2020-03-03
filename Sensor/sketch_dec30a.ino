#define BLYNK_DEBUG
#define BLYNK_PRINT Serial
#include <ESP8266WiFi.h>
#include <BlynkSimpleEsp8266.h>
#include <SoftwareSerial.h>
#include <SimpleTimer.h>
#define myPeriodic 15 //in sec | Thingspeak pub is 15sec
WidgetLCD lcd(V5);
const char* server = "api.thingspeak.com";
String apiKey ="YOUR_THINGSPEAK_API_KEY";
const char* MY_SSID = "YOUR_WIFI_NAME"; 
const char* MY_PWD = "YOUR_WIFI_PASSWORD";
int sent = 0;

char auth[] = "YOUR_BLYNK_AUTH_TOKEN";
 
// Your WiFi credentials.
// Set password to "" for open networks.
char ssid[] = "YOUR_WIFI_NAME";
char pass[] = "YOUR_WIFI_PASSWORD";
 
SimpleTimer timer;
 
String myString; // complete message from arduino, which consists of snesors data
char rdata; // received characters
 
String firstVal, secondVal,thirdVal; // sensors 
// This function sends Arduino's up time every second to Virtual Pin (1).
// In the app, Widget's reading frequency should be set to PUSH. This means
// that you define how often to send data to Blynk App.
void myTimerEvent()
{
  // You can send any value at any time.
  // Please don't send more that 10 values per second.
  Blynk.virtualWrite(V1, millis() / 1000);
  
}
 
 
void setup()
{
  // Debug console
  Serial.begin(9600);
  // Edited code: Priyank
  Serial.println("HEy there.");
  for(int i=0;i<=5;i++){
    Serial.print("HEy there.");
    delay(1000);
  }
  Blynk.begin(auth, ssid, pass);
  timer.setInterval(1000L,sensorvalue1); 
  connectWifi();
}
 
void loop()
{
  
   if (Serial.available() == 0 ) 
   {
  Blynk.run();
  timer.run(); // Initiates BlynkTimer
   }
   
  if (Serial.available() > 0 ) 
  {
    rdata = Serial.read(); 
    myString = myString+ rdata; 
   // Serial.print(rdata);
    if( rdata == '\n')
    {
 
String l = getValue(myString, ',', 0);
String m = getValue(myString, ',', 1);
String n = getValue(myString, ',', 2);
 
 
 
firstVal = l;
secondVal = m;
thirdVal = n;
 
  myString = "";
// end new code
    }
  }
  sendTeperatureTS(firstVal);
}
 
void sensorvalue1()
{
 
  // You can send any value at any time.
  // Please don't send more that 10 values per second.
  Blynk.virtualWrite(V3, firstVal);
  Blynk.virtualWrite(V4, secondVal);
 
 
      lcd.clear();
    lcd.print(0,0,"BPM:");
    lcd.print(11,0,thirdVal);
     lcd.print(0,1,"Patient Monitor");
 
}
 
 
String getValue(String data, char separator, int index)
{
    int found = 0;
    int strIndex[] = { 0, -1 };
    int maxIndex = data.length() - 1;
 
    for (int i = 0; i <= maxIndex && found <= index; i++) {
        if (data.charAt(i) == separator || i == maxIndex) {
            found++;
            strIndex[0] = strIndex[1] + 1;
            strIndex[1] = (i == maxIndex) ? i+1 : i;
        }
    }
    return found > index ? data.substring(strIndex[0],strIndex[1]):   "";
}

void connectWifi()
{
  Serial.print("Connecting to "+*MY_SSID);
  WiFi.begin(MY_SSID, MY_PWD);
  while (WiFi.status() != WL_CONNECTED) {
  delay(1000);
  Serial.print(".");
  }
  
  Serial.println("");
  Serial.println("Connected");
  Serial.println("");  
}//end connect

void sendTeperatureTS(String firstVal)
{  
   WiFiClient client;
  
   if (client.connect(server, 80)) { // use ip 184.106.153.149 or api.thingspeak.com
   Serial.println("WiFi Client connected ");
   
   String postStr = apiKey;
   postStr += "&field1=";
   postStr += String(firstVal);
   postStr += "\r\n\r\n";
   
   client.print("POST /update HTTP/1.1\n");
   client.print("Host: api.thingspeak.com\n");
   client.print("Connection: close\n");
   client.print("X-THINGSPEAKAPIKEY: " + apiKey + "\n");
   client.print("Content-Type: application/x-www-form-urlencoded\n");
   client.print("Content-Length: ");
   client.print(postStr.length());
   client.print("\n\n");
   client.print(postStr);
   delay(1000);
   
   }//end if
   sent++;
 client.stop();
}//end send
