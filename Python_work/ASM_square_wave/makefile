#target: ingredients
#    recipe

sqwv.bin: sqwv.elf #create a binary executable from elf executable
	arm-none-eabi-objcopy -O binary sqwv.elf sqwv.bin

sqwv.elf: sqwv.o linker.ld #create an elf executable from object file, using linker script
	arm-none-eabi-ld -T linker.ld -o sqwv.elf sqwv.o

sqwv.o: assembly.s #create object file from assembly file
	arm-none-eabi-as -mcpu=cortex-a72 -o sqwv.o assembly.s

clean: #remove intermediate files for good housekeeping
	rm -f sqwv.o sqwv.elf sqwv.bin 

