// Lawicel_can.h
//
// Copyright (c) 2005-2006 LAWICEL AB, Sweden
//
// Version 0.0.14
//

#ifndef __LAWICELCANH__         
#define __LAWICELCANH__


#ifdef __cplusplus
  extern "C" {
#endif

// Types
typedef unsigned char _u8;
typedef unsigned short _u16;
typedef unsigned int _u32;

typedef long CANHANDLE;
typedef unsigned char CANDATA;

// Status bits
#define CANSTATUS_RECEIVE_FIFO_FULL		0x01
#define CANSTATUS_TRANSMIT_FIFO_FULL	0x02
#define CANSTATUS_ERROR_WARNING			0x04
#define CANSTATUS_DATA_OVERRUN			0x08
#define CANSTATUS_ERROR_PASSIVE			0x20
#define CANSTATUS_ARBITRATION_LOST		0x40
#define CANSTATUS_BUS_ERROR				0x80

// Filter mask settings
#define CANUSB_ACCEPTANCE_CODE_ALL		0x00000000
#define CANUSB_ACCEPTANCE_MASK_ALL		0xFFFFFFFF

// Message flags
#define CANMSG_EXTENDED	0x80 // Extended CAN id
#define CANMSG_RTR		0x40 // Remote frame

// Flush flags
#define FLUSH_WAIT		0x00
#define FLUSH_DONTWAIT	0x01

// CAN Frame
typedef struct {
    _u32 id;        // Message id
    _u32 timestamp; // timestamp in milliseconds	
    _u8  flags;     // [extended_id|1][RTR:1][reserver:6]
    _u8  len;       // Frame size (0.8)
    _u8  data[ 8 ]; // Databytes 0..7
} CANMsg;


// Alternative CAN Frame
typedef struct {
	_u32 id;        // Message id
	_u32 timestamp; // timestamp in milliseconds
	_u8  flags;     // [extended_id|1][RTR:1][reserver:6]
	_u8  len;       // Frame size (0.8)
} CANMsgEx;

// Error return codes
#define ERROR_CANUSB_OK					1
#define ERROR_CANUSB_GENERAL			-1
#define ERROR_CANUSB_OPEN_SUBSYSTEM		-2
#define ERROR_CANUSB_COMMAND_SUBSYSTEM	-3
#define ERROR_CANUSB_NOT_OPEN			-4
#define ERROR_CANUSB_TX_FIFO_FULL		-5
#define ERROR_CANUSB_INVALID_PARAM		-6
#define ERROR_CANUSB_NO_MESSAGE			-7
#define ERROR_CANUSB_MEMORY_ERROR		-8
#define ERROR_CANUSB_NO_DEVICE			-9
#define ERROR_CANUSB_TIMEOUT			-10

// Open flags
#define CANUSB_FLAG_TIMESTAMP			0x0001	// Timestamp messages
#define CANUSB_FLAG_QUEUE_REPLACE		0x0002	// If input queue is full remove
												// oldest message and insert new
												// message.
// Prototypes

///////////////////////////////////////////////////////////////////////////////
// canusb_Open
//
// Open CAN interface to device
//
// Returs handle to device if open was successfull or zero
// or negative error code on falure.
//
//
// szID
// ====
// Serial number for adapter or NULL to open the first found.
//
//
// szBitrate
// =========
// "10" for 10kbps  
// "20" for 20kbps
// "50" for 50kbps
// "100" for 100kbps
// "250" for 250kbps
// "500" for 500kbps
// "800" for 800kbps
// "1000" for 1Mbps
//
// or 
//
// btr0:btr1 pair  ex. "0x03:0x1c" or 3:28
//
// acceptance_code
// ===============
// Set to CANUSB_ACCEPTANCE_CODE_ALL to  get all messages.
//
// acceptance_mask
// ===============
// Set to CANUSB_ACCEPTANCE_MASk_ALL to  get all messages.
//
// flags
// =====
// CANUSB_FLAG_TIMESTAMP - Timestamp will be set by adapter.
 
CANHANDLE WINAPI canusb_Open( LPCTSTR szID, 
							 LPCTSTR szBitrate, 
							 unsigned long acceptance_code,
							 unsigned long acceptance_mask,
							 unsigned long flags );



///////////////////////////////////////////////////////////////////////////////
// canusb_Close
//
// Close channel with handle h.
//
// Returns <= 0 on failure. >0 on success.

int WINAPI canusb_Close( CANHANDLE h );



///////////////////////////////////////////////////////////////////////////////
// canusb_Read 
//
// Read message from channel with handle h. 
//
// Returns <= 0 on failure. >0 on success.
//

int WINAPI canusb_Read( CANHANDLE h, CANMsg *msg );


///////////////////////////////////////////////////////////////////////////////
// canusb_ReadEx
//
// Read message from channel with handle h.
//
// This is a version without a data-array in the structure to work with LabView
//
// Returns <= 0 on failure. >0 on success.
//

int WINAPI canusb_ReadEx( CANHANDLE h, CANMsgEx *msg, CANDATA *pData );

///////////////////////////////////////////////////////////////////////////////
// canusb_ReadFirst 
//
// Read message from channel with handle h and id "id" which satisfying flags. 
//
// Returns <= 0 on failure. >0 on success.
//

int WINAPI canusb_ReadFirst( CANHANDLE h,
								unsigned long id,
								unsigned char flags,
								CANMsg *msg );


///////////////////////////////////////////////////////////////////////////////
// canusb_ReadFirstEx
//
// Read message from channel with handle h and id "id" which satisfying flags.
//
// This is a version without a data-array in the structure to work with LabView
//
// Returns <= 0 on failure. >0 on success.
//

int WINAPI canusb_ReadFirstEx( CANHANDLE h, 
									unsigned long id, 
									unsigned char flags, 
									CANMsgEx *msg, 
									CANDATA *pData );


///////////////////////////////////////////////////////////////////////////////
// canusb_Write
//
// Write message to channel with handle h.
//
// Returns <= 0 on failure. >0 on success.
//

int WINAPI canusb_Write( CANHANDLE h, CANMsg *msg );


///////////////////////////////////////////////////////////////////////////////
// canusb_WriteEx
//
// Write message to channel with handle h. 
//
// This is a version without a data-array in the structure to work with LabView
//
// Returns <= 0 on failure. >0 on success.
//

int WINAPI canusb_WriteEx( CANHANDLE h, CANMsgEx *msg, CANDATA *pData );



///////////////////////////////////////////////////////////////////////////////
// canusb_Status
//
// Get Adaper status for channel with handle h. 

int WINAPI canusb_Status( CANHANDLE h );



///////////////////////////////////////////////////////////////////////////////
// canusb_VersionInfo
//
// Get hardware/fi4rmware and driver version for channel with handle h. 
//
// Returns <= 0 on failure. >0 on success.
//
// 

int WINAPI canusb_VersionInfo( CANHANDLE h, LPTSTR verinfo );


///////////////////////////////////////////////////////////////////////////////
// canusb_Flush
//
// Flush output buffer on channel with handle h. 
//
// Returns <= 0 on failure. >0 on success.
//
// If flushflags is set to FLUSH_DONTWAIT the queue is just emptied and 
// there will be no wait for any frames in it to be sent 
//

int WINAPI canusb_Flush( CANHANDLE h, unsigned char flushflags );


#ifdef __cplusplus
}
#endif

#endif // __LAWICELCANH__
