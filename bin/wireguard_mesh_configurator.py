#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: WireGuard Mesh Configurator
Dev: K4YT3X
Date Created: October 10, 2018
Last Modified: October 12, 2019

Licensed under the GNU General Public License Version 3 (GNU GPL v3),
    available at: https://www.gnu.org/licenses/gpl-3.0.txt
(C) 2018-2019 K4YT3X

TODO
- Add private key input validation
- Make either Address or Alias mandatory
"""

# built-in imports
import contextlib

# third-party imports
from avalon_framework import Avalon

# local imports
from wmcshell import WMCShell


VERSION = '1.3.0'


def print_welcome():
    """ Print program name and legal information
    """
    print(f'''WireGuard Mesh Configurator {VERSION}
(C) 2018-2019 K4YT3X
Licensed under GNU GPL v3\n''')


# if the file is not being imported
if __name__ == '__main__':

    print_welcome()

    with contextlib.suppress(KeyboardInterrupt):

        # Launch main function
        WMCShell().cmdloop()

    Avalon.warning('Exiting')
