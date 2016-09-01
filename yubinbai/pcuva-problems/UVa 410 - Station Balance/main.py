'''
Created on Jul 17, 2013
@author: Yubin Bai
'''
import time
from multiprocessing.pool import Pool
parallelSolve = False
INF = 1 << 31


def solve(par):
    C, S, array = par
    if S < 2 * C:
        array += [0] * (2 * C - S)
    array.sort()
    result = []
    low = 0
    high = 2 * C - 1
    while low < high:
        if array[low] == 0:
            result.append([array[high]])
        else:
            result.append([array[low], array[high]])
        low += 1
        high -= 1
    avg = sum(array) * 1.0 / C
    imba = sum(abs(sum(e) - avg) for e in result)
    resultStr = []
    for i, row in enumerate(result):
        resultStr.append('%d: %s' % (i, ' '.join(str(e) for e in row)))
    resultStr.append('IMBALANCE = %.6f' % imba)
    return '\n'.join(resultStr)


class Solver:

    def getInput(self):
        self.numOfTests = 0
        self.input = []
        while True:
            line = self.fIn.readline().strip()
            if line == '':
                break
            self.numOfTests += 1
            C, S = map(int, line.split())
            array = map(int, self.fIn.readline().split())
            self.input.append((C, S, array))

    def __init__(self):
        self.fIn = open('input.txt')
        self.fOut = open('output.txt', 'w')
        self.results = []

    def parallel(self):
        self.getInput()
        p = Pool(4)
        millis1 = int(round(time.time() * 1000))
        self.results = p.map(solve, self.input)
        millis2 = int(round(time.time() * 1000))
        print("Time in milliseconds: %d " % (millis2 - millis1))
        self.makeOutput()

    def sequential(self):
        self.getInput()
        millis1 = int(round(time.time() * 1000))
        for i in self.input:
            self.results.append(solve(i))
        millis2 = int(round(time.time() * 1000))
        print("Time in milliseconds: %d " % (millis2 - millis1))
        self.makeOutput()

    def makeOutput(self):
        for test in range(self.numOfTests):
            self.fOut.write("%s\n" % self.results[test])
        self.fIn.close()
        self.fOut.close()

if __name__ == '__main__':
    solver = Solver()
    if parallelSolve:
        solver.parallel()
    else:
        solver.sequential()
