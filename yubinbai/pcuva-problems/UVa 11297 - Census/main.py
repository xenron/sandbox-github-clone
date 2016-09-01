'''
Created on Jul 9, 2013
@author: Yubin Bai
'''
import time
from multiprocessing.pool import Pool
from SegmentTree2D import SegmentTree2D
parallelSolve = False
INF = 1 << 31


def solve(par):
    N, Q, mat, queries = par
    treeMax = SegmentTree2D()

    def maxFunc(*args):
        return max(args)
    treeMax.buildTree(mat, maxFunc, INF)
    treeMin = SegmentTree2D()

    def minFunc(*args):
        return min(args)
    treeMin.buildTree(mat, minFunc, -1 * INF)
    result = []
    for q in queries:
        if q[0] == 'q':
            for j in range(1, len(q)):
                q[j] -= 1
            result.append([treeMax.query(q[1], q[2], q[3], q[4]),
                           treeMin.query(q[1], q[2], q[3], q[4])])
        if q[0] == 'c':
            for j in range(1, len(q) - 1):
                q[j] -= 1
            treeMax.update(q[1], q[2], q[3])
            treeMin.update(q[1], q[2], q[3])

    resultStr = []
    for e in result:
        resultStr.append(' '.join(str(i) for i in e))
    return '\n'.join(resultStr)


class Solver:

    def getInput(self):
        self.numOfTests = 1
        self.input = []
        N = int(self.fIn.readline())
        mat = []
        for i in range(N):
            row = map(int, self.fIn.readline().split())
            mat.append(row)
        Q = int(self.fIn.readline())
        queries = []
        for i in range(Q):
            row = self.fIn.readline().split()
            for i in range(1, len(row)):
                row[i] = int(row[i])
            queries.append(row)
        self.input.append((N, Q, mat, queries))

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
