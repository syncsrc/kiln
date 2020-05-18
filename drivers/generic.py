# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pprint
import subprocess
import os
import time
from shutil import which
import logging
logger = logging.getLogger('kiln')

class generic:

    name = "GENERIC"
    required = []

    def __init__(self, drive):
        logger.debug("Initializing " + self.name + " driver for " + drive)
        for util in self.required:
            if which(util) is not None:
                logger.debug("found " + which(util))
            else:
                exit("Required utility program " + util + " not found")
        if os.path.exists(drive):
            self.dev = drive
        else:
            exit(self.name + " interface library couldn't find " + drive)
        self.set_parameters()


    def set_parameters(self):
        f = open("/sys/class/block/" + self.dev.split('/')[-1] + "/size", "r")
        self.max_lba = f.readline().strip()
        logger.debug("Setting maximum LBA for " + self.dev + " to " + self.max_lba)
        f.close()
        f = open("/sys/class/block/" + self.dev.split('/')[-1] + "/queue/logical_block_size", "r")
        self.size_lb = f.readline().strip()
        logger.debug("Setting logical block size for " + self.dev + " to " + self.size_lb)
        f.close()
        f = open("/sys/class/block/" + self.dev.split('/')[-1] + "/queue/physical_block_size", "r")
        self.size_pb = f.readline().strip()
        logger.debug("Setting physical block size for " + self.dev + " to " + self.size_pb)
        f.close()


    def get_info(self):
        self.info = "Drive Info Unavailable"


    def get_log(self):
        self.log = "Log Page Unavailable"


    def get_temp(self):
        self.log = "Temperature Unavailable"


    def get_wear(self):
        self.wearout = "Wear Level Unavailable"
        self.reserved = "Reserved Space Unavailable"


    def print_info(self):
        pprint.pprint(self.info)


    def print_log(self):
        print(self.log)

        
    def print_temp(self):
        print(self.temperature)


    def print_wear(self):
        print(self.wearout)
        print(self.reserved)


    def write_block(self, address, data):
        if isinstance(data, bytes):
            logger.debug("Attempting to write sector " + str(address) + " with " + str(len(data)) + " bytes of data.")
        else:
            exit("Data to be written must of the bytes type.")
        if int(address) > int(self.max_lba) or int(address) < 0:
            exit("Cannot write out-of-range address " + str(address))
        elif len(data) != int(self.size_lb):
            exit("Provided " + str(len(data)) + " bytes of input data but sector size is " + self.size_lb)
        else:
            dev_info = subprocess.Popen(["dd", "of="+self.dev, "oflag=direct", "conv=fsync", "seek="+str(address), "count=1", "bs="+self.size_lb, "status=none" ], \
                                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = dev_info.communicate(input=data)
            logger.debug(output + error)

    
    def read_block(self, address):
        logger.debug("Attempting to read sector " + str(address))
        if int(address) > int(self.max_lba) or int(address) < 0:
            exit("Cannot read out-of-range address " + str(address))
        else:
            dev_info = subprocess.Popen(["dd", "if="+self.dev, "iflag=direct", "skip="+str(address), "count=1", "bs="+self.size_lb, "status=none" ], \
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = dev_info.communicate()
            logger.debug(output)
            return output


    def write_thruput(self):
        address = 0   ## TODO: does changing this affect performance?
        bs = 2**20    ## TODO: is this a good choice?
        data_size = bs * 512 # int(self.size_pb)
        while data_size/int(self.size_lb) > int(self.max_lba):
            data_size = data_size / 2
        count = int(data_size / bs)
        tmpfile = os.path.dirname(__file__) + "/tmp.bin"
        logger.info("Filling temporary file " + tmpfile + " with " + str(data_size) + " bytes of random data.")
        f = open(tmpfile, "wb")
        f.write(os.urandom(data_size))
        f.close()
        logger.info("Writing " + str(data_size) + " bytes to " + self.dev)
        start = time.time()
        dev_info = subprocess.Popen(["dd", "if="+tmpfile, "of="+self.dev, "oflag=direct", "conv=fsync", "seek="+str(address), \
                                     "count="+str(count), "bs="+str(bs)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = dev_info.communicate()
        end = time.time()
        #logger.debug(' '.join(dev_info.args))
        logger.debug(output + error)
        logger.debug("Wrote " + str(data_size) + " bytes in " + str(end-start) + " seconds.")
        logger.debug("Estimated write speed of " + str(data_size/(end-start)) + " bytes per sec")
        return data_size/(end-start)
