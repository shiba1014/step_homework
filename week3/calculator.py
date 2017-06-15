def readNumber(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        keta = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * keta
            keta *= 0.1
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index


def readPlus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1

def readMinus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1

def readTimes(line, index):
    token = {'type': 'TIMES'}
    return token, index + 1

def readDivide(line, index):
    token = {'type': 'DIVIDE'}
    return token, index + 1


def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = readNumber(line, index)
        elif line[index] == '+':
            (token, index) = readPlus(line, index)
        elif line[index] == '-':
            (token, index) = readMinus(line, index)
        elif line[index] == '*':
            (token, index) = readTimes(line, index)
        elif line[index] == '/':
            (token, index) = readDivide(line, index)
        else:
            print 'Invalid character found: ' + line[index]
            exit(1)
        tokens.append(token)
    return tokens


def secondEvaluate(tokens):
    answer = 0
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    index = 1
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']
            else:
                print 'Invalid syntax'
        index += 1
    return answer


def firstEvaluate(tokens):
    index = 0
    beforeNum = 0
    newTokens = []
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            beforeNum = tokens[index]['number']
        elif tokens[index]['type'] == 'PLUS' or tokens[index]['type'] == 'MINUS':
            token = {'type': 'NUMBER', 'number': beforeNum}
            newTokens.append(token)
            newTokens.append(tokens[index])
        elif tokens[index]['type'] == 'TIMES':
            beforeNum *= tokens[index + 1]['number']
            index += 1
        elif tokens[index]['type'] == 'DIVIDE':
            beforeNum /= tokens[index + 1]['number']
            index += 1
        index += 1

    token = {'type': 'NUMBER', 'number': beforeNum}
    newTokens.append(token)
    return newTokens



def test(line, expectedAnswer):
    tokens = tokenize(line)
    tokens = firstEvaluate(tokens)
    actualAnswer = secondEvaluate(tokens)
    if abs(actualAnswer - expectedAnswer) < 1e-8:
        print "PASS! (%s = %f)" % (line, expectedAnswer)
    else:
        print "FAIL! (%s should be %f but was %f)" % (line, expectedAnswer, actualAnswer)


# Add more tests to this function :)
def runTest():
    print "==== Test started! ===="
    test("1+2", 3)
    test("2-12", -10)
    test("1.0+2.1-3", 0.1)
    test("1+3*4/3-2", 3)
    test("-2+2", 0)
    test("1.5*2-5/2.5", 1)
    print "==== Test finished! ====\n"

runTest()

while True:
    print '> ',
    line = raw_input()
    tokens = tokenize(line)
    tokens = firstEvaluate(tokens)
    answer = secondEvaluate(tokens)
    print "answer = %f\n" % answer