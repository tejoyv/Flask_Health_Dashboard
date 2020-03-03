#define USE_ARDUINO_INTERRUPTS true    // Set-up low-level interrupts for most acurate BPM math.
#include <PulseSensorPlayground.h>     // Includes the PulseSensorPlayground Library.   
#include <OneWire.h>
#include <DallasTemperature.h>
#include <SoftwareSerial.h>
#include <stdlib.h>
SoftwareSerial nodemcu(2,3);
SoftwareSerial blue(7,8); // bluetooth module connected here

//  Variables
const int PulseWire = 0;       // PulseSensor PURPLE WIRE connected to ANALOG PIN 0
const int LED13 = 13;          // The on-board Arduino LED, close to PIN 13.
int Threshold = 550;           // Determine which Signal to "count as a beat" and which to ignore.
                               // Use the "Gettting Started Project" to fine-tune Threshold Value beyond default setting.
                               // Otherwise leave the default "550" value. 
                               
PulseSensorPlayground pulseSensor;  // Creates an instance of the PulseSensorPlayground object called "pulseSensor"


// for ds18b20 temperature sensor

#define ONE_WIRE_BUS 4 
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);
 float Celcius=0;
 float Fahrenheit=0;

String cdata; // complete data, consisting of sensors values
int sdata1 = 0; // temperature centigrade
int sdata2 = 0; // temperature Farenheit

char buff[10];
String tempc; 
String tempf;

void setup() {   

  Serial.begin(9600);          // For Serial Monitor
  nodemcu.begin(9600);
  blue.begin(9600); 
  // set up the LCD's number of columns and rows: 
  // Configure the PulseSensor object, by assigning our variables to it. 
  pulseSensor.analogInput(PulseWire);   
  pulseSensor.blinkOnPulse(LED13);       //auto-magically blink Arduino's LED with heartbeat.
  pulseSensor.setThreshold(Threshold);   

  // Double-check the "pulseSensor" object was created and "began" seeing a signal. 
   if (pulseSensor.begin()) {
    Serial.println("We created a pulseSensor Object !");  //This prints one time at Arduino power-up,  or on Arduino reset.  

  }
}



void loop() {

 int myBPM = pulseSensor.getBeatsPerMinute();  // Calls function on our pulseSensor object that returns BPM as an "int".
                                               // "myBPM" hold this BPM value now. 

if (pulseSensor.sawStartOfBeat()) {            // Constantly test to see if "a beat happened". 
Serial.println(myBPM); 
}
delay(20);
  sensors.requestTemperatures(); 
  Celcius=sensors.getTempCByIndex(0);
  Fahrenheit=sensors.toFahrenheit(Celcius);

//TEMPERATURE SENSOR DS18B20

 tempc = dtostrf(Celcius, 3, 2, buff);
  tempf = dtostrf(Fahrenheit, 3, 2, buff);

   cdata = cdata + tempc+","+tempf +","+myBPM; // comma will be used a delimeter
   Serial.println(cdata); 
   nodemcu.println(cdata);
   blue.println("Patient Monitoring."); 
   blue.println(cdata);
delay(20);
   cdata = "";

   
}
