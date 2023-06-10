# Copyright 2015 Cisco Systems, Inc.
# All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import mock
from oslo_config import cfg

from networking_cisco.plugins.ml2.drivers.cisco.ucsm import (config as
    ucsm_config)
from networking_cisco.plugins.ml2.drivers.cisco.ucsm import constants as const

from neutron.common import config as neutron_config
from neutron.plugins.ml2 import config as ml2_config

from neutron.tests import base

UCSM_IP_ADDRESS_1 = '1.1.1.1'
UCSM_USERNAME_1 = 'username1'
UCSM_PASSWORD_1 = 'password1'
UCSM_VIRTIO_ETH_PORTS_1 = ['eth0, eth1']

UCSM_IP_ADDRESS_2 = '2.2.2.2'
UCSM_USERNAME_2 = 'username2'
UCSM_PASSWORD_2 = 'password2'
UCSM_VIRTIO_ETH_PORTS_2 = ['eth2, eth3']

UCSM_PHY_NETS = ['test_physnet']


class ConfigMixin(object):

    """Mock config for UCSM driver."""

    mocked_parser = None

    def set_up_mocks(self):
        # Mock the configuration file

        args = ['--config-file', base.etcdir('neutron.conf')]
        neutron_config.init(args=args)

        # Configure the ML2 mechanism drivers and network types
        ml2_opts = {
            'mechanism_drivers': ['cisco_ucsm'],
            'tenant_network_types': ['vlan'],
        }
        for opt, val in ml2_opts.items():
            ml2_config.cfg.CONF.set_override(opt, val, 'ml2')

        # Configure the Cisco UCS Manager mechanism driver
        ucsm_test_config = {
            'ml2_cisco_ucsm_ip: 1.1.1.1': {
                'ucsm_username': [UCSM_USERNAME_1],
                'ucsm_password': [UCSM_PASSWORD_1],
                'ucsm_virtio_eth_ports': UCSM_VIRTIO_ETH_PORTS_1,
                'vnic_template_list': ['test-physnet:org-root:Test-VNIC'],
            },
            'ml2_cisco_ucsm_ip: 2.2.2.2': {
                'ucsm_username': [UCSM_USERNAME_2],
                'ucsm_password': [UCSM_PASSWORD_2],
                'ucsm_virtio_eth_ports': UCSM_VIRTIO_ETH_PORTS_2,
                'vnic_template_list': ['physnet2:org-root/org-Test-Sub:Test']
            },
        }
        expected_ucsm_dict = {
            '1.1.1.1': [UCSM_PASSWORD_1, UCSM_USERNAME_1],
            '2.2.2.2': [UCSM_PASSWORD_2, UCSM_USERNAME_2],
        }

        expected_ucsm_port_dict = {
            '1.1.1.1': [const.ETH_PREFIX + 'eth0', const.ETH_PREFIX + 'eth1'],
            '2.2.2.2': [const.ETH_PREFIX + 'eth2', const.ETH_PREFIX + 'eth3'],
        }

        expected_vnic_template_dict = {
            ('1.1.1.1', 'test-physnet'): ('org-root', 'Test-VNIC'),
            ('2.2.2.2', 'physnet2'): ('org-root/org-Test-Sub', 'Test'),
        }

        self.mocked_parser = mock.patch.object(cfg,
            'MultiConfigParser').start()
        self.mocked_parser.return_value.read.return_value = [ucsm_test_config]
        self.mocked_parser.return_value.parsed = [ucsm_test_config]
        ucsm_config.UcsmConfig()
        self.assertEqual(expected_ucsm_dict,
                         ucsm_config.UcsmConfig.ucsm_dict)
        self.assertEqual(expected_ucsm_port_dict,
                         ucsm_config.UcsmConfig.ucsm_port_dict)
        self.assertEqual(expected_vnic_template_dict,
                         ucsm_config.UcsmConfig.vnic_template_dict)
