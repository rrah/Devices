"""
Don't bother using this one. Kinda stupid and maybe broken.
Will fix at some point."""

import telnetlib as tel


hedcoHost = 'strmre.ystv.york.ac.uk'
hedcoPort = 2001
hedcoTel = tel.Telnet(hedcoHost, hedcoPort, 1)
hedcoTel.close()


def change(in_List, outList = None):
    if outList is not None:
        if len(in_List) != len(outList):
            return 'must have same number of inputs and outputs'
    string = 'BUFFER 01\r\nBUFFER CLEAR\r\n'
    if outList == None:
        outList = []
        for i in range(1, len(in_List) + 1):
            outList.append(i)
    for i in range(0, len(in_List)):
        string += 'LEVEL {}\r\nXPT {},01\r\n'.format(outList[i] - 1, in_List[i])
    string += 'EXECUTE 01\r\n'
    hedcoTel.open(hedcoHost, hedcoPort, 1)
    hedcoTel.read_until('\r\n\r\n', 1)
    hedcoTel.write(string)
    result = hedcoTel.read_until('\r\n\r\n', 1)
    hedcoTel.close()
    return result
