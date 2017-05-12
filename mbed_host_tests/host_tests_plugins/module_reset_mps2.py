"""
mbed SDK
Copyright (c) 2011-2015 ARM Limited

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Author: Przemyslaw Wirkus <Przemyslaw.Wirkus@arm.com>
"""

import os
import time

from host_test_plugins import HostTestPluginBase

# Note: This plugin is not fully functional, needs improvements

class HostTestPluginResetMethod_MPS2(HostTestPluginBase):
    """! Plugin used to reset ARM_MPS2 platform

    @details Supports:
             reboot.txt   - startup from standby state, reboots when in run mode.
             shutdown.txt - shutdown from run mode.
             reset.txt    - reset FPGA during run mode.
    """

    # Plugin interface
    name = 'HostTestPluginResetMethod_MPS2'
    type = 'ResetMethod'
    capabilities = ['reboot.txt', 'shutdown.txt', 'reset.txt']
    required_parameters = ['disk']

    def __init__(self):
        """ ctor
        """
        HostTestPluginBase.__init__(self)

    def touch_file(self, path):
        """ Touch file and set timestamp to items
        """
        with open(path, 'a'):
            os.utime(path, None)

    def setup(self, *args, **kwargs):
        """ Prepare / configure plugin to work.
            This method can receive plugin specific parameters by kwargs and
            ignore other parameters which may affect other plugins.
        """
        return True

    def execute(self, capability, *args, **kwargs):
        """! Executes capability by name

        @param capability Capability name
        @param args Additional arguments
        @param kwargs Additional arguments

        @details Each capability e.g. may directly just call some command line program or execute building pythonic function

        @return Capability call return value
        """
        result = False

        disk =  kwargs.get('disk', None)
        target_id = kwargs.get('target_id', None)
        pooling_timeout = kwargs.get('polling_timeout', 60)
        if self.check_parameters(capability, *args, **kwargs) is True:

            if capability == 'reboot.txt':
                reboot_file_path = os.path.join(disk,capability)
                reboot_fh = open(reboot_file_path,"w")
                reboot_fh.close()
                time.sleep(3) # sufficient delay for device to boot up
                mount_res, destination_disk = self.check_mount_point_ready(disk, target_id=target_id,timeout=pooling_timeout)
            elif capability == 'shutdown.txt':
                # TODO: Implement touch file for shutdown
                pass

            elif capability == 'reset.txt':
                # TODO: Implement touch file for reset
                pass

        return result

def load_plugin():
    """ Returns plugin available in this module
    """
    return HostTestPluginResetMethod_MPS2()
