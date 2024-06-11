#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#
# winnfsshare - Windows NFS Share check
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

import pytest
from cmk.agent_based.v2 import (
    Result,
    Service,
    State,
)
from cmk_addons.plugins.winnfs.agent_based import winnfsshare

EXAMPLE_STRING_TABLE = [
    ['Name', 'Online', 'Clustered', 'Authentication', 'AnonymousAccess', 'UnmappedUserAccess'],
    ['homes', 'True', 'False', 'Krb5p', 'False', 'False'],
]
EXAMPLE_SECTION = {
    'homes': {
        'AnonymousAccess': 'False',
        'Authentication': ['Krb5p'],
        'Clustered': 'False',
        'Online': 'Online',
        'UnmappedUserAccess': 'False'
    }
}


@pytest.mark.parametrize('string_table, result', [
    ([EXAMPLE_STRING_TABLE[0]], {}),
    (
        EXAMPLE_STRING_TABLE,
        EXAMPLE_SECTION
    ),
])
def test_parse_winnfsshare(string_table, result):
    assert winnfsshare.parse_winnfsshare(string_table) == result


@pytest.mark.parametrize('section, result', [
    ({}, []),
    (
        EXAMPLE_SECTION,
        [Service(item='homes', parameters={'discovered': {'Authentication': ['Krb5p'], 'AnonymousAccess': 'False', 'UnmappedUserAccess': 'False'}})]
    ),
])
def test_discover_winnfsshare(section, result):
    assert list(winnfsshare.discover_winnfsshare(section)) == result


@pytest.mark.parametrize('item, params, result', [
    ('', {}, []),
    (
        'homes',
        {'discovered': {'Authentication': ['Krb5p'], 'AnonymousAccess': 'False', 'UnmappedUserAccess': 'False'}},
        [Result(state=State.OK, summary='Online')]
    ),
    (
        'homes',
        {
            'discovered': {'Authentication': ['Krb5p'], 'AnonymousAccess': 'False', 'UnmappedUserAccess': 'False'},
            'Authentication': {'Krb5p': 'discoverd'}
        },
        [
            Result(state=State.OK, summary='Online'),
            Result(state=State.OK, summary='Authentication:'),
            Result(state=State.OK, summary='Krb5p'),
        ]
    ),
    (
        'homes',
        {
            'discovered': {'Authentication': ['Krb5i'], 'AnonymousAccess': 'False', 'UnmappedUserAccess': 'False'},
            'Authentication': {'Krb5p': 'discoverd'}
        },
        [
            Result(state=State.OK, summary='Online'),
            Result(state=State.OK, summary='Authentication:'),
            Result(state=State.WARN, summary='Not expected Krb5p'),
        ]
    ),
    (
        'homes',
        {
            'discovered': {'Authentication': ['Krb5p'], 'AnonymousAccess': 'False', 'UnmappedUserAccess': 'False'},
            'Authentication': {'Krb5i': 'required', 'Krb5p': 'forbidden'}
        },
        [
            Result(state=State.OK, summary='Online'),
            Result(state=State.OK, summary='Authentication:'),
            Result(state=State.WARN, summary='Expected Krb5i'),
            Result(state=State.WARN, summary='Not expected Krb5p'),
        ]
    ),
    (
        'homes',
        {
            'discovered': {'Authentication': ['Krb5p'], 'AnonymousAccess': 'False', 'UnmappedUserAccess': 'False'},
            'AnonymousAccess': 'discoverd',
        },
        [
            Result(state=State.OK, summary='Online'),
            Result(state=State.OK, summary='Anonymous Access not allowed'),
        ]
    ),
    (
        'homes',
        {
            'discovered': {'Authentication': ['Krb5p'], 'AnonymousAccess': 'True', 'UnmappedUserAccess': 'True'},
            'AnonymousAccess': 'discoverd', 'UnmappedUserAccess': 'discoverd',
        },
        [
            Result(state=State.OK, summary='Online'),
            Result(state=State.WARN, summary='Anonymous Access not allowed'),
            Result(state=State.WARN, summary='Unmapped User not allowed'),
        ]
    ),
    (
        'homes',
        {
            'discovered': {'Authentication': ['Krb5p'], 'AnonymousAccess': 'True', 'UnmappedUserAccess': 'False'},
            'AnonymousAccess': 'ignored', 'UnmappedUserAccess': 'ignored',
        },
        [
            Result(state=State.OK, summary='Online'),
            Result(state=State.OK, summary='Anonymous Access not allowed'),
            Result(state=State.OK, summary='Unmapped User not allowed'),
        ]
    ),
    (
        'homes',
        {
            'discovered': {'Authentication': ['Krb5p'], 'AnonymousAccess': 'True', 'UnmappedUserAccess': 'False'},
            'AnonymousAccess': 'forbidden', 'UnmappedUserAccess': 'forbidden',
        },
        [
            Result(state=State.OK, summary='Online'),
            Result(state=State.OK, summary='Anonymous Access not allowed'),
            Result(state=State.OK, summary='Unmapped User not allowed'),
        ]
    ),
    (
        'homes',
        {
            'discovered': {'Authentication': ['Krb5p'], 'AnonymousAccess': 'True', 'UnmappedUserAccess': 'False'},
            'AnonymousAccess': 'allowed', 'UnmappedUserAccess': 'allowed',
        },
        [
            Result(state=State.OK, summary='Online'),
            Result(state=State.WARN, summary='Anonymous Access not allowed'),
            Result(state=State.WARN, summary='Unmapped User not allowed'),
        ]
    ),
])
def test_check_win_scheduled_task(item, params, result):
    merged_params = winnfsshare.WINNFSSHARE_CHECK_DEFAULT_PARAMETERS.copy()
    merged_params.update(params)
    assert list(winnfsshare.check_winnfsshare(item, merged_params, EXAMPLE_SECTION)) == result
