

#include <avr/io.h>
#include <avr/interrupt.h>
#include <avr/pgmspace.h>

#include <util/delay.h>
#include <stdio.h>
#include <inttypes.h>

#include <SD.h>
#include <mcp2515.h>

#define PRINT_TO_FILE 1

#if PRINT_TO_FILE
#define	PRINT(str, ...) {sprintf(buf, str, ##__VA_ARGS__); logFile.write(buf); logFile.flush();}
#else
#define	PRINT(str, ...) {sprintf(buf, str, ##__VA_ARGS__); Serial.write(buf);}
#endif
// ----------------------------------------------------------------------------
File logFile;
tCAN message;
char buf[255];
uint8_t loopCount, statusLED;
// ----------------------------------------------------------------------------

void print_can_message(tCAN *message)
{
	uint8_t length = message->header.length;

	PRINT("[ID 0x%03x]", message->id);
	PRINT("[Length %d]", length);
	PRINT("[rtr 0x%02x]", message->header.rtr);

	if (!message->header.rtr) {
		PRINT("[");
		uint8_t i;
		for (i = 0; i < length-1; i++) {
			PRINT("0x%02x ", message->data[i]);
		}
                PRINT("0x%02x]",
                message->data[length-1]);
	}
}

void loopback_test(void)
{
	PRINT("Creating message\n");
	message.id = 0x123;
	message.header.rtr = 0;
	message.header.length = 2;
	message.data[0] = 0xab;
	message.data[1] = 0xcd;

	print_can_message(&message);

	PRINT("Changing to loop-back mode\n");
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
			PRINT("Error: Unable to read message\n");
		}
	}
	else {
		PRINT("Error: No message receieved\n");
	}

	PRINT("Changing mode back to normal\n");
	mcp2515_bit_modify(CANCTRL, (1<<REQOP2)|(1<<REQOP1)|(1<<REQOP0), 0);
}

void setup(void)
{
        pinMode(3, OUTPUT);
        digitalWrite(3, HIGH);
        
#if PRINT_TO_FILE
	SD.begin(9);
//SD_CS pin
	logFile = SD.open("log.txt", FILE_WRITE);
#else
	Serial.begin(9600);
#endif

	PRINT("----------------------------------------------------\n");

	//Activate interrupts
	sei();

	if (!mcp2515_init()) {
		PRINT("Error: unable to communicate with MCP2515!\n");
		return;
	}
	else {
		PRINT("MCP2515 initialized\n");
	}
        
	PRINT("Waiting to receieve messages\n");
}

void loop(void)
{
	logFile = SD.open("log.txt", FILE_WRITE);
	if (mcp2515_check_message()) {
		if (mcp2515_get_message(&message)) {
                        digitalWrite(3, HIGH);
			print_can_message(&message);
			PRINT("\n");
		}
		else {
			PRINT("Error: Unable to read a message!\n");
		}

	}
        digitalWrite(3, LOW);
        logFile.close();
}

