#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-


from cmk.gui.i18n import _
from cmk.gui.valuespec import (
    Dictionary,
    DropdownChoice,
    Tuple,
)
from cmk.gui.plugins.wato import (
    CheckParameterRulespecWithoutItem,
    rulespec_registry,
    RulespecGroupCheckParametersStorage,
)

def _parameter_valuespec_winnfssrv():
    return Dictionary(
        help=_("Ensure the Windows Server for NFS is in the desired state."),
        elements=[
            ("State",
             DropdownChoice(
                 title=_("Server State"),
                 choices=[
                     ('Running', _("Running")),
                     ('Stopped', _("Stopped")),
                     ('ignored', _("Is ignored")),
                 ],
                 default_value="Running",
             )),
            ("EnableNFSV2",
             DropdownChoice(
                 title=_("NFSv2"),
                 choices=[
                     (True, _("Needs to be enabled")),
                     (False, _("Needs to be disabled")),
                     ('ignored', _("Is ignored")),
                 ],
                 default_value=True,
             )),
            ("EnableNFSV3",
             DropdownChoice(
                 title=_("NFSv3"),
                 choices=[
                     (True, _("Needs to be enabled")),
                     (False, _("Needs to be disabled")),
                     ('ignored', _("Is ignored")),
                 ],
                 default_value=True,
             )),
            ("EnableNFSV4",
             DropdownChoice(
                 title=_("NFSv4"),
                 choices=[
                     (True, _("Needs to be enabled")),
                     (False, _("Needs to be disabled")),
                     ('ignored', _("Is ignored")),
                 ],
                 default_value=True,
             )),
            ("MountProtocol",
             DropdownChoice(
                 title=_("Mount Protocol"),
                 choices=[
                     ('TCP, UDP', _("TCP and UDP")),
                     ('TCP', _("TCP only")),
                     ('UDP', _("UDP only")),
                 ],
             )),
            ("NfsProtocol",
             DropdownChoice(
                 title=_("Nfs Protocol"),
                 choices=[
                     ('TCP, UDP', _("TCP and UDP")),
                     ('TCP', _("TCP only")),
                     ('UDP', _("UDP only")),
                 ],
             )),
            ("NisProtocol",
             DropdownChoice(
                 title=_("Nis Protocol"),
                 choices=[
                     ('TCP, UDP', _("TCP and UDP")),
                     ('TCP', _("TCP only")),
                     ('UDP', _("UDP only")),
                 ],
             )),
            ("NlmProtocol",
             DropdownChoice(
                 title=_("Nlm Protocol"),
                 choices=[
                     ('TCP, UDP', _("TCP and UDP")),
                     ('TCP', _("TCP only")),
                     ('UDP', _("UDP only")),
                 ],
             )),
            ("NsmProtocol",
             DropdownChoice(
                 title=_("Nsm Protocol"),
                 choices=[
                     ('TCP, UDP', _("TCP and UDP")),
                     ('TCP', _("TCP only")),
                     ('UDP', _("UDP only")),
                 ],
             )),
            ("PortmapProtocol",
             DropdownChoice(
                 title=_("Portmap Protocol"),
                 choices=[
                     ('TCP, UDP', _("TCP and UDP")),
                     ('TCP', _("TCP only")),
                     ('UDP', _("UDP only")),
                 ],
             )),
            ("MapServerProtocol",
             DropdownChoice(
                 title=_("MapServer Protocol"),
                 choices=[
                     ('TCP, UDP', _("TCP and UDP")),
                     ('TCP', _("TCP only")),
                     ('UDP', _("UDP only")),
                 ],
             )),
        ],
    )

rulespec_registry.register(
    CheckParameterRulespecWithoutItem(
        check_group_name="winnfssrv",
        group=RulespecGroupCheckParametersStorage,
        parameter_valuespec=_parameter_valuespec_winnfssrv,
        title=lambda: _("Windows NFS Server"),
    ))
