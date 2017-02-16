#!/usr/bin/env python

import math
import time
import serial
import codecs

class OSRBox:

    port = 'COM3'

    initial_baudrate = 9600
    baudrate = 19200

    tx_encoding = 'UTF-8'

    exit_char = 0x1D
    menu_char = 0x14

    '''
    Class constructor.
    Initializes a few importants variables.

    @param string port The port to connect to
    @param int baudrate The baudrate at which the communication will take place
    '''
    def __init__( self, port = False, baudrate = False ):

        self.port       = self.port if port is False else port
        self.baudrate   = self.baudrate if baudrate is False else baudrate

        self.tx_encoder = codecs.getincrementalencoder( self.tx_encoding )()

        self.ser = serial.Serial()

        self.ser.port       = self.port
        self.ser.baudrate   = self.initial_baudrate

        try:

            self.ser.open()

        except serial.serialutil.SerialException:

            print( 'Unable to open port ' + self.port + '. Exiting...' )
            exit( 1 )


    '''
    Starts the communication by sending the escape sequence to the OSRBox.
    '''
    def start( self ):

        # self.ser.write( str(0x1D) + str(0x14) )
        # self.ser.write( '\x0A' )
        # self.ser.write( '\x0C' )
        # self.ser.write( self.menu_char )

        self.ser.baudrate = self.baudrate
        print( "Starting communication on " + self.port + " at " + str( self.baudrate ) + "." )

    '''
    Ends the communication by sending the escape sequence to the OSRBox.
    '''
    def exit( self ):

        self.ser.write( self.menu_char )
        self.ser.write( self.exit_char )

        self.ser.close()


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
        response = int( response ) + 1

        return response

    '''
    WIP
    '''
    def input( self ):

        on = True

        input_char = ''
        last_input_char = ''

        while on:

            if ( self.ser.inWaiting ):

                input_char = self.read()
                if ( input_char != False ):

                    last_input_char = input_char
                    print input_char

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
    pad.input()
