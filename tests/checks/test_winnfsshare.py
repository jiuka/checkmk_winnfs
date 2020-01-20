test_for = 'winnfsshare'


AGENT = '''
<<<winnfsshare:sep(124)>>>
Name|Online|Clustered|Authentication|AnonymousAccess|UnmappedUserAccess
homes|True|False|Krb5i,Krb5p|False|False
'''

def test_parse(check):
    assert check.parse() == {'homes': {'Clustered': 'False', 'UnmappedUserAccess': 'False', 'Authentication': ['Krb5i', 'Krb5p'], 'AnonymousAccess': 'False', 'Online': 'True'}}

def test_inventory(check):
    assert check.inventory() == [
        ('homes', {'discovered': {'UnmappedUserAccess': 'False', 'Authentication': ['Krb5i', 'Krb5p'], 'AnonymousAccess': 'False'}})
    ]

def test_check_wo_config(check):
    assert (0, 'Online') in check.check('homes')

def  test_check_online(check):
    assert (0, 'Online') in check.check('homes', {'Online': 'True'})

def  test_check_offline(check):
    assert (2, 'Online (expected: Offline)') in check.check('homes', {'Online': 'False'})

def  test_check_unknown_share(check):
    assert (2, 'Share not found') in check.check('homes2')
