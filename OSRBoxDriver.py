#!/usr/bin/env python

import OSRBoxWrapper
import serial.tools.list_ports
import keyboard
import threading
import time
import os
import yaml



class OSRBoxDriver:

    nb_keys = 5

    '''
    Class Constructor.

    Initializes a few important variables, such as COM port, baudrate and
    emulated keys.
    '''
    def __init__( self, port = False ):

        self.port = None
        self.emulated_keys = { 1 : 'a', 2 : 'z', 3 : 'e', 4 : 'r', 5 : 't' }

        self.osr_conf = self.load_conf( 'OSRBox.yml' )
        self.delayed_setup = True

        if port:

            self.delayed_setup  = False
            self.port           = port

        elif port is False and self.osr_conf['port']:

            self.port           = self.osr_conf['port']

        #self.pad            = OSRBoxWrapper.OSRBoxWrapper( port, 19200 )


    '''
    Destructor redifinition.
    '''
    def __del__( self ):

        self.reader_alive   = False
        self.alive          = False

        self.pad.close()


    '''
    Binds one of the OSRBox numerical keys to emulate a given keyboard key.

    @param int      nb  The pressed OSRBox key
    @param string   key The emulated key description
    '''
    def bind( self, nb, key):

        if ( nb > self.nb_keys ):
            raise ValueError( 'There is only 5 keys on the OSRBox!' )

        self.emulated_keys[nb] = key


    '''
    Keeps track of the current OSRBox pressed key and emulate keyboard keys
    according to the <emulated_keys> dictionnary.
    '''
    def reader( self ):

        last_key_pressed = False

        while self.reader_alive:

            key_pressed = self.pad.read()

            if key_pressed:

                for key in self.emulated_keys:
                    if key_pressed == key and key_pressed != last_key_pressed:
                        last_key_pressed = key_pressed
                        keyboard.press( self.emulated_keys[key] )

            elif last_key_pressed:

                keyboard.release( self.emulated_keys[last_key_pressed] )
                last_key_pressed = False


    '''
    Runs two thread, one is a MINI(!)term and let the user ends the program,
    the other keeps updated the current active key.
    '''
    def bootstrap( self ):

        if self.delayed_setup:

            self.conf = self.load_conf()

            if not self.port:

                self.port = OSRBoxDriver.seek_port()

        self.pad = OSRBoxWrapper.OSRBoxWrapper( self.port, 19200 )

        self.osr_conf = self.load_conf( 'OSRBox.yml' )
        for k in self.osr_conf['keys']:

            self.bind( k, self.osr_conf['keys'][k] )

        self.pad.open()

        self.reader_alive = True
        self._reader    = threading.Thread( target = self.reader, name = 'rx' )
        self._reader.start()
        self._reader.join()

        self._term      = threading.Thread( target = self.term, name = 'term' )
        self._term.start()


    '''
    '''
    def run( self ):

        self.alive = True
        self.reader_alive = True

        while self.alive:

            try:

                self.bootstrap()

            except serial.serialutil.SerialException, TypeError:

                self.reader_alive = False
                self.port = None
                time.sleep( 1 )


    '''
    Ends the process.
    '''
    def stop( self ):
        self.reader_alive   = False
        self.alive          = False


    '''
    Exit mini (one key!) terminal.
    '''
    def term( self ):

        while self.reader_alive:

            exit = raw_input( 'Press Q to stop the OSRBox...' )

            if exit == 'Q':

                self.reader_alive = False
                self.alive = False


    '''
    '''
    def load_conf( self, fd = 'OSRBox.yml' ):

        stream = open( fd, 'r' )
        yaml_fd = yaml.load( stream )
        stream.close()

        return yaml_fd['OSRBox']

    '''
    Seeks the first available COM port and returns it.

    @return string The port name
    '''
    @staticmethod
    def seek_port():

        print( '\nStarting port analysis...' )
        available_com = None

        while not available_com:

            time.sleep( 1 )
            available_com = serial.tools.list_ports.comports()

        return available_com[0].device


if __name__ == '__main__':

    drv = OSRBoxDriver()
    drv.run()
