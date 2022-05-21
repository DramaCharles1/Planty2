#define BAUDRATE 57600

boolean stringComplete = false;
boolean serialFlag = false;
String ets = "";
char sep[3] = {'=', ',', '\n'};

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
        Serial.println(action + ",OK");
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
