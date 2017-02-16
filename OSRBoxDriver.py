#!/usr/bin/env python

import OSRBoxWrapper
import keyboard
import threading
import time

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
    def __init__ ( self, port, daemon = False ):

        self.pad = OSRBoxWrapper.OSRBoxWrapper( port, 19200 )

        self.emulated_keys = {
            1 : 'a',
            2 : 'z',
            3 : 'e',
            4 : 'r',
            5 : 't'
        }

        self._term = threading.Thread( target = self.term, name = 'term' )
        self._term.daemon = daemon
        self._reader = threading.Thread( target = self.reader, name = 'rx' )
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
    accordingly.
    '''
    def reader( self ):

        last_key_pressed = False

        while self.alive:
            key_pressed = self.pad.read()

            if( key_pressed is not False ):

                for key in self.emulated_keys:
                    if key_pressed == key and key_pressed != last_key_pressed:
                        last_key_pressed = key_pressed
                        self.current_key = key_pressed
                        keyboard.press( self.emulated_keys[key] )

            elif last_key_pressed:

                keyboard.release( self.emulated_keys[last_key_pressed] )
                last_key_pressed = False

            # time.sleep( 0.1 )


    '''
    Runs two thread, one is a miniterm and let the user ends the program,
    the other keeps updated the current active key.
    '''
    def run( self ):

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
    Exit hook.
    '''
    def term( self ):

        while self.alive:
            exit = raw_input( 'Press Q to stop the OSRBox...' )

            if exit == 'Q':
                self.alive = False



if __name__=='__main__':

    drv = OSRBoxDriver( 'COM3', True )

    key_conf = load_conf( 'OSRBox.yml' )
    for k in key_conf:
        drv.bind( k, key_conf[k] )

    drv.run()
