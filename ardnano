/*
 * SDI-12 program for H-3611 WaterLog
 * 
 * Distance value = sensor to surface of water
 * Slope is set at -1.0
 * Stage = (-1.0 x Distance) + Offset
 * Offset should be the distance from Sensor to the ground
 * level. (e.g 2.000 metres)
 * 
 */
 
#include <SDISerial.h>
#define DATA_PIN 2
SDISerial connection(DATA_PIN);

String inst;
int rd = 0;

void setup(){
      connection.begin();
      Serial.begin(9600);//so we can print to standard uart
      delay(3000);
    
      String Sensor = connection.sdi_query("?I!",1000);
//      Serial.print("Sensor: ");
//      Serial.println(Sensor);
      
      String SlopeWrite = connection.sdi_query("0XWS-1.0!",1000);
      delay (1000);
      String Slope = connection.sdi_query("0D0!", 1000);
//      Serial.print("Slope: ");
//      Serial.println(Slope);
      
      String OffsetWrite = connection.sdi_query("0XWO10.0!",1000);
      delay (1000);
      String Offset = connection.sdi_query("0D0!", 1000);
//      Serial.print("Offset: ");
//      Serial.println(Offset);
      delay (1000);
}

void loop(){
  int commaPosition;
  String D[5] = {}; // address & 4 data readings
  if (Serial.available() > 0) {
    inst = Serial.readString(); // read the incoming byte:
//    Serial.println(inst);
    if (inst=="R"){
      rd=1;
//      Serial.println("Read detected");   
    }
  }
  else{
//    Serial.println("Waiting on loop");
    delay(1000);
  }
   if (rd==1){
    rd=0;
    //measurement commmand
    String dataM = connection.sdi_query("?M!",1000);//1 second timeout
//    Serial.print("dataM: ");
//    Serial.println(dataM);
    delay (4000);
            
    String dataD0 = connection.sdi_query("0D0!", 1000);
//    Serial.print("dataD0original: ");
//    Serial.println (dataD0);    
    dataD0.replace("+", ",");
    dataD0.replace("-", ",-");
//    Serial.print ("dataD0adjusted: ");
//    Serial.println(dataD0);

    for(int i =0; i<5; i++)
    {
      commaPosition = dataD0.indexOf(',');
      if (commaPosition !=-1)
      {
        D[i] = {dataD0.substring(0, commaPosition)};
        D[i].trim();
        dataD0 = dataD0.substring(commaPosition +1, dataD0.length());
      }

      else
      {
        if(dataD0.length()>0)
        {
          D[i] = {dataD0};
          D[i].trim();
        }
      }
    }
    String seri = String(D[1]+","+D[2]+","+D[3]+","+D[4]);
    Serial.println(seri);
//    Serial.print("Stage: ");
//    Serial.println(D[1]);
//    
//    Serial.print("Distance: ");
//    Serial.println(D[2]);
//
//    Serial.print("Status: "); // 0 = success
//    Serial.println(D[3]);
//    
//    Serial.print("Battery: ");
//    Serial.println(D[4]);
//    
//    Serial.println();
   } 

 }
