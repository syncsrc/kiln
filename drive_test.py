# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from drivers import select
import logging
logger = logging.getLogger('kiln')

class drive_test:

    description = "Default test description."
    
    def __init__(self, drive=None):
        if drive != None:
            self.dev = select.select_driver(drive)

    def __main__(self):
        print("Chillin\'.")
