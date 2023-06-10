# Copyright 2012 Cloudbase Solutions Srl
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from oslo_log import log as oslo_logging

from cloudbaseinit.osutils import factory as osutils_factory
from cloudbaseinit.plugins.common import base
from cloudbaseinit.utils import hostname

LOG = oslo_logging.getLogger(__name__)


class SetHostNamePlugin(base.BasePlugin):
    def execute(self, service, shared_data):
        osutils = osutils_factory.get_os_utils()
        metadata_host_name = service.get_host_name()

        if not metadata_host_name:
            LOG.debug('Hostname not found in metadata')
            return base.PLUGIN_EXECUTION_DONE, False

        (_, reboot_required) = hostname.set_hostname(
            osutils, metadata_host_name)

        return base.PLUGIN_EXECUTION_DONE, reboot_required
