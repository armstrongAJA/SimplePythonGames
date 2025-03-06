import sys
import pygame
import random
import globalVariables as mn
from piece import piece as Piece

class Tetris():
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[0 for x in range(width)] for y in range(height)]
        self.currentPiece = self.newPiece()
        self.isGameOver = False
        self.score = 0

    def newPiece(self):
        shape = random.choice(mn.SHAPES)
        print('creating new piece')
        return Piece(self.width//2,0,shape)

    def validMove(self, piece, x, y, rotation):
        for i, row in enumerate(piece.shape[(piece.rotation + rotation)%len(piece.shape)]):
            for j, cell in enumerate(row):
                if cell == '0':
                    try:
                        if ((self.grid[piece.y+i+y][piece.x+j+x]) != 0):
                            return False
                        if piece.x+j+x<0:
                            return False
                    except IndexError:
                        return False
        return True
        
    def clearLines(self):
        clearedLines = 0
        for i, row in enumerate(self.grid):
            if all(cell != 0 for cell in row):
                del self.grid[i]
                self.grid.insert(0, [0 for x in range(self.width)])
                clearedLines+=1
        return clearedLines
    
    def lockPiece(self, piece):
        print('locking piece...')
        for i, row in enumerate(piece.shape[piece.rotation%len(piece.shape)]):
            for j, cell in enumerate(row):
                if cell == '0':
                    self.grid[piece.y+i][piece.x+j] = piece.color
                    
        linesCleared = self.clearLines()
        self.score += 100 * linesCleared

        self.currentPiece = self.newPiece()

        if not self.validMove(self.currentPiece,0, 0, 0):
            self.isGameOver = True
            
        return linesCleared
        
    def updatePiece(self):
        if not self.isGameOver:
            if self.validMove(self.currentPiece, 0, 1, 0):
                self.currentPiece.y += 1
            else:
                self.lockPiece(self.currentPiece)
            

    def draw(self, screen):
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                pygame.draw.rect(screen, cell, pygame.Rect(j * mn.GRID_SIZE, i * mn.GRID_SIZE, mn.GRID_SIZE - 1, mn.GRID_SIZE - 1))

        if self.currentPiece:
            for i, row in enumerate(self.currentPiece.shape[self.currentPiece.rotation % len(self.currentPiece.shape)]):
                for j, cell in enumerate(row):
                    if cell == '0':
                        pygame.draw.rect(screen, self.currentPiece.color, ((self.currentPiece.x + j) * mn.GRID_SIZE, (self.currentPiece.y + i) * mn.GRID_SIZE, mn.GRID_SIZE - 1, mn.GRID_SIZE - 1))
