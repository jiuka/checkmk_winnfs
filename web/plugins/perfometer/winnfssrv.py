#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

def perfometer_winnfssrv(row, check_command, perf_data):
    h = '<div class="stacked">'
    texts = []
    for i, color, base, scale, verbfunc in [
        (0, "#00FFB2", 10000, 10, lambda v: ("Clients: %d") % v),
        (1, "#00FFFF", 10000, 10, lambda v: ("Sessions: %d") % v),
    ]:
        val = float(perf_data[i][1])
        h += perfometer_logarithmic(val, base, scale, color)
        texts.append(verbfunc(val))
    h += '</div>'
    return " / ".join(texts), h

perfometers["check_mk-winnfssrv"] = perfometer_winnfssrv
