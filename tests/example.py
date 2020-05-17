# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from drivers import select
from drive_test import drive_test
import logging
logger = logging.getLogger('kiln')

# all test scripts must contain a run_test(drive_test) class
class run_test(drive_test):

    # __init__() is defined in the parent class, do not reimplement

    # A description of the test is required.
    description = "Example test. Displays drive information."
    
    # Main must be defined, this is executed by Kiln as the test routine.
    def __main__(self):
        self.dev.get_info()
        self.dev.print_info()
