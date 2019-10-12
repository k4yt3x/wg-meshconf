#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: Utilities
Dev: K4YT3X
Date Created: October 11, 2019
Last Modified: October 12, 2019
"""

# built-in imports
import subprocess


class Utilities:
    """ Useful utilities

    This class contains a number of utility tools.
    """

    @staticmethod
    def execute(command: list, input_value='') -> list:
        """ execute command and returns output

        Arguments:
            command {list} -- command list to execute

        Keyword Arguments:
            input_value {str} -- value to pass into stdin (default: {''})

        Returns:
            list -- list of command output
        """
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        output = process.communicate(input=input_value)[0]
        return output.decode().replace('\n', '')
