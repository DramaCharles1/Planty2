#define BAUDRATE 57600
#define MOIS_SENSOR_CONTROL 2

//serial communication
boolean stringComplete = false;
boolean serialFlag = false;
String ets = "";
char sep[3] = {'=', ',', '\n'};

//moisture sensor
int samples = 0; 

//analog pins
int mois_sensor_read = A0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(BAUDRATE);
  pinMode(MOIS_SENSOR_CONTROL, OUTPUT); //D2
}

void loop() 
{
  if (serialFlag == true && stringComplete == true)
  {
    if (checkCommand(ets))
    {
      String action = getAction(ets);
      if(action == "MOIS")
      {
        samples = ets.substring(ets.indexOf('=') + 1).toInt();
        if (samples > 0)
        {
          int moisInc = 0;
          for (int i = 1; i <= samples; i++)
          {
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
      else if(action == "TEST")
      {
        int on = ets.substring(ets.indexOf('=') + 1).toInt();
        if(on == 1)
        {
          digitalWrite(MOIS_SENSOR_CONTROL, HIGH); // moisSensorTranPin HIGH
          Serial.println(action + "=" + on + ",OK");
        }
        else if (on == 0)
        {
          digitalWrite(MOIS_SENSOR_CONTROL, LOW); // moisSensorTranPin HIGH
          Serial.println(action + "=" + on + ",OK");
        }
        else
        {
          Serial.println(action + "=" + on + ",ERR");
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
  if (action == "MOIS" || action == "TEST")
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
  digitalWrite(MOIS_SENSOR_CONTROL, HIGH); // moisSensorTranPin HIGH
  delay(200);
  moisValue = analogRead(mois_sensor_read);
  digitalWrite(MOIS_SENSOR_CONTROL, LOW); // moisSensorTranPin LOW
  delay(200);

  return moisValue;
}
