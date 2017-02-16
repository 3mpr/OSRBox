#!/usr/bin/env python

import OSRBoxWrapper
import serial.tools.list_ports
import keyboard
import threading
import time
import os
import yaml

def load_conf( fd = 'OSRBox.yml' ):

    stream = open( fd, 'r' )
    yaml_fd = yaml.load( stream )

    return yaml_fd['OSRBox']

class OSRBoxDriver:

    nb_keys = 5

    '''
    Class Constructor.

    Initializes a few important variables, such as COM port, baudrate and
    emulated keys.
    '''
    def __init__( self, port = False, daemon = False ):

        if( port is False ):
            self.delayed_setup  = True
        else:
            self.delayed_setup  = False
            self.pad            = OSRBoxWrapper.OSRBoxWrapper( port, 19200 )

        self.emulated_keys = {
            1 : 'a',
            2 : 'z',
            3 : 'e',
            4 : 'r',
            5 : 't'
        }

        self._term          = threading.Thread( target = self.term, name = 'term' )
        self._term.daemon   = daemon
        self._reader        = threading.Thread( target = self.reader, name = 'rx' )
        self._reader.daemon = daemon


    '''
    Destructor redifinition.
    '''
    def __del__( self ):

        self.pad.close()
        self.alive = False


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

        if self.delayed_setup:
            raise UnboundLocalError( 'Local COM Port has not been initialized yet.' )

        last_key_pressed = False

        while self.alive:

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
    def run( self ):

        if self.delayed_setup:
            raise UnboundLocalError( 'Local COM Port has not been initialized yet.' )

        self.pad.open()

        self.alive = True

        self._reader.start()
        self._term.start()

        self._reader.join()
        self._term.join()


    '''
    Ends the process.
    '''
    def stop( self ):

        self.alive = False


    '''
    Exit mini (one key!) terminal.
    '''
    def term( self ):

        while self.alive:
            exit = raw_input( 'Press Q to stop the OSRBox...' )

            if exit == 'Q':
                self.alive = False

    '''
    Seeks the first available COM port and returns it.

    @return string The port name
    '''
    @staticmethod
    def seekPort():

        print( '\nStarting port analysis...' )
        available_com = None

        while not available_com:

            time.sleep( 1 )
            available_com = serial.tools.list_ports.comports()

        return available_com[0].device


if __name__ == '__main__':

    osr_conf = load_conf( 'OSRBox.yml' )

    if( osr_conf['port'] ):

        drv = OSRBoxDriver( osr_conf['port'], True )

    else:

        port = OSRBoxDriver.seekPort()
        drv = OSRBoxDriver( port, True )

    for k in osr_conf['keys']:

        drv.bind( k, osr_conf['keys'][k] )

    drv.run()
