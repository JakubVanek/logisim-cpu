#include <stdint.h>
#include <stdbool.h>

#define UART_CTL_READY     0x01
#define UART_CTL_RESET_IN  0x02
#define UART_CTL_RESET_OUT 0x04
#define LCD_CTL_RESET      0x01

static volatile uint32_t *led_line = (volatile uint32_t *) 0xf0000000u;
static volatile uint32_t *uart_ctl = (volatile uint32_t *) 0xf0000004u;
static volatile uint32_t *uart_rd  = (volatile uint32_t *) 0xf0000008u;
static volatile uint32_t *uart_wr  = (volatile uint32_t *) 0xf000000cu;
static volatile uint32_t *lcd_ctl  = (volatile uint32_t *) 0xf0000010u;
static volatile uint32_t *lcd_data = (volatile uint32_t *) 0xf0000014u;

int main(void)
{
    *led_line = 0;
    *uart_ctl = UART_CTL_RESET_IN | UART_CTL_RESET_OUT;
    *lcd_ctl = LCD_CTL_RESET;

    *uart_wr = 'H';
    *uart_wr = 'e';
    *uart_wr = 'l';
    *uart_wr = 'l';
    *uart_wr = 'o';
    *uart_wr = '!';
    *uart_wr = '\n';

    for (int y = 0; y < 2; y++) {
        for (int x = 0; x < 2; x++) {
            *(lcd_data + y * 128 + x) = 0x00FFFFFF;
        }
    }

    *uart_wr = 'y';
    *uart_wr = 'e';
    *uart_wr = 'a';
    *uart_wr = 'h';
    *uart_wr = '\n';

    while (true) {
        while (*uart_ctl == 0) {}
        do { *uart_wr = *uart_rd; } while (*uart_ctl != 0);
    }

    return 0;
}
