#include "functions.h"
#include <avr/io.h>
#include <util/delay.h>
#include <avr/boot.h>
#include <avr/interrupt.h>
#include <avr/pgmspace.h>

void write_program(const uint32_t address, const uint8_t *program_buffer, const uint32_t program_buffer_size)
{
    uint8_t sreg_last_state = SREG;
    cli();

    eeprom_busy_wait();

    // iterate through the program_buffer one page at a time
    for (uint32_t current_page_address = address;
         current_page_address < (address + program_buffer_size);
         current_page_address += SPM_PAGESIZE)
    {
        boot_page_erase(current_page_address);
        boot_spm_busy_wait(); // Wait until the memory is erased.

        // iterate through the page, one word (two bytes) at a time
        for (uint16_t i = 0; i < SPM_PAGESIZE; i += 2)
        {
            uint16_t current_word = 0;
            if ((current_page_address + i) < (address + program_buffer_size))
            {
                // Set up a little-endian word and point to the next word
                current_word = *program_buffer++;
                current_word |= (*program_buffer++) << 8;
            }
            else
            {
                current_word = 0xFFFF;
            }

            boot_page_fill(current_page_address + i, current_word);
        }

        boot_page_write(current_page_address); // Store buffer in a page of flash memory.
        boot_spm_busy_wait();                  // Wait until the page is written.
    }

    // Re-enable RWW-section. We need this to be able to jump back
    // to the application after bootloading.
    boot_rww_enable();

    // Re-enable interrupts (if they were ever enabled).
    SREG = sreg_last_state;
}


void read_from_serial(uint8_t *dst, size_t size)
{
    uint8_t byte = 0;
    size_t i = 0;
    for (; i < size; i++)
    {
        byte = USART_Receive();
        dst[i] = byte;
    }
}



void calculate_xxhash(const uint8_t *data, size_t len, uint8_t hash[NUM_ECC_DIGITS]) {
  XXH128_hash_t hashResult = XXH3_128bits(data, len); 

  memcpy(hash, &hashResult.low64, 8);
  memcpy(hash + 8, &hashResult.high64, 8);
}


bool verify_image(uint8_t *data, size_t size) {
    uint8_t hash[NUM_ECC_DIGITS];
    
    size_t i = 0;


    uint8_t r[NUM_ECC_DIGITS];
    uint8_t s[NUM_ECC_DIGITS];

    // fill in r and s values
    for (i = 0; i < NUM_ECC_DIGITS; i++) r[i] = data[i];
    for (i = 0; i < NUM_ECC_DIGITS; i++) s[i] = data[NUM_ECC_DIGITS + i];

    calculate_xxhash((uint8_t*) (data + (NUM_ECC_DIGITS * 2)), size - (NUM_ECC_DIGITS * 2), hash); // calculate hash
    for (i = 0; i < 8; i++) hash[16+i] = 0; // padding

    if (ecdsa_verify(&public_0, hash, r, s) == 1) return true;
    return false;
}