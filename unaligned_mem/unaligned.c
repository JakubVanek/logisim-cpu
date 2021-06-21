#include <stdint.h>
#include <stdbool.h>

#define UART_CTL_READY     0x01
#define UART_CTL_RESET_IN  0x02
#define UART_CTL_RESET_OUT 0x04
#define LCD_CTL_RESET      0x01

static volatile uint32_t *led_line = (volatile uint32_t *) 0xf0000000u;
static volatile uint32_t *uart_wr  = (volatile uint32_t *) 0xf000000cu;

int main(void)
{
    *led_line = 0;
    const char *str = "Hello, World! This program is\nrunning on a MIPS CPU in Logisim\n";
    const char *ptr = str;
    while (*ptr != '\0') {
        *uart_wr  = *ptr;
        ptr++;
    }
    return 0;
}
