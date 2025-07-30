#ifndef MAX17048_DRIVER_H
#define MAX17048_DRIVER_H



#include <stdint.h>
#include <Wire.h>


#define VCELL_ADDR        0x02
#define SOC_ADDR          0x04
#define MODE_ADDR         0x06
#define VERSION_ADDR      0x08
#define HIBRT_ADDR        0x0A
#define CONFIG_ADDR       0x0C
#define VALRT_ADDR        0x14
#define CRATE_ADDR        0x16
#define VRESET_ID_ADDR    0x18
#define STATUS_ADDR       0x1A
#define CMD_ADDR          0xFE


#define MODE_VAL_DEFAULT       0x0000
#define HIBRT_VAL_DEFAULT      0x8030
#define CONFIG_VAL_DEFAULT     0x971C
#define VALRT_VAL_DEFAULT      0x00FF
#define VRESET_ID_VAL_DEFAULT  0x9600  // assume lower byte = 0x00 placeholder
#define STATUS_VAL_DEFAULT     0x0100  // assume lower byte = 0x00 placeholder
#define CMD_VAL_POR            0xFFFF 

#define I2CFG_ADDR        0x36

void fg_init(void);

uint8_t fg_read_register(uint8_t reg);

void fg_write_register(uint8_t reg, uint8_t value);

#endif