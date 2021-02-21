#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#
# winnfsshare - Windows NFS Share check
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

# <<<winnfsshare:sep(124)>>>
# Name|Online|Clustered|Authentication|AnonymousAccess|UnmappedUserAccess
# homes|True|False|Krb5p|False|False

from typing import Any, Dict, Mapping, Optional
from .agent_based_api.v1 import (
    register,
    type_defs,
    Service,
    Result,
    State,
)


def parse_winnfsshare(string_table: type_defs.StringTable) -> Optional[Dict[str, Dict[str, Any]]]:
    parsed: Dict[str, Dict[str, Any]] = {}

    keys = string_table.pop(0)[1:]

    for line in string_table:
        name = line.pop(0)
        parsed[name] = dict(zip(keys, line))
        parsed[name]['Authentication'] = parsed[name]['Authentication'].split(',')
        parsed[name]['Online'] = 'Online' if parsed[name]['Online'] == 'True' else 'Offline'

    return parsed


register.agent_section(
    name='winnfsshare',
    parse_function=parse_winnfsshare,
)


WINNFSSHARE_CHECK_DEFAULT_PARAMETERS = {
    'Online': 'Online',
}


def discover_winnfsshare(section: Optional[Dict[str, Dict[str, Any]]]) -> type_defs.DiscoveryResult:
    for key, value in section.items():
        params = {'discovered': {
            'Authentication': value['Authentication'],
            'AnonymousAccess': value['AnonymousAccess'],
            'UnmappedUserAccess': value['UnmappedUserAccess'],
        }}
        yield Service(item=key, parameters=params)


def check_winnfsshare(item: str, params: Mapping, section: Optional[Dict[str, Dict[str, Any]]]) -> type_defs.CheckResult:
    if item not in section:
        return

    current = section[item]

    if params['Online'] == 'ignored' or params['Online'] == current['Online']:
        yield Result(state=State.OK, summary=current['Online'])
    else:
        yield Result(state=State.CRIT, summary="%s (expected: %s)" % (current['Online'], params['Online']))

    if 'Authentication' in params:
        yield Result(state=State.OK, summary="Authentication:")
        for methode, state in params['Authentication'].items():
            if state == 'ignored':
                continue

            if state == 'forbidden':
                if methode in current['Authentication']:
                    yield Result(state=State.WARN, summary='Not expected %s' % methode)
            elif state == 'required':
                if methode in current['Authentication']:
                    yield Result(state=State.OK, summary=methode)
                else:
                    yield Result(state=State.WARN, summary='Expected %s' % methode)
            else:
                if methode in current['Authentication'] and methode in params['discovered']['Authentication']:
                    yield Result(state=State.OK, summary=methode)
                elif methode in current['Authentication']:
                    yield Result(state=State.WARN, summary='Not expected %s' % methode)
                else:
                    yield Result(state=State.WARN, summary='Expected %s' % methode)

    if 'AnonymousAccess' in params:
        if params['AnonymousAccess'] == 'ignored':
            pass
        if params['AnonymousAccess'] == 'discoverd':
            params['AnonymousAccess'] = params['discovered']['AnonymousAccess']

        state = State.OK
        if current['AnonymousAccess'] != params['AnonymousAccess']:
            state = State.WARN

        if current['AnonymousAccess'] == 'True':
            yield Result(state=state, summary='Anonymous Access allowed')
        else:
            yield Result(state=state, summary='Anonymous Access not allowed')

    if "UnmappedUserAccess" in params:
        if params['UnmappedUserAccess'] == 'ignored':
            pass
        if params['UnmappedUserAccess'] == 'discoverd':
            params['UnmappedUserAccess'] = params['discovered']['UnmappedUserAccess']

        state = State.OK
        if current['UnmappedUserAccess'] != params['UnmappedUserAccess']:
            state = State.WARN

        if current['UnmappedUserAccess'] == 'True':
            yield Result(state=state, summary='Unmapped User Access allowed')
        else:
            yield Result(state=state, summary='Unmapped User not allowed')


register.check_plugin(
    name = 'winnfsshare',
    service_name = 'NFS Share /%s',
    discovery_function = discover_winnfsshare,
    check_function = check_winnfsshare,
    check_default_parameters = WINNFSSHARE_CHECK_DEFAULT_PARAMETERS,
    check_ruleset_name = 'winnfsshare',
)
