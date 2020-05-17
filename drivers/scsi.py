# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import subprocess
import os
from drivers.protocol import protocol
import logging
logger = logging.getLogger('kiln')

class scsi(protocol):

    name = "SCSI"
    required = ["dd", "sg_inq", "sg_format", "sg_logs"]

    def get_info(self):
        dev_info = subprocess.Popen(["sg_inq", self.dev], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.info = dev_info.stdout.readlines()


    def get_temp(self):
        dev_info = subprocess.Popen(["sg_logs", "-p", "0x0d", self.dev], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in dev_info.stdout.readlines():
            logger.debug(line)
            if "Current temperature" in str(line):
                self.temperature = str(line).split('=')[-1]
