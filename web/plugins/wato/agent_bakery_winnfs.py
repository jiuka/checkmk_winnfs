#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

register_rule(
    "agents/" + _("Agent Plugins"),
    "agent_config:winnfssrv",
    Alternative(
        title = _("Windows NFS Server"),
        help = _("This will deploy the agent plugin <tt>winnfs</tt> "
                 "for checking Windows NFS Server and Shares.")
        style = "dropdown",
        elements = [
	    FixedValue(True, title _("Deploy the Windows NFS Server plugin"), totext = _("(enabled)") ),
            FixedValue(None, title = _("Do not deploy the SSL certificates plugin"), totext = _("(disabled)") ),
        ]
    ),
)
