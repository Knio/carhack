#include <avr/io.h>
#include <avr/interrupt.h>
#include <avr/pgmspace.h>

#include <util/delay.h>
#include <stdio.h>
#include <inttypes.h>

#include <SD.h>
#include <mcp2515.h>

#define	PRINT(string, ...) logFile.println(string)//printf_P(PSTR(string), ##__VA_ARGS__)
// ----------------------------------------------------------------------------
File logFile;
tCAN message;
// ----------------------------------------------------------------------------

void print_can_message(tCAN *message)
{
	uint8_t length = message->header.length;
	
	PRINT("ID:     0x%3x\n", message->id);
	PRINT("Length: %d\n", length);
	PRINT("rtr:    %d\n", message->header.rtr);
	
	if (!message->header.rtr) {
		PRINT("Data:  ");
		uint8_t i;
		for (i = 0; i < length; i++) {
			PRINT("0x%02x ", message->data[i]);
		}
		PRINT("\n");
	}
}

void setup(void)
{
        if (!SD.begin(9)) //SD_CS pin
        {
          pinMode(13, OUTPUT);
          while (1)
          {
            digitalWrite(13, HIGH);
            delay(100);
            digitalWrite(13, LOW);
            delay(100);
          }
        }
        
        logFile = SD.open("log.txt", FILE_WRITE);
        
        //Activate interrupts
	sei();

	if (!mcp2515_init(0)) {
		PRINT("Error: unable to communicate with MCP2515!\n");
		for (;;);
	}
	else {
		PRINT("MCP2515 initialized\n\n");
	}
	
	PRINT("Creating message\n");	
	message.id = 0x123;
	message.header.rtr = 0;
	message.header.length = 2;
	message.data[0] = 0xab;
	message.data[1] = 0xcd;
	
	print_can_message(&message);
	
	PRINT("\nChanging to loop-back mode\n\n");
	mcp2515_bit_modify(CANCTRL, (1<<REQOP2)|(1<<REQOP1)|(1<<REQOP0), (1<<REQOP1));
	
	if (mcp2515_send_message(&message)) {
		PRINT("Message successfully written to buffer\n");
	}
	else {
		PRINT("Error: Unable to send message\n");
	}
	
	_delay_ms(10);
	
	if (mcp2515_check_message()) {
		PRINT("Message available!\n");
		
		if (mcp2515_get_message(&message)) {
			print_can_message(&message);
			PRINT("\n");
		}
		else {
			PRINT("Error: Unable to read message\n\n");
		}
	}
	else {
		PRINT("Error: No message receieved\n\n");
	}
	
	PRINT("Changing mode back to normal\n\n");
	mcp2515_bit_modify(CANCTRL, (1<<REQOP2)|(1<<REQOP1)|(1<<REQOP0), 0);
	
	
	PRINT("Attempting to send a message over the CAN-bus\n");
	
	if (mcp2515_send_message(&message)) {
		PRINT("Message successfully written to buffer\n\n");
	}
	else {
		PRINT("Error: Unable to send message\n\n");
	}
	
	PRINT("Waiting to receieve messages\n\n");
        logFile.close();
}

void loop(void)
{/*
  		if (mcp2515_check_message()) {
			PRINT("Receieving message!\n");
			
			if (mcp2515_get_message(&message)) {
				print_can_message(&message);
				PRINT("\n");
			}
			else {
				PRINT("Error: Unable to read message!\n\n");
			}
		}
*/}
