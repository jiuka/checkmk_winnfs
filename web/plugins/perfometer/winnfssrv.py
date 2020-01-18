#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

def perfometer_winnfssrv(row, check_command, perf_data):
    perf_data = dict(map(lambda x: (x[0], x[1:]), perf_data))
    return "Clients: %d" % (perf_data['winnfssrv_client'][0]), perfometer_logarithmic(perf_data['winnfssrv_client'][0], 4, 2, "#0f0")

perfometers["check_mk-winnfssrv"] = perfometer_winnfssrv
