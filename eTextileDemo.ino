const int rectifiedVoltagePin = A6;

const int analogOutPin = 9;

uint32_t rectifiedVoltage = 0;
int outputValue = 0;
float digitalVoltage = 0;
int i = 0;
uint32_t sum = 0, average = 0;
uint32_t stepCount = 0;
  
void setup() {
  // initialize serial communications at 9600 bps:
  Serial.begin(9600);
}

void loop() {
  // read the rectified voltage:
  rectifiedVoltage = analogRead(rectifiedVoltagePin);

  digitalVoltage = 0.005 * rectifiedVoltage;

  for(; i < 4; i++) {
    sum += rectifiedVoltage;
    if(i == 3)
    {
      average = sum / 4;
      i = 0;
      sum = 0;
      if (average > 95)
      {
        stepCount++;
      }
      break;
    }
  }


  // print the results to the Serial Monitor:
  //Serial.print("Rectified voltage = ");
  Serial.print(digitalVoltage);
  // Serial.print(", Step count = ");
  Serial.print(" ");
  Serial.println(stepCount);
  /*Serial.print(", Voltage = ");
  Serial.println(digitalVoltage);
  Serial.print("i = ");
  Serial.print(i);
  Serial.print(", sum = ");
  Serial.print(sum);*/

delay(1000);
}
