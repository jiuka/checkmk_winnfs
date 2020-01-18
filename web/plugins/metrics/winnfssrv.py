#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

metric_info["winnfssrv_client"] = {
    "title": _("Clients"),
    "unit": "count",
    "color": "31/a",
}

metric_info["winnfssrv_session"] = {
    "title": _("Sessions"),
    "unit": "count",
    "color": "32/a",
}

check_metrics["check_mk-winnfssrv"] = {
    "winnfssrv_client": {
        "name": "winnfssrv_client",
    },
    "winnfssrv_session": {
        "name": "winnfssrv_session",
    },
}
