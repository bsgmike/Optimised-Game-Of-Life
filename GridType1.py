"""
This grid class is pinched from https://github.com/yiHahoi/conway
"""
import sys
import os
import numpy


class gridType1(object):

    def __init__(self, W = 20, H = 20):
        # Initialise class attributes
        self.WIDTH = W
        self.HEIGHT = H
        self.prevState = numpy.zeros((self.HEIGHT, self.WIDTH))
        self.nextState = numpy.zeros((self.HEIGHT, self.WIDTH))
        numpy.copyto(self.prevState, self.nextState)

    def tick(self):
        # Advance one generation
        self.applyRules()
        numpy.copyto(self.prevState, self.nextState)

    def applyRules(self):
        for i in range(self.HEIGHT):
            for j in range(self.WIDTH):
                count = self.countNeighbors(i, j)
                if self.prevState[i, j] == 1:
                    #Subpoblacion
                    if count < 2:
                        self.nextState[i, j] = 0
                    #Sobrepoblacion
                    elif count > 3:
                        self.nextState[i, j] = 0
                    #Estasis
                    else:
                        self.nextState[i, j] = 1
                #MUERTA
                else:
                    #Reproduccion
                    if count == 3:
                        self.nextState[i, j] = 1

    def countNeighbors(self, i, j):
        """
        Cuenta el numero de vecinos vivos de la posicion i,j

        [ i-1,j-1 ]    [ i-1,j ]    [ i-1,j+1 ]
        [  i,j-1  ]    [  i,j  ]    [  i,j+1  ]
        [ i+1,j-1 ]    [ i+1,j ]    [ i+1,j+1 ]

        """
        ctr = 0
        # FILA 1
        if i - 1 >= 0 and j - 1 >= 0 and self.prevState[i - 1, j - 1] == 1:
            ctr += 1
        if i - 1 >= 0 and self.prevState[i - 1, j] == 1:
            ctr += 1
        if i - 1 >= 0 and j + 1 < self.WIDTH and self.prevState[i - 1, j + 1] == 1:
            ctr += 1
        # FILA 2
        if j - 1 >= 0 and self.prevState[i, j - 1] == 1:
            ctr += 1
        if j + 1 < self.WIDTH and self.prevState[i, j + 1] == 1:
            ctr += 1
        # FILA 3
        if i + 1 < self.HEIGHT and j - 1 >= 0 and self.prevState[i + 1, j - 1] == 1:
            ctr += 1
        if i + 1 < self.HEIGHT and self.prevState[i + 1, j] == 1:
            ctr += 1
        if i + 1 < self.HEIGHT and j + 1 < self.WIDTH and self.prevState[i + 1, j + 1] == 1:
            ctr += 1

        return ctr
