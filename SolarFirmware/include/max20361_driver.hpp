#ifndef MAX20361_DRIVER_H
#define MAX20361_DRIVER_H

#include <stdint.h>
#include <Wire.h>


#define I2CMPPT_ADDR      0x15
#define DeviceID_ADDR     0x00
#define Status_ADDR       0x01
#define Int_ADDR          0x02
#define IntMsk_ADDR       0x03
#define SysRegCfg_ADDR    0x04
#define WakeCfg_ADDR      0x05
#define MpptCfg_ADDR      0x06
#define MeasCfg_ADDR      0x07
#define DevCntl_ADDR      0x08
#define VOCMeas_ADDR      0x09
#define HarvCntH_ADDR     0x0A
#define HarvCntL_ADDR     0x0B
#define SleepThd_ADDR     0x0C

#define DeviceID_VAL      0x11
#define Status_VAL        0x00
#define Int_VAL           0x00
#define IntMsk_VAL        0x00
#define SysRegCfg_VAL     0x02
#define WakeCfg_VAL       0xC1
#define MpptCfg_VAL       0x19
#define MeasCfg_VAL       0x0E
#define DevCntl_VAL       0x38
#define VOCMeas_VAL       0x05
#define HarvCntH_VAL      0x00
#define HarvCntL_VAL      0x00
#define SleepThd_VAL      0x00


void mppt_init(void);

uint8_t mppt_read_register(uint8_t reg);

void mppt_write_register(uint8_t reg, uint8_t value);



#endif