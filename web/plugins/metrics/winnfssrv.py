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

from cmk.gui.plugins.metrics import (
    metric_info,
    check_metrics,
    perfometer_info,
)


metric_info['winnfssrv_client'] = {
    'title': _('Clients'),
    'unit': 'count',
    'color': '31/a',
}

metric_info['winnfssrv_session'] = {
    'title': _('Sessions'),
    'unit': 'count',
    'color': '32/a',
}

check_metrics['check_mk-winnfssrv'] = {
    'winnfssrv_client': {
        'name': 'winnfssrv_client',
    },
    'winnfssrv_session': {
        'name': 'winnfssrv_session',
    },
}

perfometer_info.append({
    "type": "stacked",
    "perfometers": [{
        "type": "logarithmic",
        "metric": "winnfssrv_client",
        "half_value": 10,
        "exponent": 2
    }, {
        "type": "logarithmic",
        "metric": "winnfssrv_session",
        "half_value": 10,
        "exponent": 2
    }],
})
