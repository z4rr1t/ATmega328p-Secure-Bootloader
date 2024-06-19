#include "uart.h"

void USART_Init(unsigned int ubrr)
{
  UBRR0H = (uint8_t)(ubrr >> 8);
  UBRR0L = (uint8_t)ubrr;

  // enable tx and rx
  UCSR0B = (1 << RXEN0) | (1 << TXEN0);

  // usart format: 8 bit data, 2 stop bits;
  UCSR0C = (1 << USBS0) | (3 << UCSZ00);
}

void USART_Transmit(uint8_t data)
{
  while (!(UCSR0A & (1 << UDRE0)))
  {
  } // wait for empty tx buffer

  UDR0 = data;
}

unsigned char USART_Receive(void)
{
  while (!(UCSR0A & (1 << RXC0)))
  {
  } // wait for data to be available

  return UDR0;
}

void USART_Print(const uint8_t *data)
{
  while (*(data))
    USART_Transmit((uint8_t) * (data++));
}

void USART_TransmitHEX(uint8_t data)
{
  uint8_t n;
  n = data >> 4;
  if (n < 10)
    USART_Transmit((uint8_t)('0' + n));
  else
    USART_Transmit((uint8_t)('a' + (n - 10)));

  n = data & 0xf;
  if (n < 10)
    USART_Transmit((uint8_t)('0' + n));
  else
    USART_Transmit((uint8_t)('a' + (n - 10)));
}

void USART_PrintHEX(const uint8_t *data, size_t len)
{
  size_t i = 0;
  while (i < len)
  {
    USART_TransmitHEX((uint8_t)data[i++]);
    USART_Transmit(' ');
  }

  USART_Transmit('\n');
}