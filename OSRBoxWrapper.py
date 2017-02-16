#!/usr/bin/env python

import math
import time
import serial
import codecs

class OSRBoxWrapper:

    '''
    Class constructor.
    Initializes a few importants variables.

    @param string   port        The port to connect to
    @param int      baudrate    The baudrate ~= the speed at which the communication will take place
    '''
    def __init__( self, port, baudrate ):

        self.port       = port
        self.baudrate   = baudrate

        self.tx_encoder = codecs.getincrementalencoder( 'UTF-8' )()

        self.ser = serial.Serial()

        self.ser.port       = self.port
        self.ser.baudrate   = self.baudrate

        self.escape_sequence = '\x1D\x14\n\r'

    '''
    Starts the communication by sending the escape sequence to the OSRBox.
    '''
    def open( self ):

        print( "\nStarting communication on " + self.port + " at " + str( self.baudrate ) + " bauds.\n" )

        try:

            self.command( self.escape_sequence )

        except serial.serialutil.SerialException:

            print( 'Unable to open port ' + self.port + '. Exiting...' )
            raise


    '''
    Ends the communication by sending the escape sequence to the OSRBox.
    '''
    def close( self ):

        # Does'nt work !?
        self.command( self.escape_sequence )
        self.ser.close()


    '''
    Downgrades the connection rate to 9600 bauds, issues the command to the OSR
    then reupgrade the connection to 19200 bauds.

    @param string cmd The command to issue
    '''
    def command( self, cmd ):

        self.ser.close()
        self.ser.baudrate = 9600
        self.ser.open()
        self.write( cmd )
        self.ser.close()
        self.ser.baudrate = self.baudrate
        self.ser.open()


    '''
    Wraps the serial writing operation with an UTF-8 encoding.

    @param string Data The data to write
    '''
    def write( self, data ):

        self.ser.write( self.tx_encoder.encode( data ) )


    '''
    Reads the current OSRBox state.
    Can be False, 1, 2, 3, 4, 5 where False stands for no button(s) pressed(s)
    and the numbers for the correlating key number (1-indexed)

    @return int key The pressed key or False if no key is currently pressed
    '''
    def read( self ):

        response = self.ser.read( 1 )
        response = ord( response )

        if response == 0:
            return False

        response = math.log( response, 2 )
        response = int( response ) + 1

        return response


    '''
    Outputs the current input flow, visual purposes.
    '''
    def debug( self ):

        while True:

            if ( self.ser.inWaiting() ):
                print self.read()
