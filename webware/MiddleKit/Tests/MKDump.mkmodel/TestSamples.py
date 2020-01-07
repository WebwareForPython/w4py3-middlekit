import difflib


def test(store):
    with open('Dump.csv', 'w') as samples:
        store.dumpObjectStore(samples)

    dumped = open('Dump.csv').readlines()
    expected = open('../MKDump.mkmodel/Samples.csv').readlines()
    diff = list(map(str.rstrip, difflib.context_diff(dumped, expected,
        fromfile='dumped.csv', tofile='expected.csv')))

    if diff:
        print('\n\n\nDump output did not match what was expected.')
        print('DIFF OUTPUT BEGIN:')
        for line in diff:
            print(line)
        print('DIFF OUTPUT END')

    assert not diff
