#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

from cmk.gui.i18n import _
from cmk.gui.valuespec import (
    DropdownChoice,
)
from cmk.gui.plugins.wato import (
    HostRulespec,
    rulespec_registry,
)

try:
    from cmk.gui.cee.plugins.wato.agent_bakery import RulespecGroupMonitoringAgentsWindowsAgent
except:
    from cmk.gui.plugins.wato import RulespecGroupCheckParametersStorage as RulespecGroupMonitoringAgentsWindowsAgent

def _valuespec_agent_config_winnfs():
    return DropdownChoice(
        title=_("Windows NFS Server"),
        help=_("This will deploy the agent plugin <tt>winnfs</tt> "
               "for checking Windows NFS Server and Shares."),
        choices=[
            (True, _("Deploy Windows NFS Server plugin")),
            (None, _("Do not deploy Windows NFS Server plugin")),
        ],
    )

rulespec_registry.register(
    HostRulespec(
        group=RulespecGroupMonitoringAgentsWindowsAgent,
        name="agent_config:winnfs",
        valuespec=_valuespec_agent_config_winnfs,
    ))
