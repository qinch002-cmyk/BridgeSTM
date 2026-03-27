// ====== MCP4821 DAC TEST CODE FOR PHOTON 2 ======

#define PIN_CS   D10     // 片选 CS#
#define PIN_SCK  S3      // SPI Clock
#define PIN_SDI  S2      // SPI MOSI

void setup() {
    pinMode(PIN_CS, OUTPUT);
    digitalWrite(PIN_CS, HIGH);

    SPI.begin();  
}

void loop() {
    testVoltage(0);        // 0V
    delay(1000);
    testVoltage(1024);     // ~1V
    delay(1000);
    testVoltage(2048);     // ~2V
    delay(1000);
    testVoltage(3072);     // ~3V
    delay(1000);
    testVoltage(4095);     // ~4V（满量程）
    delay(1000);
}

void testVoltage(uint16_t val) {
    // MCP4821 格式：12-bit data + control bits
    uint16_t cmd = 0;
    cmd |= (0b0011 << 12);   // GA=1 (x2 gain), SHDN=1
    cmd |= (val & 0x0FFF);

    digitalWrite(PIN_CS, LOW);
    SPI.transfer16(cmd);
    digitalWrite(PIN_CS, HIGH);
}


