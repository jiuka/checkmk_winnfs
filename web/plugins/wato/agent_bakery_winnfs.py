# -*- encoding: utf-8; py-indent-offset: 4 -*-
#
# Windows NFS checks
#
# Copyright (C) 2020  Marius Rieder <marius.rieder@scs.ch>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from cmk.gui.i18n import _
from cmk.gui.valuespec import (
    DropdownChoice,
)
from cmk.gui.plugins.wato import (
    HostRulespec,
    rulespec_registry,
)

try:
    from cmk.gui.cee.plugins.wato.agent_bakery import (
        RulespecGroupMonitoringAgentsWindowsAgent
    )
except Exception:
    RulespecGroupMonitoringAgentsWindowsAgent = None


def _valuespec_agent_config_winnfs():
    return DropdownChoice(
        title=_('Windows NFS Server'),
        help=_('This will deploy the agent plugin <tt>winnfs</tt> '
               'for checking Windows NFS Server and Shares.'),
        choices=[
            (True, _('Deploy Windows NFS Server plugin')),
            (None, _('Do not deploy Windows NFS Server plugin')),
        ],
    )


if RulespecGroupMonitoringAgentsWindowsAgent is not None:
    rulespec_registry.register(
        HostRulespec(
            group=RulespecGroupMonitoringAgentsWindowsAgent,
            name='agent_config:winnfs',
            valuespec=_valuespec_agent_config_winnfs,
        ))
