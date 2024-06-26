#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#
# winnfssrv - Windows NFS Server check
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

# <<<winnfssrv:sep(0)>>>
#
#
# State                            : Running
# LogActivity                      :
# CharacterTranslationFile         : Not Configured
# DirectoryCacheSize (KB)          : 128
# HideFilesBeginningInDot          : Enabled
# EnableNFSV2                      : False
# EnableNFSV3                      : False
# EnableNFSV4                      : True
# EnableAuthenticationRenewal      : True
# AuthenticationRenewalIntervalSec : 600
# NlmGracePeriodSec                : 45
# MountProtocol                    : {TCP, UDP}
# NfsProtocol                      : {TCP, UDP}
# NisProtocol                      : {TCP, UDP}
# NlmProtocol                      : {TCP, UDP}
# NsmProtocol                      : {TCP, UDP}
# PortmapProtocol                  : {TCP, UDP}
# MapServerProtocol                : {TCP, UDP}
# PreserveInheritance              : False
# NetgroupCacheTimeoutSec          : 30
# UnmappedUserAccount              :
# WorldAccount                     : Everyone
# AlwaysOpenByName                 : False
# GracePeriodSec                   : 240
# LeasePeriodSec                   : 120
# OnlineTimeoutSec                 : 180
#
# Clients : 0
# Sessions : 0

import re
from typing import Any, Dict, Mapping, Optional
from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    Metric,
    Result,
    Service,
    State,
    StringTable,
)


def parse_winnfssrv(string_table: StringTable) -> Optional[Dict[str, Any]]:
    parsed: Dict[str, Any] = {}

    for line in string_table:
        key, val = re.split(r'\s*:\s*', line[0])
        if val.isdigit():
            parsed[key] = int(val)
        elif val in ['Enabled', 'True']:
            parsed[key] = True
        elif val in ['Disabled', 'False']:
            parsed[key] = False
        elif val.startswith('{'):
            parsed[key] = val[1:-1]
        else:
            parsed[key] = val
    return parsed


agent_section_winnfssrv = AgentSection(
    name='winnfssrv',
    parse_function=parse_winnfssrv,
)


WINNFSSRV_CHECK_DEFAULT_PARAMETERS = {
    'State': 'Running',
}


def discover_winnfssrv(section: Optional[Dict[str, Dict[str, Any]]]) -> DiscoveryResult:
    if 'State' in section:
        yield Service()


def check_winnfssrv(params: Mapping, section: Optional[Dict[str, Dict[str, Any]]]) -> CheckResult:
    if params['State'] in ['ignored', section['State']]:
        yield Result(state=State.OK, summary=section['State'])
    else:
        yield Result(state=State.CRIT, summary='%s (expected: %s)' % (section['State'], params['State']))

    for version in range(2, 5):
        name = 'EnableNFSV%d' % version
        param = params.get(name, 'ignored')

        match param, section[name]:
            case 'ignored', True:
                yield Result(state=State.OK, summary='NFSv%d' % version)
            case 'enabled', True:
                yield Result(state=State.OK, summary='NFSv%d' % version)
            case 'enabled', False:
                yield Result(state=State.WARN, summary='Expected NFSv%d' % version)
            case 'disabled', False:
                yield Result(state=State.OK, summary='No NFSv%d' % version)
            case 'disabled', True:
                yield Result(state=State.WARN, summary='Not expected NFSv%d' % version)

    for protocol in [
            'MountProtocol',
            'NfsProtocol',
            'NisProtocol',
            'NlmProtocol',
            'NsmProtocol',
            'PortmapProtocol',
            'MapServerProtocol']:
        if protocol not in params:
            continue

        if params[protocol] == 'TCPUDP':
            params[protocol] = 'TCP, UDP'

        if section[protocol] == params[protocol]:
            yield Result(state=State.OK, summary='%s: %s' % (protocol, section[protocol]))
        else:
            yield Result(state=State.WARN, summary='%s: %s (expected: %s)' % (protocol, section[protocol], params[protocol]))

    yield Metric('winnfssrv_session', section['Sessions'])
    yield Metric('winnfssrv_client', section['Clients'])


check_plugin_winnfssrv = CheckPlugin(
    name = 'winnfssrv',
    service_name = 'NFS Server',
    discovery_function = discover_winnfssrv,
    check_function = check_winnfssrv,
    check_default_parameters = WINNFSSRV_CHECK_DEFAULT_PARAMETERS,
    check_ruleset_name = 'winnfssrv',
)
