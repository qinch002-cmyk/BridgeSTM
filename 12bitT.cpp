#include "Particle.h"

const int CS = D10;   // 你的 CS 针脚
const int SCK = S3;   
const int SDI = S2;

void writeDAC(uint16_t value) {
    if (value > 4095) value = 4095;
    uint16_t cmd = 0x3000 | (value & 0x0FFF);
    digitalWrite(CS, LOW);
    SPI.transfer16(cmd);
    digitalWrite(CS, HIGH);
}

void setup() {
    pinMode(CS, OUTPUT);
    digitalWrite(CS, HIGH);

    SPI.begin();
    SPI.setDataMode(SPI_MODE0);
    SPI.setClockSpeed(1000000);
}

void loop() {
    writeDAC(0);    // 0V
    delay(1000);

    writeDAC(1024); // ~1V
    delay(1000);

    writeDAC(2048); // ~2V
    delay(1000);

    writeDAC(3072); // ~3V
    delay(1000);

    writeDAC(4095); // ~4.096V
    delay(1000);
}

