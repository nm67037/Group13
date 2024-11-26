@ mmap part taken from by https://bob.cs.sonoma.edu/IntroCompOrg-RPi/sec-gpio-mem.html

@ Constants for blink at GPIO21
@ GPFSEL2 [Offset: 0x08] responsible for GPIO Pins 20 to 29
@ GPCLR0 [Offset: 0x28] responsible for GPIO Pins 0 to 31
@ GPSET0 [Offest: 0x1C] responsible for GPIO Pins 0 to 31

@ GPOI21 Related
.equ    GPFSEL2, 0x08   @ function register offset
.equ    GPCLR0, 0x28    @ clear register offset
.equ    GPSET0, 0x1c    @ set register offset
.equ    GPFSEL2_GPIO21_MASK, 0b111000   @ Mask for fn register
.equ    MAKE_GPIO21_OUTPUT, 0b1000      @ use pin for ouput
.equ    PIN, 21                         @ Used to set PIN high / low

@ Args for mmap
.equ    OFFSET_FILE_DESCRP, 0   @ file descriptor
.equ    mem_fd_open, 3
.equ    BLOCK_SIZE, 4096        @ Raspbian memory page
.equ    ADDRESS_ARG, 3          @ device address

@ Misc
.equ    SLEEP_IN_S,1            @ sleep one second

@ The following are defined in /usr/include/asm-generic/mman-common.h:
.equ    MAP_SHARED,1    @ share changes with other processes
.equ    PROT_RDWR,0x3   @ PROT_READ(0x1)|PROT_WRITE(0x2)

.equ    duty,50         @ Square Wave dutycycle gets defined here
.equ    frq,1000        @ Square Wave frequency gets defined here

@ Constant program data
    .section .rodata
device:
    .asciz  "/dev/gpiomem"

@ The program
    .text
    .global main
main:
@ Open /dev/gpiomem for read/write and syncing
    ldr     r1, O_RDWR_O_SYNC   @ flags for accessing device
    ldr     r0, mem_fd          @ address of /dev/gpiomem
    bl      open     
    mov     r4, r0              @ use r4 for file descriptor

@ Map the GPIO registers to a main memory location so we can access them
@ mmap(addr[r0], length[r1], protection[r2], flags[r3], fd[r4])
    str     r4, [sp, #OFFSET_FILE_DESCRP]   @ r4=/dev/gpiomem file descriptor
    mov     r1, #BLOCK_SIZE                 @ r1=get 1 page of memory
    mov     r2, #PROT_RDWR                  @ r2=read/write this memory
    mov     r3, #MAP_SHARED                 @ r3=share with other processes
    mov     r0, #mem_fd_open                @ address of /dev/gpiomem
    ldr     r0, GPIO_BASE                   @ address of GPIO
    str     r0, [sp, #ADDRESS_ARG]          @ r0=location of GPIO
    bl      mmap
    mov     r5, r0           @ save the virtual memory address in r5

@ Set up the GPIO pin funtion register in programming memory
    add     r0, r5, #GPFSEL2            @ calculate address for GPFSEL2
    ldr     r2, [r0]                    @ get entire GPFSEL2 register
    bic     r2, r2, #GPFSEL2_GPIO21_MASK@ clear pin field
    orr     r2, r2, #MAKE_GPIO21_OUTPUT @ enter function code
    str     r2, [r0]                    @ update register

@ Calculate the number of loops necessary to pulse at the frequency and duty cycle defined above
frqnduty:
    ldr r7, =frq        @ r7 = frequency defined at the top of the file
    lsl r7,#1           @ r7 * 2
    ldr r8,=#1800475088 @ r8 = Raspberry Pi Clock Speed
    udiv r7, r8, r7     @ r7 = Pi Clock Speed / (defined frequency * 2)
    mov r9, r7          @ r9 = total clocks for 1 period at defined frequency
    mov r8, #100        @ r8 = 100
    udiv r7, r7, r8     @ r7 = one hundrendth of the required loops
    mov r8, #duty       @ r8 = %dutycycle
    mul r7, r8, r7      @ r7 = number of loops * (%dutycycle/100)
    sub r8, r9, r7      @ r8 = total number of loops - number of loops spent on

@ main loop of the program
mainloop:    
    bl on       @ Turn on the GPio then return here after its delay
    bl off      @ Turn off the GPio then return here after its delay
    b mainloop  @ Repeat

@Delay Time on
delay_on:
    mov	r6, r7	@ r6 = number of loops to achieve the right on time required by frequency and duty 

onl:	subs	r6, r6, #1		@ Decrement loop count down 
	bne	onl			            @ repeat on loop until r6 = 0 
    bx lr       @ Return to caller at mainloop

@Delay time off
delay_off:
    mov	r6, r8	@ r6 = number of loops to achieve the right off time required by frequency and duty 

offl:	subs	r6, r6, #1		@ Decrement loop count down
    bne	offl			        @ repeat off loop until r6 = 0 
    bx lr       @ Return to caller at mainloop

on:
@ Turn on
    add     r0, r5, #GPSET0 @ calc GPSET0 address
    mov     r3, #1          @ turn on bit
    lsl     r3, r3, #PIN    @ shift bit to pin position
    orr     r2, r2, r3      @ set bit
    str     r2, [r0]        @ update register

    b delay_on              @ branch to on delay loop

off:
@ Turn off
    add     r0, r5, #GPCLR0 @ calc GPCLR0 address
    mov     r3, #1          @ turn off bit
    lsl     r3, r3, #PIN    @ shift bit to pin position
    orr     r2, r2, r3      @ set bit
    str     r2, [r0]        @ update register

    b delay_off             @ branch to off delay loop

GPIO_BASE:
    .word   0xfe200000  @GPIO Base address Raspberry pi 4
mem_fd:
    .word   device
O_RDWR_O_SYNC:
    .word   2|256       @ O_RDWR (2)|O_SYNC (256).
