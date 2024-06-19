#ifndef UART_H__
#define UART_H__

#include <Arduino.h>

#define F_CPU 16000000UL
#define BAUD 9600
#define UBRR F_CPU / 16 / BAUD - 1

void USART_Init(unsigned int ubrr);
void USART_Transmit(uint8_t data);
unsigned char USART_Receive(void);
void USART_Print(const uint8_t *data);

void USART_TransmitHEX(uint8_t data);
void USART_PrintHEX(const uint8_t *data, size_t len);

#endif