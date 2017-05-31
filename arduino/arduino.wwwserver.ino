#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <DHT.h>
#include <SparkFunTSL2561.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_TSL2561_U.h>

Adafruit_TSL2561_Unified tsl = Adafruit_TSL2561_Unified(TSL2561_ADDR_FLOAT, 12345);

#define DHTTYPE DHT11
#define DHTPIN  2
 
const char* ssid     = "Guest";
const char* password = "test";
 
ESP8266WebServer server(80);
 
// Initialize DHT sensor 
DHT dht(DHTPIN, DHTTYPE, 11); // 11 works fine for ESP8266


//Global Variables
float humidity, temp_c;  // Values read from sensor
String webString="";     // String to display
unsigned long previousMillis = 0;        // will store last temp was read
const long interval = 2000;              // interval at which to read sensor
boolean gain;     // Gain setting, 0 = X1, 1 = X16;
unsigned int ms;  // Integration ("shutter") time in milliseconds
double lux;    // Resulting lux value
boolean good;  // True if neither sensor is saturated
    
// Create an SFE_TSL2561 object, here called "light":

SFE_TSL2561 light;

void configureSensor(void)
{
  tsl.enableAutoRange(true); 
  tsl.setIntegrationTime(TSL2561_INTEGRATIONTIME_13MS);
}

void gettemperature() {
  // Wait at least 2 seconds seconds between measurements.
  // if the difference between the current time and last time you read
  // the sensor is bigger than the interval you set, read the sensor
  // Works better than delay for things happening elsewhere also
  unsigned long currentMillis = millis();
 
  if(currentMillis - previousMillis >= interval) {
    // save the last time you read the sensor 
    previousMillis = currentMillis;   
 
    // Reading temperature for humidity takes about 250 milliseconds!
    // Sensor readings may also be up to 2 seconds 'old' (it's a very slow sensor)
    humidity = dht.readHumidity();          // Read humidity (percent)
    temp_c = dht.readTemperature();     // Read temperature as Fahrenheit
    // Check if any reads failed and exit early (to try again).
    if (isnan(humidity) || isnan(temp_c)) {
      Serial.println("Failed to read from DHT sensor!");
      return;
    }
  }
}

void getlight() {
  // Wait between measurements before retrieving the result
  // (You can also configure the sensor to issue an interrupt
  // when measurements are complete)
  
  // This sketch uses the TSL2561's built-in integration timer.
  // You can also perform your own manual integration timing
  // by setting "time" to 3 (manual) in setTiming(),
  // then performing a manualStart() and a manualStop() as in the below
  // commented statements:
  
  // ms = 1000;
  // light.manualStart();
  delay(ms);
  // light.manualStop();
  
  // Once integration is complete, we'll retrieve the data.
  
  // There are two light sensors on the device, one for visible light
  // and one for infrared. Both sensors are needed for lux calculations.
  
  // Retrieve the data from the device:

  unsigned int data0, data1;
  
  if (light.getData(data0,data1))
  {
    // getData() returned true, communication was successful
    
    Serial.print("data0: ");
    Serial.print(data0);
    Serial.print(" data1: ");
    Serial.print(data1);
  
    // To calculate lux, pass all your settings and readings
    // to the getLux() function.
    
    // The getLux() function will return 1 if the calculation
    // was successful, or 0 if one or both of the sensors was
    // saturated (too much light). If this happens, you can
    // reduce the integration time and/or gain.
    // For more information see the hookup guide at: https://learn.sparkfun.com/tutorials/getting-started-with-the-tsl2561-luminosity-sensor
  
    
    
    // Perform lux calculation:

    good = light.getLux(gain,ms,data0,data1,lux);
    
    // Print out the results:
  
    Serial.print(" lux: ");
    Serial.print(lux);
    if (good) Serial.println(" (good)"); else Serial.println(" (BAD)");

  }
  else
  {
    // getData() returned false because of an I2C error, inform the user.

    byte error = light.getError();
    printError(error);
  }
}

void printError(byte error)
  // If there's an I2C error, this function will
  // print out an explanation.
{
  Serial.print("I2C error: ");
  Serial.print(error,DEC);
  Serial.print(", ");
  
  switch(error)
  {
    case 0:
      Serial.println("success");
      break;
    case 1:
      Serial.println("data too long for transmit buffer");
      break;
    case 2:
      Serial.println("received NACK on address (disconnected?)");
      break;
    case 3:
      Serial.println("received NACK on data");
      break;
    case 4:
      Serial.println("other error");
      break;
    default:
      Serial.println("unknown error");
  }
}


void handle_root() {
  server.send(200, "text/plain", "Hello from the weather esp8266, read from /temp or /humidity");
  delay(100);
}
 
void setup(void)
{
  // You can open the Arduino IDE Serial Monitor window to see what the code is doing
  Serial.begin(115200);  // Serial connection from ESP-01 via 3.3v console cable
  dht.begin();           // initialize temperature sensor
  
  // Connect to WiFi network
  WiFi.begin(ssid, password);
  Serial.print("\n\r \n\rWorking to connect");
 
  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("Temp/Humidity/Light");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  if(!tsl.begin())
  {
    /* There was a problem detecting the ADXL345 ... check your connections */
    Serial.print("Ooops, no TSL2561 detected ... Check your wiring or I2C ADDR!");
    while(1);
  }
   
  server.on("/", handle_root);
  
  server.on("/temp", [](){  // if you add this subdirectory to your webserver call, you get text below :)
    gettemperature();       // read sensor
    getlight();
          /* Get a new sensor event */ 
      sensors_event_t event;
      tsl.getEvent(&event);
 
  /* Display the results (light is measured in lux) */
  if (event.light)
  {
    Serial.print(event.light); Serial.println(" lux");
    lux = event.light;
  }
  else
  {
    /* If event.light = 0 lux the sensor is probably saturated
       and no reliable data could be generated! */
    Serial.println("Sensor overload");
  }
  delay(250);
    webString="<html><head><title>Toronto Mesh</title><style>body { background-color: #cccccc; font-family: Arial,\
    Helvetica, Sans-Serif; Color: #000088; }</style><meta http-equiv='Refresh' content='5'>\
    </head><body><h3>ESP8266 WebServer + WiFi.softAPIP</h3>\<h3>Temperature & Humidity</h3><br><table width=160 border=0 cellpadding=0 cellspacing=0><tr> <td>\
    <!-- this table is for the verbal display of info -->  <table width='100%' border=0 cellpadding=0 cellspacing=0>\ 
    <tr><td align='center'><small>Temp:" +String((int)temp_c)+" C</small></td></tr><tr><td align='center'>\
    <!-- this table is for the visual display of info, set black box width here --><table width='500' border=0 cellpadding=0 cellspacing=2\
    bgcolor='black'><tr><td bgcolor='gray' align='left'><!-- this table is for the blue box, image is for Netscape and opera bug  -->\
    <table width=" +String((int)(temp_c*2))+"%' border=0 cellpadding=0 cellspacing=0 bgcolor=#66ff33><tr><td><img src='/images/dot_clear.gif' \
    width=1 height=13 alt='' border=0></td></tr></table><!-- close blue box table --></td></tr></table><!-- close blue box table --></td> \
    </tr> </table></td></tr></table>\
    <br><table width=160 border=0 cellpadding=0 cellspacing=0><tr> <td>\
    <!-- this table is for the verbal display of info -->  <table width='100%' border=0 cellpadding=0 cellspacing=0>\ 
    <tr><td align='center'><small>Humidity:" +String((int)humidity)+" %</small></td></tr><tr><td align='center'>\
    <!-- this table is for the visual display of info, set black box width here --><table width='500' border=0 cellpadding=0 cellspacing=2\
    bgcolor='black'><tr><td bgcolor='gray' align='left'><!-- this table is for the blue box, image is for Netscape and opera bug  -->\
    <table width=" +String((int)(humidity))+"%' border=0 cellpadding=0 cellspacing=0 bgcolor=#66ff33><tr><td><img src='/images/dot_clear.gif' \
    width=1 height=13 alt='' border=0></td></tr></table><!-- close blue box table --></td></tr></table><!-- close blue box table --></td> \
    </tr> </table></td></tr></table>\
    <br><table width=160 border=0 cellpadding=0 cellspacing=0><tr> <td>\
    <!-- this table is for the verbal display of info -->  <table width='100%' border=0 cellpadding=0 cellspacing=0>\ 
    <tr><td align='center'><small>Lux:" +String((int)lux)+"</small></td></tr><tr><td align='center'>\
    <!-- this table is for the visual display of info, set black box width here --><table width='500' border=0 cellpadding=0 cellspacing=2\
    bgcolor='black'><tr><td bgcolor='gray' align='left'><!-- this table is for the blue box, image is for Netscape and opera bug  -->\
    <table width=" +String((int)(lux/1000))+"%' border=0 cellpadding=0 cellspacing=0 bgcolor=#66ff33><tr><td><img src='/images/dot_clear.gif' \
    width=1 height=13 alt='' border=0></td></tr></table><!-- close blue box table --></td></tr></table><!-- close blue box table --></td> \
    </tr> </table></td></tr></table>";  
    server.send(200, "text/html", webString);            


    
  });
 
  server.on("/humidity", [](){  // if you add this subdirectory to your webserver call, you get text below :)
    gettemperature();           // read sensor
    webString="Humidity: "+String((int)humidity)+"%";
    server.send(200, "text/plain", webString);               // send to someones browser when asked
  });
  
  server.begin();
  Serial.println("HTTP server started");
}
 
void loop(void)
{ 
  server.handleClient();
} 

