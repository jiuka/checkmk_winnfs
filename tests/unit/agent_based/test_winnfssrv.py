#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#
# winnfssrv - Windows NFS Server check
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

import pytest
from cmk.base.plugins.agent_based.agent_based_api.v1 import (
    Metric,
    Result,
    Service,
    State,
)
from cmk.base.plugins.agent_based import winnfssrv

EXAMPLE_STRING_TABLE = [
    ['State                            : Running'],
    ['LogActivity                      :'],
    ['CharacterTranslationFile         : Not Configured'],
    ['DirectoryCacheSize (KB)          : 128'],
    ['HideFilesBeginningInDot          : Enabled'],
    ['EnableNFSV2                      : False'],
    ['EnableNFSV3                      : False'],
    ['EnableNFSV4                      : True'],
    ['EnableAuthenticationRenewal      : True'],
    ['AuthenticationRenewalIntervalSec : 600'],
    ['NlmGracePeriodSec                : 45'],
    ['MountProtocol                    : {TCP, UDP}'],
    ['NfsProtocol                      : {TCP, UDP}'],
    ['NisProtocol                      : {TCP, UDP}'],
    ['NlmProtocol                      : {TCP, UDP}'],
    ['NsmProtocol                      : {TCP, UDP}'],
    ['PortmapProtocol                  : {TCP, UDP}'],
    ['MapServerProtocol                : {TCP, UDP}'],
    ['PreserveInheritance              : False'],
    ['NetgroupCacheTimeoutSec          : 30'],
    ['UnmappedUserAccount              :'],
    ['WorldAccount                     : Everyone'],
    ['AlwaysOpenByName                 : False'],
    ['GracePeriodSec                   : 240'],
    ['LeasePeriodSec                   : 120'],
    ['OnlineTimeoutSec                 : 180'],
    ['Clients : 1'],
    ['Sessions : 2'],
]
EXAMPLE_SECTION = {
    'State': 'Running',
    'LogActivity': '',
    'CharacterTranslationFile': 'Not Configured',
    'DirectoryCacheSize (KB)': 128,
    'HideFilesBeginningInDot': True,
    'EnableNFSV2': False,
    'EnableNFSV3': False,
    'EnableNFSV4': True,
    'EnableAuthenticationRenewal': True,
    'AuthenticationRenewalIntervalSec': 600,
    'NlmGracePeriodSec': 45,
    'MountProtocol': 'TCP, UDP',
    'NfsProtocol': 'TCP, UDP',
    'NisProtocol': 'TCP, UDP',
    'NlmProtocol': 'TCP, UDP',
    'NsmProtocol': 'TCP, UDP',
    'PortmapProtocol': 'TCP, UDP',
    'MapServerProtocol': 'TCP, UDP',
    'PreserveInheritance': False,
    'NetgroupCacheTimeoutSec': 30,
    'UnmappedUserAccount': '',
    'WorldAccount': 'Everyone',
    'AlwaysOpenByName': False,
    'GracePeriodSec': 240,
    'LeasePeriodSec': 120,
    'OnlineTimeoutSec': 180,
    'Clients': 1,
    'Sessions': 2,
}


@pytest.mark.parametrize('string_table, result', [
    ([], {}),
    (
        EXAMPLE_STRING_TABLE,
        EXAMPLE_SECTION
    ),
])
def test_parse_winnfssrv(string_table, result):
    assert winnfssrv.parse_winnfssrv(string_table) == result


@pytest.mark.parametrize('section, result', [
    ({}, []),
    (EXAMPLE_SECTION, [Service()]),
])
def test_discover_winnfssrv(section, result):
    assert list(winnfssrv.discover_winnfssrv(section)) == result


@pytest.mark.parametrize('params, result', [
    (
        {},
        [
            Result(state=State.OK, summary='Running'),
            Result(state=State.OK, summary='NFSv4'),
            Metric('winnfssrv_session', 2.0),
            Metric('winnfssrv_client', 1.0)
        ]
    ),
    (
        {'EnableNFSV3': True},
        [
            Result(state=State.OK, summary='Running'),
            Result(state=State.WARN, summary='Expected NFSv3'),
            Result(state=State.OK, summary='NFSv4'),
            Metric('winnfssrv_session', 2.0),
            Metric('winnfssrv_client', 1.0)
        ]
    ),
    (
        {'EnableNFSV3': False},
        [
            Result(state=State.OK, summary='Running'),
            Result(state=State.OK, summary='No NFSv3'),
            Result(state=State.OK, summary='NFSv4'),
            Metric('winnfssrv_session', 2.0),
            Metric('winnfssrv_client', 1.0)
        ]
    ),
    (
        {'EnableNFSV3': 'ignored', 'EnableNFSV4': 'ignored'},
        [
            Result(state=State.OK, summary='Running'),
            Result(state=State.OK, summary='NFSv4'),
            Metric('winnfssrv_session', 2.0),
            Metric('winnfssrv_client', 1.0)
        ]
    ),
])
def test_check_win_scheduled_task(params, result):
    merged_params = winnfssrv.WINNFSSRV_CHECK_DEFAULT_PARAMETERS.copy()
    merged_params.update(params)
    assert list(winnfssrv.check_winnfssrv(merged_params, EXAMPLE_SECTION)) == result
