# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from drivers import select
from drive_test import drive_test
import logging
logger = logging.getLogger('kiln')

class run_test(drive_test):

    description = "Displays SSD wear level."
    
    def __main__(self):
        self.dev.get_wear()
        self.dev.print_wear()
