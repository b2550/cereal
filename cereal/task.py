import threading
import time

import serial

from cereal import clog, slog


class CerealTask:
    def __init__(self):
        """
        Cereal's Device Management, Serial Connection Management, and Listener Thread Management
        """
        self.device = None  # Serial Connection Object
        self.device_name = None  # Name of Serial Device
        self.serial_thread = None  # Listener Thread

    def stop(self):
        """
        Stop Listener Thread and Close Serial Connection
        """
        if self.serial_thread is not None:
            # Stop listener thread
            self.serial_thread.update = False
            self.serial_thread.join()
            self.serial_thread = None
            # Close connection
            self.device.close()
            self.device = None
            self.device_name = None
            clog("Serial disconnected")

    def set_device(self, name):
        """
        Start listening to a serial device

        :param name: (string) Serial Device Name
        """
        if self.device is not None:
            # Close existing connection
            self.stop()
        if name != '':
            try:
                # Try to create new connection and thread
                self.device = serial.Serial(name, 9600, timeout=5)
                self.device_name = name
                self.serial_thread = threading.Thread(target=self.loop)
                self.serial_thread.start()
                clog("Input device set to " + name)
            except:
                clog("Device " + name + " was not found or could not be opened")

    def exit(self):
        """
        Exit Handler.

        Must be called when application exits or else:
            - Serial connection may be left open/busy.
            - Listener Thread will remain active but not modifiable from GUI
            - Listener Thread will have to be manually terminated

        Call when application closes and/or with atexit
        """
        print("Exiting...")
        try:
            self.device.close()
            self.serial_thread.update = False
            self.serial_thread.join()
        except:
            print("Exit experienced an error. Most likely no device was set.")
        time.sleep(1)

    def loop(self):
        """
        Listener Thread

        WARNING: Do not run directly. Only run as thread.

        Listens to messages from active Serial Device

        Attempts to reconnect when device connection is lost
        """
        assert threading.current_thread() is not threading.main_thread()  # Prevent from being run in main thread
        t = threading.currentThread()  # Get current thread

        # Listener loop
        while getattr(t, "update", True):
            try:
                # Try to read current line from serial connection
                msg = self.device.readline()
                # Log decoded message
                slog(msg[0:-2].decode('utf-8'))
            except:
                # Check that the connection hasn't been canceled
                if getattr(t, "update", False):
                    break
                clog("Device connection lost. Retrying in 5 seconds...")
                time.sleep(5)  # Wait 5 seconds
                # Check the connection hasn't been canceled again
                if getattr(t, "update", False):
                    break
                try:
                    # Attempt to reconnect
                    self.device = serial.Serial(self.device_name, 9600, timeout=5)
                    clog("Retry Success")
                except:
                    clog("Retry failed")
