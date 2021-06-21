#include <stdint.h>

int main(void)
{
    volatile uint32_t *led_line = (volatile uint32_t *) 0xf0000000u;
    int fib_now = 0;
    int fib_next = 1;
    for (int i = 0; i < 20; i++) {
        int fib_bak = fib_next;
        fib_next = fib_now + fib_next;
        fib_now = fib_bak;
        *led_line = fib_now;
    }
    return 0;
}
