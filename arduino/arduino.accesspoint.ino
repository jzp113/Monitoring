#include <ESP8266WiFi.h>
#include <WiFiClient.h> 
#include <ESP8266WebServer.h>
#include <DHT.h> 

#define DHTPIN 2     // what digital pin we're connected to

// Uncomment whatever type you're using!
#define DHTTYPE DHT11   // DHT 11
//#define DHTTYPE DHT22   // DHT 22  (AM2302), AM2321
//#define DHTTYPE DHT21   // DHT 21 (AM2301)

// Initialize DHT sensor.
DHT dht(DHTPIN, DHTTYPE);

float humidity, temp_c, temp_f, heatindex;
String webString="";     // String to display
// Generally, you should use "unsigned long" for variables that hold time
unsigned long previousMillis = 0;        // will store last temp was read
const long interval = 2000;              // interval at which to read sensor

/* Set these to your desired credentials. */
const char *ssid = "ESPap";
const char *password = "thereisnospoon";

ESP8266WebServer server(80);

/* Just a little test message.  Go to http://192.168.4.1 in a web browser
 * connected to this access point to see it.
 */
void handleRoot() {
int size=1000;
char temp[size];
int sec = millis() / 1000;
int min = sec / 60;
int hr = min / 60;

server.send(200, "text/plain", ("yyyyyyyyyyyyyyyyyy"));
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

void setup() {
  delay(1000);
  Serial.begin(115200);
  Serial.println("DHTxx test!");
  dht.begin();
  Serial.print("Configuring access point...");
  /* You can remove the password parameter if you want the AP to be open. */
  WiFi.softAP(ssid, password);

  IPAddress myIP = WiFi.softAPIP();
  Serial.print("AP IP address: ");
  Serial.println(myIP);
  server.on("/", handleRoot);
  
  server.on("/temp", [](){  // if you add this subdirectory to your webserver call, you get text below :)
    gettemperature();       // read sensor
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
    </tr> </table></td></tr></table>";
    server.send(200, "text/html", webString);            // send to someones browser when asked
  });
  server.begin();
  Serial.println("HTTP server started");
}

void loop() {
  server.handleClient();
}
