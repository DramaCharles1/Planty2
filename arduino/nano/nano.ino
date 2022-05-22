#define BAUDRATE 57600

//pins
int mois_sensor_control = D2;
int mois_sensor_read = A1;

//serial communication
boolean stringComplete = false;
boolean serialFlag = false;
String ets = "";
char sep[3] = {'=', ',', '\n'};

//moisture sensore
int samples = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(BAUDRATE);
}

void loop() 
{
  if (serialFlag == true && stringComplete == true)
  {
    if (checkCommand(ets))
    {
      String action = getAction(ets);

      if (action == "MOTR")
      {
        Serial.println(action + ",OK");
      }
      else if(action == "MOIS")
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
        }
        else
        {
          Serial.println(ets + ",ERR");
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

//Functions
void serialEvent() {
  //statements
  while (Serial.available()) {
    // get the new byte:
    char rec = (char)Serial.read();
    // add it to the inputString:
    ets += rec;
    if (rec == '\n') {
      stringComplete = true;
    }
    serialFlag = true;
  }
}

boolean checkCommand(String in)
{
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

int readMoistureSensor()
{
  int moisValue = -1;
  digitalWrite(mois_sensor_control, HIGH); // moisSensorTranPin HIGH
  delay(200);
  moisValue = analogRead(mois_sensor_read);
  digitalWrite(mois_sensor_control, LOW); // moisSensorTranPin LOW
  delay(200);

  return moisValue;
}
