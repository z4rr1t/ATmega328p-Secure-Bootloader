#ifndef KEYS_H__
#define KEYS_H__

#define ECC_CURVE secp192r1
#include "ecc.h"
#include "xxhash.h"

static uint8_t private_0[NUM_ECC_DIGITS] = {0x64, 0xF2, 0x04, 0xD7, 0x01, 0x8B, 0xCC, 0xAA, 0x61, 0x17, 0x3E, 0xB6, 0xE1, 0xE8, 0x15, 0x3E, 0x77, 0xB5, 0xC8, 0xA6, 0x0E, 0x0B, 0x9C, 0xE8};
static EccPoint public_0 = {
    {0x4F, 0x21, 0x34, 0x41, 0x39, 0x37, 0x46, 0xFF, 0x40, 0x6C, 0x40, 0x4E, 0xD7, 0x97, 0x8F, 0xF7, 0x22, 0xD6, 0x8F, 0x20, 0xAC, 0xC8, 0x01, 0x3A},
    {0x58, 0x0E, 0xBE, 0x72, 0x72, 0xB3, 0xE9, 0xD9, 0xA0, 0x1D, 0xB0, 0xEB, 0xAC, 0x9C, 0x65, 0xDB, 0xBE, 0x92, 0xF0, 0xCA, 0xEE, 0xB1, 0xD0, 0x77}};

#endif