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

from unittest import mock

from oslo_config import cfg

from neutron.agent import agent_extensions_manager as ext_manager
from neutron.conf.agent import agent_extensions_manager as ext_manager_config
from neutron.tests import base


class TestAgentExtensionsManager(base.BaseTestCase):

    def setUp(self):
        super().setUp()
        mock.patch('neutron.agent.l2.extensions.qos.QosAgentExtension',
                   autospec=True).start()
        conf = cfg.CONF
        ext_manager_config.register_agent_ext_manager_opts()
        cfg.CONF.set_override('extensions', ['qos'], 'agent')
        namespace = 'neutron.agent.l2.extensions'
        self.manager = ext_manager.AgentExtensionsManager(conf, namespace)

    def _get_extension(self):
        return self.manager.extensions[0].obj

    def test_initialize(self):
        connection = object()
        self.manager.initialize(connection, 'fake_driver_type')
        ext = self._get_extension()
        ext.initialize.assert_called_once_with(connection, 'fake_driver_type')
