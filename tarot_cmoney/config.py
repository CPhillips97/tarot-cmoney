import os
import configparser

class Config:
    def __init__(self):
        self.__config_file: str = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.ini')
        self.__config = configparser.ConfigParser()
        self.__config.read(self.__config_file)

    @property
    def reverse_probability(self) -> float:
        return self.__config.getfloat('Tarot', 'reverse_probability')

    @reverse_probability.setter
    def reverse_probability(self, value: float):
        if value < 0 or value > 1:
            raise ValueError("Reverse probability must be between 0 and 1")
        self.__write_to_config('Tarot', 'reverse_probability', value)

    def __write_to_config(self, category, variable, value):
        valstr = str(value)
        self.__config.set(category, variable, valstr)
        with open(self.__config_file, 'w') as configfile:
            self.__config.write(configfile)

    @property
    def chatgpt_write_using_stream(self):
        return self.__config.getboolean('ChatGPT', 'write_using_stream')

    @chatgpt_write_using_stream.setter
    def chatgpt_write_using_stream(self, value: bool):
        self.__config.set('ChatGPT', 'write_using_stream', str(value))