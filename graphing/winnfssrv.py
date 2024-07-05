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

from cmk.graphing.v1 import (
    metrics,
    perfometers,
)

metric_winnfssrv_client = metrics.Metric(
    name='winnfssrv_client',
    title=metrics.Title('Clients'),
    unit=metrics.Unit(metrics.DecimalNotation("")),
    color=metrics.Color.LIGHT_GREEN,
)

metric_winnfssrv_session = metrics.Metric(
    name='winnfssrv_session',
    title=metrics.Title('Sessions'),
    unit=metrics.Unit(metrics.DecimalNotation("")),
    color=metrics.Color.GREEN,
)

perfometer_winnfssrv = perfometers.Stacked(
    name='winnfssrv',
    upper=perfometers.Perfometer(
        name='winnfssrv_client',
        focus_range=perfometers.FocusRange(perfometers.Closed(0), perfometers.Open(10)),
        segments=['winnfssrv_client'],
    ),
    lower=perfometers.Perfometer(
        name='winnfssrv_session',
        focus_range=perfometers.FocusRange(perfometers.Closed(0), perfometers.Open(10))),
        segments=['winnfssrv_session'],
    )
)
