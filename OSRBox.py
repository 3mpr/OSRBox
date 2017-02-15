#!/usr/bin/env python

import math
import time
import serial
import codecs

class OSRBox:

    port = 'COM3'
    baudrate = 19200

    tx_encoding = 'UTF-8'
    rx_encoding = 'Latin1'

    menu_char = '0x14'
    exit_char = '0x1d'

    '''
    Class constructor.
    Initializes a few importants variables.

    @param string port The port to connect to
    @param int baudrate The baudrate at which the communication will take place
    '''
    def __init__( self, port = False, baudrate = False ):

        self.port       = self.port if port is False else port
        self.baudrate   = self.baudrate if baudrate is False else baudrate

        self.tx_encoder = codecs.getincrementalencoder( self.tx_encoding )

        self.ser = serial.Serial()

        self.ser.port       = self.port
        self.ser.baudrate   = self.baudrate

        try:

            self.ser.open()

        except serial.serialutil.SerialException:

            print( 'Unable to open port ' + self.port + '. Exiting...' )
            exit( 1 )


    '''
    Starts the communication by sending a carriage return (?) to the OSRBox.
    '''
    def start( self ):

        print( "Starting..." )
        self.write( self.menu_char + self.exit_char )

    def write( self, data ):

        self.ser.write( self.tx_encoder.encode( data ) )

    '''
    Reads the current OSRBox state.

    Can be False, 0, 1, 2, 3, 4 where False stands for no button(s) pressed(s)
    and the numbers for the correlating key number (0-indexed)
    '''
    def read( self ):

        response = self.ser.read( 1 )
        response = ord( response )

        if response == 0:
            return False

        response = math.log( response, 2 )
        response = int( response )

        return response

    '''
    Outputs the current input flow, visual purposes.
    '''
    def debug( self ):

        while True:

            if ( self.ser.inWaiting() ):
                print self.read()

if __name__ == "__main__":

    pad = OSRBox()
    pad.start()
    pad.debug()
