# Slow control for fan

# Telnet protocol follows example at http://www.pythonforbeginners.com/code-snippets-source-code/python-using-telnet
# Another useful example: https://docs.python.org/2/library/telnetlib.html
# protocol provided to FAN constructor should be 'serial' or (default) 'telnet'
# Telnet supported added May 27 2018 by Justin Vandenbroucke
# Modified for DeviceController class and Python 3 Aug 14 2018 by Ari Brill

import socket
import telnetlib
import time

import serial

from slow_control_classes import *

SLEEP_SECS = 3

class FanController(DeviceController):

    def __init__(self, config):
        self._telnet_settings = {'host': None, 'port': None, 'timeout': None}
        for setting in self._telnet_settings:
            try:
                self._telnet_settings[setting] = config[setting]
            except KeyError as e:
                raise ConfigurationError(setting) from e
        self._ser = None

    def _open_connection(self):
        if self._ser is not None:
            raise CommandSequenceError("Connection to fan is already open, "
                    "close before reopening.")
        try:
            self._ser = telnetlib.Telnet(
                    self._telnet_settings['host'],
                    self._telnet_settings['port'],
                    self._telnet_settings['timeout'])
        except OSError as e:
            raise CommunicationError() from e

    def _close_connection(self):
        if self._ser is not None:
            self._ser.close()
        self._ser = None

    def _send_cmd(self, cmd):
        try:
            self._ser.write("{}\n".format(cmd).encode('ascii'))
            time.sleep(0.5)
            val = self._ser.read_until('\n'.encode('ascii'), timeout=1)
            val = val.decode('ascii')[:6] # strip non-numerical output
            return val
        except OSError as e:
            self._ser = None
            raise CommunicationError() from e

    def execute_command(self, command):
        cmd = command.command
        update = None
        if cmd == "open_connection":
            self._open_connection()
        elif self._ser is None:
            raise CommunicationError()
        elif cmd == "close_connection":
            self._close_connection()
        elif cmd == "check_connection":
            update = ('connected', self._ser is not None)
        elif cmd == "turn_on":
            self._send_cmd("PWR ON")
            time.sleep(SLEEP_SECS)
        elif cmd == "turn_off":
            self._send_cmd("PWR OFF")
            time.sleep(SLEEP_SECS)
        elif cmd == "read_voltage":
            voltage = self._send_cmd("VREAD")
            update = ('voltage', voltage)
        elif cmd == "read_current":
            current = self._send_cmd("IREAD")
            update = ('current', current)
        else:
            raise CommandNameError
        return update
