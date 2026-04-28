#include <Wire.h>

// Defines the data variable, the frequency of which values are collected
int Temp_data;

int frequency = 1000;

// Defines a list of temperatures to gauge where the reading temperature is

static const float tempF[] = {
   -40,  -20,    0,   20,   40,   60,   70,   80,   90,   100,  120,  140,  160,  180,  200,  220,  240
};

// Defines a list of resistances. Used to gauge where the thermistors resistance lies
static const float resOhms[] = {
    613,  676,  744,  818,  895,  978, 1035, 1095, 1158, 1223, 1359, 1507, 1668, 1841, 2025, 2221, 2428
};

const int nPts = sizeof(tempF) / sizeof(tempF[0]);

const float Rfixed = 988.0;

float readTemp(int pin)
{
    // Read ADC
    int adc = analogRead(pin);
    float Vadc = adc * (5.0 / 1023.0);

    // Compute thermistor resistance (thermistor on top)
    float Rt = Rfixed * (Vadc / (5.0 - Vadc));

    // Find where Rt sits between table entries
    int i;
    for (i = 0; i < nPts - 1; i++) {
        if (Rt >= resOhms[i] && Rt <= resOhms[i + 1])
            break;
    }

    // If out of range, return nearest endpoint
    if (i == nPts - 1)
        return tempF[nPts - 1];
    if (Rt < resOhms[0])
        return tempF[0];

    // Linear interpolation:
    float R1 = resOhms[i];
    float R2 = resOhms[i + 1];
    float T1 = tempF[i];
    float T2 = tempF[i + 1];

    float fraction = (Rt - R1) / (R2 - R1);
    return T1 + fraction * (T2 - T1);
}

void setup() {

  Serial.begin(9600); // 9600 baud, if the sensor requires a differen baudrate change this value

  while (!Serial) { // A delay to allow for proper setup
      delay(1);
  }
}

// Continuous data reading
void loop() {
  
    // Reads the pin where the sensor is wired in at
    // Currently using analog pin 0, but can change to whatever analog pin is being used
    Temp_data = readTemp(A0);

    // Prints the data to a serial monitor, used to output the data to the python file
    Serial.println(Temp_data);

    delay(frequency);
}
