test_for = 'winnfssrv'


AGENT = '''
<<<winnfssrv:sep(0)>>>


State                            : Running
EnableNFSV2                      : False
EnableNFSV3                      : False
EnableNFSV4                      : True
EnableAuthenticationRenewal      : True
MountProtocol                    : {TCP, UDP}
NfsProtocol                      : {TCP, UDP}
NisProtocol                      : {TCP, UDP}
NlmProtocol                      : {UDP}
NsmProtocol                      : {TCP}
PortmapProtocol                  : {TCP, UDP}
MapServerProtocol                : {TCP, UDP}


Clients : 1
Sessions : 1
'''

def test_parse(check):
    assert check.parse() == {
        'State': 'Running',
        'EnableNFSV2': False,
        'EnableNFSV3': False,
        'EnableNFSV4': True,
        'EnableAuthenticationRenewal': True,
        'MountProtocol': 'TCP, UDP',
        'NfsProtocol': 'TCP, UDP',
        'NisProtocol': 'TCP, UDP',
        'NlmProtocol': 'UDP',
        'NsmProtocol': 'TCP',
        'PortmapProtocol': 'TCP, UDP',
        'MapServerProtocol': 'TCP, UDP',
        'Clients': 1,
        'Sessions': 1
    }

def test_inventory(check):
    assert check.inventory() == [
        (None, {})
    ]

def test_check_wo_config(check):
    assert (0, 'Running') in check.check(None)

def  test_check_stopped(check):
    assert (2, 'Running (expected: Stopped)') in check.check(None, {'State': 'Stopped'})

def  test_check_nov3(check):
    assert (0, 'No NFSv3') in check.check(None, {'EnableNFSV3': False})

def  test_check_withv3(check):
    assert (1, 'Expected NFSv3') in check.check(None, {'EnableNFSV3': True})

def  test_check_nov4(check):
    assert (1, 'Not expected NFSv4') in check.check(None, {'EnableNFSV4': False})

def  test_check_withv4(check):
    assert (0, 'NFSv4') in check.check(None, {'EnableNFSV4': True})

def  test_check_perfdata(check):
    assert (0, None, [('winnfssrv_session', 1), ('winnfssrv_client', 1)]) in check.check(None)
