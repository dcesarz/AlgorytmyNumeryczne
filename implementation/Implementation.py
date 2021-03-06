# KOD : DOMINIKA CESARZ

import numpy as np
from numpy import linalg as LA
from implementation.ControlledParser import ControlledParser
from implementation.Als import Als

class Implementation:
    p = None
    u = None
    r = None
    rCopy = None
    fup_r = None

    def __init__(self, lamb, d, iterations, max_p):
        self.lamb = lamb
        self.d = d
        self.parser = ControlledParser()
        self.als = Als()
        self.i = iterations
        self.max_p = max_p

    @staticmethod
    def generate(h, w):
        m = np.random.random((h, w))
        return m

    # Ten kawałek: Marta Rybarczyk ###

    def fup(self):
        uArray = np.array(self.u)
        uArrayTransposed = np.transpose(self.u)
        pArray = np.array(self.p)
        multipliedUP = np.matmul(uArrayTransposed, pArray)
        sumRUP = 0
        sumUU = 0
        sumPP = 0
        for u in range(0, len(self.u[0])):
            for p in range(0, len(self.p[0])):
                if self.r[u][p] != 0:
                    sumRUP += (self.r[u][p] - multipliedUP[u][p]) ** 2
        for u in range(0, len(self.u)):
            sumUU += LA.norm(uArray[u]) ** 2
        for p in range(0, len(self.p)):
            sumPP += LA.norm(pArray[p]) ** 2
        foo = self.lamb * (sumUU + sumPP)
        return sumRUP + foo

    def calculatingErrors(self, r):
        sumErrors = 0
        weird = 0
        qErrors = 1
        for i in range(0, len(self.r)):
            for j in range(0, len(self.r[0])):
                if self.r[i][j] != 0:
                    weird = 0
                    for k in range (0, self.d):
                        weird += self.u[k][i] * self.p[k][j]
                        qErrors += 1
                    sumErrors += abs(self.r[i][j] - weird)
        aproxErrors = sumErrors / qErrors
        return aproxErrors

    ##################################

    def do_alg(self):
        self.parser.parseToNewFile(self.max_p)
        self.r = self.parser.parseFromNewFile()
        p_size = len(self.r[0])
        u_size = len(self.r)

        self.p = self.generate(self.d, p_size)
        self.u = self.generate(self.d, u_size)

        for j in range(0, self.i):
            self.u, self.p = self.als.als(self.r, self.u, self.p, self.lamb)
            self.fup()

        r = self.als.createResult(self.u, self.p)
        aproxErrors = self.calculatingErrors(r)
        separator = ' '
        ae = separator.join(["średnia błędu =", str(aproxErrors), "\n"])
        return r, ae

    def zb(self):
        self.parser.parseToNewFile(self.max_p)
        self.r = self.parser.parseFromNewFile()
        p_size = len(self.r[0])
        u_size = len(self.r)
        zbieznosc = []
        foo1 = 0
        foo2 = 0

        self.p = self.generate(self.d, p_size)
        self.u = self.generate(self.d, u_size)

        for j in range(0, self.i):
            self.u, self.p = self.als.als(self.r, self.u, self.p, self.lamb)
            self.fup()
            if j % 2 == 0:
                foo1 = self.fup()
                if j != 0:
                    zbieznosc.append((abs(foo1 - foo2) / foo1))
            elif j % 2 == 1:
                foo2 = self.fup()
                zbieznosc.append((abs(foo1 - foo2) / foo1))

        return zbieznosc


