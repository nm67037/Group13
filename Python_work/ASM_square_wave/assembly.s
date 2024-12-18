.global _start 

.equ GPIO_base, 0xFE200000 @actual base address for GPIO work.
.equ GPFSEL2, 0x08 @Function Select 2 is required to control GPIO 21. It has an offset of 0x8 from base.
.equ GPIO_21_OUT, 0x08 @This is what FSEL2 needs to be set to to make GPIO21 an OUT.

.equ SET0, 0x1C @offset from base to appropriate set register
.equ CLR0, 0x28 @offset from base to appropriate clear register

.equ delay, 0x59682F00 @this sets the delay to 1 second

.equ GPIO21_value, 0x200000 @In 24 bits, 1 logical shifted left 21 spaces.

_start:

    ldr r0 =GPIO_base @make r0 the base/reference register

    ldr r1 =GPIO_21_OUT
    str r1, [r0, #GPFSEL2]
    @make FSEL2 8, making GPIO21 an OUTPUT

    ldr r2,=delay

loop: @turn on LED

    ldr r1, =GPIO21_value
    str r1, [r0, #SET0] @turn ON

    @controllable? delay
    mov r10, #0 @clear r10
    delay1
        add r10, r10, #1 @increment by 1
        cmp r10, r2 
        bne, delay1 @branch to keep delaying. Fall through if increment counter r10 reaches initial counter in r2.

    @above program turns ON the LED and waits for some time

    ldr r1, =GPIO21_value
    str r1, [r0, #CLR0] @turn OFF

    @controllable? delay
    mov r10, #0 @clear r10
    delay2
        add r10, r10, #1 @increment by 1
        cmp r10, r2 
        bne, delay2 @branch to keep delaying. Fall through if r10 reaches r2.

    @above program turns OFF the LED. Same logic as turn ON. Just using CLR register instead.

    b loop @run PWM/square wave code indefinitely

    @delay comments: Each delay takes 2 clock cycles (ignoring branches due to good branch prediction)
    @Thus, if you want the delay between PWM ON and OFF to be 1 second, and 1 clock cycle is 0.67 ns, 
    @then set r2 to be the hex conversion of 1.5 billion (decimal)


