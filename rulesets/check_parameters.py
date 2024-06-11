#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#
# Windows NFS check
#
# Copyright (C) 2020-2024  Marius Rieder <marius.rieder@scs.ch>
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


from cmk.rulesets.v1 import Title, Help
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    List,
    SingleChoice,
    SingleChoiceElement,
    String,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, Topic, HostCondition, HostAndItemCondition


def AuthState(**kwargs):
    return SingleChoice(
        **kwargs,
        elements=[
            SingleChoiceElement(name='discoverd', title=Title('Is discoverd')),
            SingleChoiceElement(name='required', title=Title('Is required')),
            SingleChoiceElement(name='forbidden', title=Title('Is forbidden')),
            SingleChoiceElement(name='ignored', title=Title('Is ignored')),
        ],
        prefill=DefaultValue('discoverd'),
    )


def _migrate_bool_allowed_forbidden(obj: object) -> str:
    if obj is True:
        return 'allowed'
    if obj is False:
        return 'forbidden'
    return obj


def _migrate_bool_en_disabled(obj: object) -> str:
    if obj is True:
        return 'enabled'
    if obj is False:
        return 'disabled'
    return obj


def _parameter_form_winnfsshare():
    return Dictionary(
        elements={
            'Online': DictElement(
                parameter_form=SingleChoice(
                    title=Title('Share Status'),
                    elements=[
                        SingleChoiceElement(name='Online', title=Title('Online')),
                        SingleChoiceElement(name='Offline', title=Title('Offline')),
                        SingleChoiceElement(name='ignored', title=Title('Is ignored')),
                    ],
                    prefill=DefaultValue('Online'),
                )
            ),
            'Authentication': DictElement(
                parameter_form=Dictionary(
                    title=Title('Authentication'),
                    elements={
                        'sys': DictElement(parameter_form=AuthState(title=Title('System Authentication'))),
                        'Krb5': DictElement(parameter_form=AuthState(title=Title('Kerberos Authentication'))),
                        'Krb5i': DictElement(parameter_form=AuthState(title=Title('Kerberos Authentication w/ integrity'))),
                        'Krb5p': DictElement(parameter_form=AuthState(title=Title('Kerberos Authentication w/ privacy'))),
                    },
                ),
                required=True,
            ),
            'AnonymousAccess': DictElement(
                parameter_form=SingleChoice(
                    title=Title('Anonymous Access'),
                    elements=[
                        SingleChoiceElement(name='discoverd', title=Title('Is discoverd')),
                        SingleChoiceElement(name='allowed', title=Title('Allowed')),
                        SingleChoiceElement(name='forbidden', title=Title('Forbidden')),
                        SingleChoiceElement(name='ignored', title=Title('Is ignored')),
                    ],
                    prefill=DefaultValue('ignored'),
                    migrate=_migrate_bool_allowed_forbidden,
                )
            ),
            'UnmappedUserAccess': DictElement(
                parameter_form=SingleChoice(
                    title=Title('Unmapped User Access'),
                    elements=[
                        SingleChoiceElement(name='discoverd', title=Title('Is discoverd')),
                        SingleChoiceElement(name='allowed', title=Title('Allowed')),
                        SingleChoiceElement(name='forbidden', title=Title('Forbidden')),
                        SingleChoiceElement(name='ignored', title=Title('Is ignored')),
                    ],
                    prefill=DefaultValue('ignored'),
                    migrate=_migrate_bool_allowed_forbidden,
                )
            ),
            'discovered': DictElement(
                parameter_form=Dictionary(
                    elements={
                        'Authentication': DictElement(
                            parameter_form=List(element_template=String())
                        ),
                        'AnonymousAccess': DictElement(parameter_form=String()),
                        'UnmappedUserAccess': DictElement(parameter_form=String()),
                    }
                ),
                render_only=True,
            )
        }
    )


rule_spec_winnfsshare = CheckParameters(
    title=Title('Windows NFS Share'),
    topic=Topic.STORAGE,
    parameter_form=_parameter_form_winnfsshare,
    name='winnfsshare',
    condition=HostAndItemCondition(item_title=Title('NFS Share name')),
    help_text=Help('Ensure the Windows Server for NFS Share is in the desired state.'),
)


def _migrate_protocol_state(obj: object) -> str:
    if obj in ['TCP', 'UDP']:
        return obj
    return 'TCPUDP'


def ProtocolState(**kwargs):
    return SingleChoice(
        **kwargs,
        elements=[
            SingleChoiceElement(name='TCPUDP', title=Title('TCP and UDP')),
            SingleChoiceElement(name='TCP', title=Title('TCP only')),
            SingleChoiceElement(name='UDP', title=Title('UDP only')),
        ],
        prefill=DefaultValue('TCPUDP'),
        migrate=_migrate_protocol_state,
    )


def _parameter_form_winnfssrv() -> Dictionary:
    return Dictionary(
        elements={
            'State': DictElement(
                parameter_form=SingleChoice(
                    title=Title('Server State'),
                    elements=[
                        SingleChoiceElement(name='Running', title=Title('Running')),
                        SingleChoiceElement(name='Stopped', title=Title('Stopped')),
                        SingleChoiceElement(name='ignored', title=Title('Is ignored')),
                    ],
                    prefill=DefaultValue('Running'),
                )
            ),
            'EnableNFSV2': DictElement(
                parameter_form=SingleChoice(
                    title=Title('NFSv2'),
                    elements=[
                        SingleChoiceElement(name='enabled', title=Title('Needs to be enabled')),
                        SingleChoiceElement(name='disabled', title=Title('Needs to be disabled')),
                        SingleChoiceElement(name='ignored', title=Title('Is ignored')),
                    ],
                    prefill=DefaultValue('enabled'),
                    migrate=_migrate_bool_en_disabled,
                )
            ),
            'EnableNFSV3': DictElement(
                parameter_form=SingleChoice(
                    title=Title('NFSv3'),
                    elements=[
                        SingleChoiceElement(name='enabled', title=Title('Needs to be enabled')),
                        SingleChoiceElement(name='disabled', title=Title('Needs to be disabled')),
                        SingleChoiceElement(name='ignored', title=Title('Is ignored')),
                    ],
                    prefill=DefaultValue('enabled'),
                    migrate=_migrate_bool_en_disabled,
                )
            ),
            'EnableNFSV4': DictElement(
                parameter_form=SingleChoice(
                    title=Title('NFSv4'),
                    elements=[
                        SingleChoiceElement(name='enabled', title=Title('Needs to be enabled')),
                        SingleChoiceElement(name='disabled', title=Title('Needs to be disabled')),
                        SingleChoiceElement(name='ignored', title=Title('Is ignored')),
                    ],
                    prefill=DefaultValue('enabled'),
                    migrate=_migrate_bool_en_disabled,
                )
            ),
            'MountProtocol': DictElement(
                parameter_form=ProtocolState(title=Title('Mount Protocol'))
            ),
            'NfsProtocol': DictElement(
                parameter_form=ProtocolState(title=Title('Nfs Protocol'))
            ),
            'NisProtocol': DictElement(
                parameter_form=ProtocolState(title=Title('Nis Protocol'))
            ),
            'NlmProtocol': DictElement(
                parameter_form=ProtocolState(title=Title('Nlm Protocol'))
            ),
            'NsmProtocol': DictElement(
                parameter_form=ProtocolState(title=Title('Nsm Protocol'))
            ),
            'PortmapProtocol': DictElement(
                parameter_form=ProtocolState(title=Title('Portmap Protocol'))
            ),
            'MapServerProtocol': DictElement(
                parameter_form=ProtocolState(title=Title('MapServer Protocol'))
            ),
        },
    )


rule_spec_winnfssrv = CheckParameters(
    title=Title('Windows NFS Server'),
    topic=Topic.STORAGE,
    parameter_form=_parameter_form_winnfssrv,
    name='winnfssrv',
    condition=HostCondition(),
    help_text=Help('Ensure the Windows Server for NFS is in the desired state.'),
)
