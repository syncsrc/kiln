# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

## EDIT THESE FOR YOUR SYSTEM
blocklist = ['sdf', 'sdg', 'sdh', 'sdi']

from drivers.sata import sata
from drivers.scsi import scsi
from drivers.nvme import nvme

import os
import glob
import logging
logger = logging.getLogger('kiln')


def select_driver(device):
    logging.info("Testing of the following drives will not be allowed: " + ", ".join(blocklist))

    ## Make sure the device specified at the command line is valid
    if os.path.exists(device):
        if 'dev' in device.split('/'):
            dev = device.split('/')[-1]
            if dev in blocklist:
                exit("I'm sorry, Dave. I'm afraid I can't do that.")
            else:
                logging.info("Using " + device)
        else:
            exit("this doesn't look like a valid device")
    else:
        exit("can't find device. " + device + " is not a valid path.")

    ## Many NVME commands require a namespace, easier to require it and
    ## remove from commands that don't allow it.
    if os.path.exists("/sys/class/nvme/" + dev):
        files=glob.glob("/sys/class/block/nvme*")
        print("Must provide a namespace for NVME drives. Try one of", [ns.split('/')[-1] for ns in files])
        exit()

    ## Check that sysfs entry for the block device exists
    elif os.path.exists("/sys/class/block/" + dev):

        # Figure out what type of drive was specified
        subsys = os.readlink("/sys/class/block/" + dev +"/device/subsystem").split('/')[-1]

        # Lots of things use the SCSI subsystem, so look deeper
        if subsys == "scsi":
            f = open("/sys/class/block/" + dev + "/device/vendor", "r")
            scsi_type = f.readline().strip()
            f.close()
            f = open("/sys/class/block/" + dev + "/device/scsi_level", "r")
            scsi_level = f.readline().strip()
            f.close()
            logging.debug("Vendor: " + scsi_type + " and SCSI level: " + scsi_level)
            if scsi_type == "ATA":
                if scsi_level == "6":
                    return sata(device)
                else:
                    exit("Inconsistancy in SATA check.")
            else:
                return scsi(device)

        # NVME drive
        elif subsys == "nvme":
            return nvme(device)

        # Other types are unsupported
        else:
            exit("Kiln does not currently support " + subsys + " drives.")

    # D'oh
    else:
        exit("something went wrong, couldn't find /sys/class/block/ entries for " + device)
