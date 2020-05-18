# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import subprocess
import os
from drivers.generic import generic
import logging
logger = logging.getLogger('kiln')

class sata(generic):

    name = "SATA"
    required = ["dd", "smartctl", "hdparm"]

    def get_info(self):
        dev_info = subprocess.Popen(["hdparm", "-i", self.dev], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.info = dev_info.stdout.readlines()

    def get_temp(self):
        dev_info = subprocess.Popen(["smartctl", "-A", self.dev], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in dev_info.stdout.readlines():
            logger.debug(line)
            if "Temperature_Internal" in str(line):
                self.temperature = str(line).split(' ')[-1]

    def get_wear(self):
        dev_info = subprocess.Popen(["smartctl", "-A", self.dev], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in dev_info.stdout.readlines():
            logger.debug(line)
            if ("Media_Wearout_Indicator" in str(line)) or ("Wear_Leveling_Count" in str(line)):
                self.wearout = str(line)
            elif "Available_Reservd_Space" in str(line):
                self.reserved = str(line)
