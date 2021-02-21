#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#
# Windows NFS check
#
# Copyright (C) 2020-2021  Marius Rieder <marius.rieder@scs.ch>
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
    Dictionary,
    DropdownChoice,
    TextAscii,
)
from cmk.gui.plugins.wato import (
    CheckParameterRulespecWithItem,
    rulespec_registry,
    RulespecGroupCheckParametersStorage,
)


def AuthState(**kwargs):
    return DropdownChoice(
        choices=[
            ('discoverd', _('Is discoverd')),
            ('required', _('Is required')),
            ('forbidden', _('Is forbidden')),
            ('ignored', _('Is ignored')),
        ],
        default_value='discoverd',
        **kwargs)


def _parameter_valuespec_winnfsshare():
    return Dictionary(
        help=_('Ensure the Windows Server for NFS Share is in the desired state.'),
        required_keys=['Authentication'],
        elements=[
            (
                'Online',
                DropdownChoice(
                    title=_('Share Status'),
                    choices=[
                        ('Online', _('Online')),
                        ('Offline', _('Offline')),
                        ('ignored', _('Is ignored')),
                    ],
                    default_value='Online',
                )
            ),
            (
                'Clustered',
                DropdownChoice(
                    title=_('Availability'),
                    choices=[
                        ('True', _('Clustered')),
                        ('False', _('Standard (not clustered)')),
                        ('ignored', _('Is ignored')),
                    ],
                    default_value='ignored',
                )
            ),
            (
                'Authentication',
                Dictionary(
                    title=_('Authentication'),
                    elements=[
                        ('sys', AuthState(title=_('System Authentication'))),
                        ('Krb5', AuthState(title=_('Kerberos Authentication'))),
                        ('Krb5i', AuthState(title=_('Kerberos Authentication w/ integrity'))),
                        ('Krb5p', AuthState(title=_('Kerberos Authentication w/ privacy'))),
                    ]
                )
            ),
            (
                'AnonymousAccess',
                DropdownChoice(
                    title=_('Anonymous Access'),
                    choices=[
                        ('discoverd', _('Is discoverd')),
                        ('True', _('Allowed')),
                        ('False', _('Forbidden')),
                        ('ignored', _('Is ignored')),
                    ],
                    default_value='ignored',
                )
            ),
            (
                'UnmappedUserAccess',
                DropdownChoice(
                    title=_('Unmapped User Access'),
                    choices=[
                        ('discoverd', _('Is discoverd')),
                        ('True', _('Allowed')),
                        ('False', _('Forbidden')),
                        ('ignored', _('Is ignored')),
                    ],
                    default_value='ignored',
                )
            ),
        ],
    )


def _item_spec_winnfsshare():
    return TextAscii(
        title=_('NFS Share name'),
    )


rulespec_registry.register(
    CheckParameterRulespecWithItem(
        check_group_name='winnfsshare',
        group=RulespecGroupCheckParametersStorage,
        item_spec=_item_spec_winnfsshare,
        parameter_valuespec=_parameter_valuespec_winnfsshare,
        title=lambda: _('Windows NFS Share'),
    ))
