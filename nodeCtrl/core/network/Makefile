CC=gcc
PLATFORM=LINUX

ifeq ($(PLATFORM),MSP430)
	MCU=-mmcu=msp430g2553
	CC=msp430-gcc
endif

DEPS = network.h ../neighbor/neighbor.h ../routing/routing.h ../memory_map/memory_map.h

OBJ = network.o ../memory_map/memory_map.o

PACK = 0

%.o: %.c $(DEPS)
	$(CC) -c -Os -DPACK_STRUCT=$(PACK) -D$(PLATFORM) -o $@ $< 
	$(CC) -S -Os -DPACK_STRUCT=$(PACK) -D$(PLATFORM) -o $(basename $@)_$(PACK)_$(PLATFORM).asm $< 

pgrm: $(OBJ)
	echo "built network"

test: clean pgrm 

.PHONY: clean

clean:
	rm -f *.o *~ pgrm
