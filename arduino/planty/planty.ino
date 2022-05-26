#include <dht.h>
#include <EEPROM.h>
#include "Adafruit_VEML7700.h"
#include <Adafruit_NeoPixel.h>

Adafruit_VEML7700 veml = Adafruit_VEML7700();
//#define DHT11PIN 2 //Maybe needs to change
#define LED_COUNT 24
#define LED_PIN 4
#define LED_INPIN 7
#define WATER_INTERUPT 6
#define RESET_GO 5
#define RX_LED 5
#define RX 0

//PI control stuff
double setpoint = 0;
double error;
double totalError;
double lastError;
double sensedOutput;
double controlSignal;
double maxControl = 25500;
double minControl = 0;
double Kp = 0;
double Ki = 0;
int T = 200; //ms?
unsigned long lastTime;
bool runPI = false;


Adafruit_NeoPixel strip(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);
uint32_t purple = strip.Color(255, 100, 255);
uint32_t white = strip.Color(255, 255, 255);
uint32_t red = strip.Color(255, 0, 0);
uint32_t green = strip.Color(0, 255, 0);
uint32_t blue = strip.Color(0, 0, 255);
uint32_t purpleish = strip.Color(255, 100, 255);

//I/O
int motorTranPin = 3;
int moisSensorTranPin = A1;
int sensorPin = A2;
int tempSensorPin = A3;
int boardLed = 13;
//int buttonPin = 0; //switch interrupt
//int LEDin = 4;

int addr = 0;
float power = 0;
int duration = 0;
int samples = 0;

volatile byte state = LOW;
volatile char rec = 'o';
volatile char sen = 'o';

String ets = "";
char sep[3] = {'=', ',', '\n'};

//String plant = "Nothing yet :(";

boolean stringComplete = false;
boolean serialFlag = false;
boolean ALSready = false;

dht DHT;

void setup()
{
  strip.begin();
  strip.show(); //All pixels off
  Serial.begin(57600);
  pinMode(motorTranPin, OUTPUT);
  pinMode(moisSensorTranPin, OUTPUT); // A1
  pinMode(boardLed, OUTPUT);
  pinMode(RX_LED, OUTPUT);
  //pinMode(LEDin, OUTPUT);
  //digitalWrite(motorTranPin, LOW);  // turn off the motor
  analogWrite(motorTranPin, 0); //power off

  //pinMode(WATER_INTERUPT, INPUT_PULLUP);
  //pinMode(RESET_GO, INPUT_PULLDOWN);
  //attachInterrupt(digitalPinToInterrupt(WATER_INTERUPT), ButtonWater, LOW);
  //Serial.println("Welcome!");

  digitalWrite(RX_LED, LOW); 

}

void loop()
{

  String action = "";

  if (ALSready == false) {
    startALS();
  }

  if (runPI) PI_control();

  if (serialFlag == true && stringComplete == true)
  {

    if (checkCommand(ets))
    {

      String action = getAction(ets);

      if (ets.endsWith("\n"))
      {
        ets.remove(ets.length() - 1, 1);

      }

      if (action == "MOTR")
      {

        if (ets.substring(5, 6).toInt() == 1)
        {

          if (ets.substring(7).toFloat() < 101.00 && ets.substring(7).toFloat() > 0)
          {
            power = ets.substring(7, ets.indexOf(',', 7)).toFloat();

            duration = ets.substring(ets.indexOf(',', 7) + 1).toInt();

            analogWrite(motorTranPin, power * (255.00 / 100.00));
            digitalWrite(boardLed, HIGH);
            
            delay(duration);

            analogWrite(motorTranPin, 0);
            digitalWrite(boardLed, LOW);

            Serial.println(ets + ",OK");
          } else
          {
            Serial.println(ets + ",ERR");
          }

        }
        else if (ets.substring(5, 6).toInt() == 2)
        {

          Serial.println(action + "=" + power + ",OK");
        }
        else if (ets.substring(5, 6).toInt() == 0)
        {
          power = 0.00;

          analogWrite(motorTranPin, power);
          digitalWrite(boardLed, LOW);
          Serial.println(ets + ",OK");
        }
        else
        {
          Serial.println(ets + ",ERR");
        }

      }
      else if (action == "MOIS")
      {
        samples = ets.substring(ets.indexOf('=') + 1).toInt();

        if (samples > 0)
        {

          int moisInc = 0;

          for (int i = 1; i <= samples; i++) {

            moisInc += readMoistureSensor();
            delay(10);
          }

          float moisValue = moisInc / samples;

          if (moisValue == -1.0)
          {
            Serial.println(action + ",ERR");
          }
          else
          {
            Serial.println(action + "=" + moisValue + ",OK");
          }
        } else
        {
          Serial.println(ets + ",ERR");
        }


      }
      else if (action == "TEMP")
      {
        float tempHumValue = readHumTempSensor(ets.substring(5).toInt());

        if (tempHumValue == -1)
        {

          Serial.println(ets + ",ERR");
        }
        else
        {

          Serial.print(action + "=");
          Serial.print(tempHumValue);
          Serial.println(",OK");

        }
      }
      else if (action == "PLANT")
      {
        if (ets.indexOf('1') != -1)
        {
          //read plant info from eeprom
          String temp = read_String(0);
          Serial.println(action + "=" + temp + ",OK");

        } else if (ets.indexOf('2') != -1)
        {
          String plant = ets.substring(ets.indexOf(sep[1]) + 1);

          writeString(0, plant);
          delay(200);
          String temp = read_String(0);

          Serial.println(action + "=" + temp + ",OK");
        } else
        {

          Serial.println(ets + ",ERR");
        }
      } else if (action == "ALS")
      {
        uint16_t ALSval = 0;

        if (!ALSready) {
          Serial.println(action + ",ERR");
        } else {
          ALSval = veml.readALS();

          if (ALSval < 0)
          {
            ALSval = 65535;
          }

          Serial.println(action + "=" + ALSval + ",OK");
        }

      }
      else if (action == "LED")
      {
        int LEDparam = -1;
        LEDparam = ets.substring(ets.indexOf('=') + 1).toInt();

        if (LEDparam == 1) {

          String retcolor = "";
          int color = ets.substring(ets.indexOf(',') + 1).toInt();
          int bright = ets.substring(ets.indexOf('=') + 5).toInt();

          if (bright > 255) {
            bright = 255;
          }

          if (color == 0 || color == 1 || color == 2 || color == 3 || color == 4 || color == 5 || color == 99) {
            setLED(color, bright);

            switch (color) {
              case 0:
                retcolor = "off";
                break;
              case 1:
                retcolor = "purple";
                break;
              case 2:
                retcolor = "white";
                break;
              case 3:
                retcolor = "red";
                break;
              case 4:
                retcolor = "green";
                break;
              case 5:
                retcolor = "blue";
                break;
              case 99:
                retcolor = "mix";
                break;
              default:
                // statements
                break;
            }

            Serial.println(action + "=" + retcolor + ",OK");
          } else {
            Serial.println(action + "=" + retcolor + ",ERR");
          }
        }
        else if (LEDparam == 2) {
          //Not yet implemented :(
          uint32_t qcolor = strip.getPixelColor(0);

          union
          {
            struct
            {
              uint8_t byte1;
              uint8_t byte2;
              uint8_t byte3;
              uint8_t byte4;
            };
            uint32_t longint;
          } convert;
          
          convert.longint = qcolor;
          uint8_t bright = strip.getBrightness();
          Serial.println(action + "=" + LEDparam + "," + convert.byte3 + "," + convert.byte2 + "," + convert.byte1 + ",OK");
        }
        else {
          Serial.println(action + "=" + LEDparam + ",ERR");
        }

      }
      else if (action == "PISET") {
        if (ets.substring(ets.indexOf('=') + 1).toInt() == 1) {
          Serial.println(action + "=" + Kp + "," + Ki + "," + T + "," + maxControl + ",OK");
        
        } else if (ets.substring(ets.indexOf('=') + 1).toInt() == 2) {
          int oldindex = ets.indexOf(',');
          Kp = ets.substring(oldindex + 1, ets.indexOf(',', oldindex + 1)).toDouble();
          
          oldindex = ets.indexOf(',', oldindex + 1);
          Ki = ets.substring(oldindex + 1, ets.indexOf(',', oldindex + 1)).toDouble();
          oldindex = ets.indexOf(',', oldindex + 1);

          T = ets.substring(oldindex + 1, ets.indexOf(',', oldindex + 1)).toDouble();
          oldindex = ets.indexOf(',', oldindex + 1);

          maxControl = ets.substring(oldindex + 1, ets.indexOf(',', oldindex + 1)).toDouble();

          Serial.println(action + "=" + Kp + "," + Ki + "," + T + "," + maxControl + ",OK");
        }

      }
      else if (action == "PI") {
        int PIok = -1;

        if (ets.substring(ets.indexOf('=') + 1).toInt() == 1) {
          if (runPI) PIok = 1;
          else PIok = 0;

          Serial.println(action + "=" + PIok + ",OK");

        }

        else if (ets.substring(ets.indexOf('=') + 1).toInt() == 2) {
          if (ets.substring(ets.indexOf('=') + 3).toInt() == 0) runPI = false;
          else if (ets.substring(ets.indexOf('=') + 3).toInt() == 1) runPI = true;

          if (runPI) PIok = 1;
          else PIok = 0;

          if (!runPI) setLED(0, 0);
          else {
            setpoint = ets.substring(ets.indexOf('=') + 5).toDouble();
          }

          Serial.println(action + "=" + PIok + "," + setpoint + ",OK");
        }
      }
    }

    else
    {
      Serial.println(ets + ",ERR");
    }

    //Set flag to false
    Serial.flush();
    ets = "";
    serialFlag = false;
    stringComplete = false;
  }
}


void serialEvent() {
  //statements
  
  while (Serial.available()) {
    
    digitalWrite(RX_LED, HIGH); 
    
    // get the new byte:
    char rec = (char)Serial.read();
    // add it to the inputString:
    ets += rec;
    if (rec == '\n') {
      stringComplete = true;
    }
    serialFlag = true;

    digitalWrite(RX_LED, LOW); 
  }

}

boolean checkCommand(String in)
{
  //String action = in.substring(0, 4);

  String action = getAction(in);

  if (action == "MOTR" || action == "MOIS" || action == "TEMP" || action == "PLANT" || action == "ALS" || action == "LED" || action == "PI" || action == "PISET")
  {
    return true;
  }
  else
  {
    return false;
  }

}

int readMoistureSensor()
{
  int moisValue = -1;
  digitalWrite(moisSensorTranPin, HIGH); // moisSensorTranPin HIGH
  delay(200);
  moisValue = analogRead(sensorPin);
  digitalWrite(moisSensorTranPin, LOW); // moisSensorTranPin LOW
  delay(200);

  return moisValue;
}

float readHumTempSensor(int action)
{
  float humTempValue = -1;

  int chk = DHT.read11(tempSensorPin);

  if (action == 1) //If action=1 read temperature
  {
    humTempValue = DHT.temperature;
  }
  else if (action == 2) //if action=2 read humidity
  {
    humTempValue = DHT.humidity;
  }

  return humTempValue;

}

String getAction(String in)
{
  String action = "nope!";

  if (in.indexOf(sep[0]) != -1)
  {
    action = in.substring(0, in.indexOf(sep[0]));

  } else
  {
    action = in.substring(0, in.indexOf(sep[2]));

  }

  return action;

}

void writeString(char add, String data)
{
  int _size = data.length();
  int i;
  for (i = 0; i < _size; i++)
  {
    EEPROM.write(add + i, data[i]);
  }
  EEPROM.write(add + _size, '\0'); //Add termination null character for String Data
}

String read_String(char add)
{
  int i;
  char data[100]; //Max 100 Bytes
  int len = 0;
  unsigned char k;
  k = EEPROM.read(add);
  while (k != '\0' && len < 500) //Read until null character
  {
    k = EEPROM.read(add + len);
    data[len] = k;
    len++;
  }
  data[len] = '\0';
  return String(data);
}

boolean startALS() {

  if (veml.begin()) {
    ALSready = true;

    veml.setGain(VEML7700_GAIN_1_8);
    veml.setIntegrationTime(VEML7700_IT_800MS);
  } else {
    ALSready = false;
  }

}

void setLED(int color, int bright) {

  if (color == 1) {
    //digitalWrite(LED_PIN, HIGH);
    strip.fill(purple, 0);
    strip.setBrightness(bright);
    strip.setPixelColor(0, 255, 0, 255);
    strip.show();
  }
  if (color == 2) {
    //digitalWrite(LED_PIN, HIGH);
    strip.fill(white, 0);
    strip.setBrightness(bright);
    //strip.setPixelColor(0, 255, 0, 255);
    strip.show();
  }
  if (color == 3) {
    //digitalWrite(LED_PIN, HIGH);
    strip.fill(red, 0);
    strip.setBrightness(bright);
    //strip.setPixelColor(0, 255, 0, 255);
    strip.show();
  }
  if (color == 4) {
    //digitalWrite(LED_PIN, HIGH);
    strip.fill(green, 0);
    strip.setBrightness(bright);
    //strip.setPixelColor(0, 255, 0, 255);
    strip.show();
  }
  if (color == 5) {
    //digitalWrite(LED_PIN, HIGH);
    strip.fill(blue, 0);
    strip.setBrightness(bright);
    //strip.setPixelColor(0, 255, 0, 255);
    strip.show();
  }
  if (color == 99) {
    //digitalWrite(LED_PIN, HIGH);
    strip.fill(purpleish, 0);
    strip.setBrightness(bright);
    //strip.setPixelColor(0, 255, 128, 255);
    strip.show();
  }
  else if (color == 0) {
    //digitalWrite(LED_PIN, LOW);
    strip.clear();
    //strip.setPixelColor(0, 0, 0, 0);
    strip.show();
  }
}

void ButtonWater() {

  Serial.println("Water!");
  
  while (digitalRead(WATER_INTERUPT) == LOW) {
    analogWrite(motorTranPin, 255.0);
    digitalWrite(boardLed, HIGH);
  }

  delay(100);

  analogWrite(motorTranPin, 0.0);
  digitalWrite(boardLed, LOW);
}

void PI_control() {
  unsigned long currentTime = millis();
  int deltaTime = currentTime - lastTime;

  if (deltaTime >= T) {
    uint16_t ALS = veml.readALS();
    sensedOutput = (double) ALS;
    double error = setpoint - sensedOutput;

    totalError += error; //accumalates the error - integral term

    if (totalError >= maxControl) totalError = maxControl;
    else if (totalError <= minControl) totalError = minControl;

    controlSignal = Kp * error + (Ki * T * 0.001) * totalError;
    if (controlSignal > maxControl) controlSignal = maxControl;
    else if (controlSignal < minControl) controlSignal = minControl;

    int brightControl = (controlSignal / maxControl) * 255;

    setLED(99, brightControl);

    lastError = error;
    lastTime = currentTime;
  }
}
