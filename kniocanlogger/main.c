/*
  Name: SaabCanLogger
  Copyright: Freeware, use as you please
  Author: Tomi Liljemark (firstname.surname@gmail.com)
  Created: 2007-07-12
  Modified: 2007-08-23
  Compiler: Dev-C++ v4.9.9.2 (shouldn't matter)
            Uses libraries canusbdrv.lib and FTD2XX.lib
  Description: Freeware Saab I-Bus or P-Bus logger
               Logs all CAN messages to a comma separated text file
*/

#include <stdio.h>
#include <stdlib.h>
#include <windows.h>
#include "lawicel_can.h"

#define RELEASE_VERSION "0.30"
#define RELEASE_DATE    "2007-08-23"


int main(int argc, char *argv[])
{
    CANHANDLE h;
    CANMsg msg;
    FILE *log;
    int ch, ret, i;
    int timestamp, last_timestamp;

    printf("---- KnioCanLogger ----\n");

    if( argc < 2 )
    {
        printf("Usage: KnioCanLogger <filename.log>\n");
        return -1;
    }

    log = fopen( argv[1], "a" );
    if( log == NULL )
    {
        printf("Failed to open log file '%s'.\n", argv[1]);
        fclose( log );
        return -1;
    }

    printf("Opening CAN channel to Knio's car (1000 kBit/s)...");
    // Open CAN Channel
    if ( 0 >= ( h = canusb_Open( NULL,
    		"1000",
    		CANUSB_ACCEPTANCE_CODE_ALL,
    		CANUSB_ACCEPTANCE_MASK_ALL,
    		CANUSB_FLAG_TIMESTAMP ) ) ) {
    	printf("Failed to open device\n");
    	fclose( log );
    	return -1;
    }
    
    printf("OK\n");

    printf("Logging to file '%s'. Press ESC to stop logging.\n", argv[1]);

    ch = 0;
    timestamp = 0;
    last_timestamp = 0;

    while( !kbhit() )
    {
        ret = canusb_Read( h, &msg );
        if( ret == ERROR_CANUSB_OK )
        {
            if( msg.timestamp < last_timestamp )
            {
                timestamp++;
                printf(".");
            }
            last_timestamp = msg.timestamp;
            fprintf( log, "%08X,%03X,%d,%02X,%02X,%02X,%02X,%02X,%02X,%02X,%02X\n\r", msg.timestamp+(timestamp<<16), msg.id, msg.len,
                                                                          msg.data[0], msg.data[1], msg.data[2],
                                                                          msg.data[3], msg.data[4], msg.data[5], 
                                                                          msg.data[6], msg.data[7]);
            printf( "%08X,%03X,%d,%02X,%02X,%02X,%02X,%02X,%02X,%02X,%02X\n", msg.timestamp+(timestamp<<16), msg.id, msg.len,
                                                                          msg.data[0], msg.data[1], msg.data[2],
                                                                          msg.data[3], msg.data[4], msg.data[5],
                                                                          msg.data[6], msg.data[7]);
        }
        else if( ret != ERROR_CANUSB_NO_MESSAGE )
        {
            printf("E%d", ret);
        }
    }
    if( kbhit() ) i = getch();
    
    // Flush data CAN channel
    canusb_Flush( h, FLUSH_WAIT );
    
    // Close CAN channel
    canusb_Close( h );
    printf("\nCAN channel closed.\n");

    fclose( log );
    return 0;
}
