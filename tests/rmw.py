# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from drivers import select
from drive_test import drive_test
import logging
logger = logging.getLogger('kiln')

class run_test(drive_test):

    description = "Data read-modify-write."
    
    def __main__(self):
        address = 100
        data = self.dev.read_block(address)
        self.dev.write_block(address, data[0:510]+bytes([255,255]))
        self.dev.read_block(address)
