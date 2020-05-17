#!/usr/bin/python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

## KILN info
ver = "0.1.0"
info = """
Framework for SSD and HDD qualification testing.
"""
epi = """
Running these tests will destroy all the data on any drive being tested. It may even permenantly damage the drive. Use with caution.
"""

import argparse
import glob
import importlib
import logging

## Setup debug messages
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('kiln')

## Get command-line options
parser = argparse.ArgumentParser(description=info, epilog=epi)
parser.add_argument('-v', '--version', action='version', version=ver)
parser.add_argument('-d', '--dev', dest='dev', required=True,
                    help='Block device to test.')
parser.add_argument('-l', '--list', dest='list_mods', action='store_true', default=False,
                    help='Show list of available modules and exit.')
group = parser.add_mutually_exclusive_group()
group.add_argument('-a', '--all', dest='all_mods', action='store_true', default=False,
                    help='Run all available modules.')
group.add_argument('-m', '--module', dest='modules', nargs='*',
                    help='Run specified module.')
parser.add_argument('-i', '--iterations', dest='iterations', type=int, default=1,
                    help='Number of times to run a module. Cannot be used if more than one module is specified.')
opts = parser.parse_args()

# get working list of modules
#   if "all" or "list" option is selected, get all the available modules
#   else use modules specified via -m command line option
modules = []
if opts.list_mods or opts.all_mods:
    logger.debug("Searching for modules in tests/ folder.")
    mod_files = glob.glob('tests/*.py')
    for mod in mod_files:
        modules.append(mod.split('/')[-1].rstrip(".py"))
elif len(opts.modules) > 0:
    modules = opts.modules
else:
    exit("No modules specified, nothing to do.")
logger.info("Using the following modules: " + ", ".join(modules))

# allowing this seemed like a bad idea.
if len(modules) > 1 and opts.iterations > 1:
    logger.warn("Can only run multiple iterations on a single module. Reducing iteration count to 1.")
    opts.iterations = 1

# Import each module in the list
# TODO: filter modules based on which type of drives are supported?
for mod in modules:
    test_module = importlib.import_module("." + mod, "tests")

    # if --list was selected print module info, but don't load the driver or run the test
    if opts.list_mods:
        print('{0: <15}{1}'.format(mod, test_module.run_test.description))

    # otherwise proceed with testing
    else:
        logger.debug("Running " + mod + " test module on " + opts.dev)
        test_case = test_module.run_test(opts.dev)
        for i in range(opts.iterations):
            test_case.__main__()
