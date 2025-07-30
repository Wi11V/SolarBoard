#include <Arduino.h>
#include "max20361_driver.hpp"
#include "max17048_driver.hpp"

void setup() {
  Serial.begin(115200);
  Wire.begin();

  mppt_init();
  fg_init();
}

void loop() {

  uint8_t HRVST_COUNTH = mppt_read_register(HarvCntH_ADDR);
  uint8_t HRVST_COUNTL = mppt_read_register(HarvCntL_ADDR);
  uint8_t VOC_MEASURE = mppt_read_register(VOCMeas_ADDR);
  uint16_t COUNT = ((uint16_t)HRVST_COUNTH << 8) | HRVST_COUNTL;


  uint8_t VCELL = fg_read_register(VCELL_ADDR);
  uint8_t SOC = fg_read_register(SOC_ADDR);
  uint8_t DISCHARGE = fg_read_register(CRATE_ADDR);
  
  Serial.print("VOC:");
  Serial.print(VOC_MEASURE);
  Serial.print("|COUNT:");
  Serial.print(COUNT);
  Serial.print("|VCELL:");
  Serial.print(VCELL);
  Serial.print("|SOC:");
  Serial.print(SOC);
  Serial.print("|DISCHARGE:");
  Serial.println(DISCHARGE);  
  delay(500); 
}

//-----------FG DRIVER----------------------------------------------------

void fg_init(void){
    uint8_t dev_id = fg_read_register(VERSION_ADDR);
    if (dev_id != VRESET_ID_VAL_DEFAULT ){
        Serial.print("Unexpected Device ID");
        Serial.println(dev_id,HEX);
        return;
    }
    

}

uint8_t fg_read_register(uint8_t reg){
    Wire.beginTransmission(I2CFG_ADDR);
    Wire.write(reg);
    Wire.endTransmission(false);
    Wire.requestFrom(I2CFG_ADDR,1);

    if(Wire.available()){
        return Wire.read();
    }else{
        return 0xFF;
    }

}

void fg_write_register(uint8_t reg, uint8_t val){
    Wire.beginTransmission(I2CFG_ADDR);
    Wire.write(reg);
    Wire.write(val);
    Wire.endTransmission();
}

//------------------------------------------------------------------------

//--------MPPT DRIVER-----------------------------------------------------

void mppt_init(void){
    uint8_t dev_id = mppt_read_register(DeviceID_ADDR);
    if (dev_id != 0x11){
        Serial.print("Unexpected Device ID");
        Serial.println(dev_id,HEX);
        return;
    }
    mppt_write_register(MpptCfg_ADDR, MpptCfg_VAL);  //  VMP/VOC ratio
    mppt_write_register(WakeCfg_ADDR, WakeCfg_VAL);  //  VOC meas, VTH meas, CLMP, WakeThr 
    mppt_write_register(MeasCfg_ADDR, MeasCfg_VAL);  //  Meas time, settling time, interval
    mppt_write_register(DevCntl_ADDR, DevCntl_VAL);  //  Boost pk current, Thermal en, wake, i2c

    mppt_read_register(Int_ADDR); // Clears interrupts

}

uint8_t mppt_read_register(uint8_t reg){
    Wire.beginTransmission(I2CMPPT_ADDR);
    Wire.write(reg);
    Wire.endTransmission(false);
    Wire.requestFrom(I2CMPPT_ADDR,1);

    if(Wire.available()){
        return Wire.read();
    }else{
        return 0xFF;
    }

}

void mppt_write_register(uint8_t reg, uint8_t val){
    Wire.beginTransmission(I2CMPPT_ADDR);
    Wire.write(reg);
    Wire.write(val);
    Wire.endTransmission();
}




