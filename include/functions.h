#ifndef FUNCTIONS_H__
#define FUNCTIONS_H__

#include <Arduino.h>
#include "uart.h"
#include "ecc.h"
#include "keys.h"

void write_program(const uint32_t address, const uint8_t *program_buffer, const uint32_t program_buffer_size);

bool verify_image(uint8_t *data, size_t size);

void calculate_xxhash(const uint8_t *data, size_t len, uint8_t hash[NUM_ECC_DIGITS]);

void read_from_serial(uint8_t *dst, size_t size);

#endif