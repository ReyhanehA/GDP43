# (C) Copyright 2016 Hewlett Packard Enterprise Development Company LP
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import subprocess

from freezer.tests.freezer_tempest_plugin.tests.api import base
from freezer import __version__ as FREEZER_VERSION
from tempest import test


class TestFreezerVersion(base.BaseFreezerTest):

    @test.attr(type="gate")
    def test_version(self):

        version = subprocess.check_output(['freezer-agent', '--version'],
                                          stderr=subprocess.STDOUT)
        self.assertEqual(FREEZER_VERSION, version.strip())
