# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import subprocess
import os
from drivers.protocol import protocol
import logging
logger = logging.getLogger('kiln')

class nvme(protocol):

    name = "NVME"
    required = ["dd", "nvme"]
    
    def get_info(self):
        dev_info = subprocess.Popen(["nvme", "id-ctrl", self.dev, "-H"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT) 
        self.info = dev_info.stdout.readlines()

    def get_log(self):
        dev_info = subprocess.Popen(["nvme", "fw-log", self.dev], stdout=subprocess.PIPE, stderr=subprocess.STDOUT) 
        self.log = dev_info.stdout.readlines()

    def get_temp(self):
        dev_info = subprocess.Popen(["nvme", "smart-log", self.dev], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in dev_info.stdout.readlines():
            logger.debug(line)
            if "temperature" in str(line):
                self.temperature = str(line).split(':')[-1]

    def get_wear(self):
        dev_info = subprocess.Popen(["nvme", "smart-log", self.dev], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in dev_info.stdout.readlines():
            logger.debug(line)
            if "percentage_used" in str(line):
                self.wearout = str(line)
            if "available_spare" in str(line):
                self.reserved = str(line)
