# Shared slow control classes and definitions

from abc import ABC, abstractmethod
from collections import namedtuple

HighLevelCommand = namedtuple('HighLevelCommand', ['command', 'args'])

# args are values given by the user as input and are strings. The
# DeviceController shall cast them to another type if needed.
# params are constant values explicitly set in the config file. YAML
# automatically casts them to their correct types.
Command = namedtuple('Command', ['device', 'command', 'args', 'params'])

class DeviceController(ABC):

    @abstractmethod
    def __init__(self, config):
        raise NotImplementedError()

    # Execute the specified command (of type Command), returning either a
    # dict containing update values or None.
    @abstractmethod
    def execute_command(self, command):
        raise NotImplementedError()
