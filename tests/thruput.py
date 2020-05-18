# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from drivers import select
from drive_test import drive_test
import logging
logger = logging.getLogger('kiln')

class run_test(drive_test):

    description = "Test drive write thruput."
    
    def __main__(self):
        thruput = self.dev.write_thruput() / 1000000
        print("Estimated write thruput for", self.dev.dev, "is", '{:.2f}'.format(thruput), "MB/s")
