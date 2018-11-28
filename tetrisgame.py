import sys
import pygame
import copy
from random import randrange as rand

default_config = {
	'cell_size':	10,
	'cols':		    20,
	'rows':		    20,
	'delay':	    750,
	'maxfps':	    30,
    'numPieces':    5
    }

colors = [
    (0,   0,   0  ),
    (255, 0,   0  ),
    (0,   150, 0  ),
    (0,   0,   255),
    (255, 120, 0  ),
    (255, 255, 0  ),
    (180, 0,   255),
    (0,   220, 220),
    (255, 255, 255)
    ]

class tetrisPiece():

    config = default_config

    tetris_shapes = [
	[[1, 1, 1],
	 [0, 1, 0]],
	
	[[0, 2, 2],
	 [2, 2, 0]],
	
	[[3, 3, 0],
	 [0, 3, 3]],
	
	[[4, 0, 0],
	 [4, 4, 4]],
	
	[[0, 0, 5],
	 [5, 5, 5]],
	
	[[6, 6, 6, 6]],
	
	[[7, 7],
	 [7, 7]]
    ]

    pieceShape = []
    piece_x = 0
    piece_y = 0

    def __init__(self, startLoc = None, shape = None):
        if shape == None:
            self.assignRandomShape()
        else:
            self.pieceShape = shape

        if startLoc == None:
            self.piece_x = 0
        else:
            self.piece_x = startLoc

        self.piece_y = 0


    def rotateClockwise(self):
        return [ [ self.pieceShape[y][x]
                for y in range(len(self.pieceShape)) ]
            for x in range(len(self.pieceShape[0]) - 1, -1, -1) ]

    def assignRandomShape(self):
        self.pieceShape = self.tetris_shapes[rand(len(self.tetris_shapes))]

    #used for some collision operations
    def negatePiece(self):
        return [[val*-1 for val in row] for row in self.pieceShape]

    def testEquivalent(self, givenPiece):
        if givenPiece.piece_x == self.piece_x and givenPiece.piece_y == self.piece_y and givenPiece.pieceShape == self.pieceShape:
            return True
        return False
        
class tetrisBoard():

    board = []
    collList = []
    regenerateCollList = True

    config = default_config

    def __init__(self, config = None):
        self.new_board()
        if config != None:
            self.config = config

    def new_board(self):
        self.board = [ [ 0 for x in range(self.config['cols']) ] for y in range(self.config['rows']) ]

    def remove_row(self, row):
        del self.board[row]
        self.board = [[0 for i in range(self.config['cols'])]] + self.board
    
    def join_matrixes(self, mat1, mat2, mat2_off):
        off_x, off_y = mat2_off
        for cy, row in enumerate(mat2):
            for cx, val in enumerate(row):
                mat1[cy+off_y][cx+off_x] += val
        return mat1

    def placePiece(self, piece):
        self.board = self.join_matrixes(self.board, piece.pieceShape, (piece.piece_x, piece.piece_y))
    
    def checkRows(self):
        toRemove = []
        for index, item in enumerate(self.board):
            if 0 not in item:
                toRemove.append(index)
        
        for rowIndex in toRemove:
            self.remove_row(rowIndex)

        return len(toRemove)

    def checkCollision(self, piece):
        return self.checkCollisionOffset(piece, 0, 0)

    def checkCollisionMatrix(self, mat, offset):
        offsX = offset[0]
        offsY = offset[1]
        for cy, row in enumerate(mat):
            for cx, cell in enumerate(row):
                try:
                    if cell and self.board[ cy + offsY ][ cx + offsX ]:
                        return True
                    elif cx + offsX < 0:
                        return True
                except IndexError:
                    return True
        return False

    def checkCollisionOffset(self, piece, x_offs, y_offs):
        for cy, row in enumerate(piece.pieceShape):
            for cx, cell in enumerate(row):
                try:
                    if cell and self.board[ cy + piece.piece_y + y_offs][ cx + piece.piece_x + x_offs]:
                        return True
                    elif cx + piece.piece_x + x_offs < 0:
                        return True
                except IndexError:
                    return True
        return False

    #takes piece, along with list of all pieces
    def checkCollisionOffsetMultiPiece(self, piece, pieceList, x_offs, y_offs):
        if self.regenerateCollList:
            self.generateCollisionList(pieceList)

        #remove piece from collision map if it would have been factored in
            if piece in pieceList:
                self.collList = self.join_matrixes(self.collList, piece.negatePiece(), (piece.piece_x, piece.piece_y))

        #check collision against the generated list
        return self.checkCollisionGivenBoard(piece.pieceShape, self.collList, (x_offs+piece.piece_x, y_offs+piece.piece_y))

    def checkCollisionGivenBoard(self, pieceShape, board, offset):
        offsX = offset[0]
        offsY = offset[1]
        for cy, row in enumerate(pieceShape):
            for cx, cell in enumerate(row):
                try:
                    if cell and board[ cy + offsY][ cx + offsX]:
                        return True
                    elif cx + offsX < 0:
                        return True
                except IndexError:
                    return True
        return False

    #stores and returns a list of all collision blocks (Only needed for multiple pieces)
    def generateCollisionList(self, pieceList = None):

        self.collList = [[0 for col in range(len(self.board[0]))] for row in range(len(self.board))]

        for y, row in enumerate(self.collList):
            for x, item in enumerate(row):
                self.collList[y][x] += self.board[y][x]

        for piece in pieceList:
            self.collList = self.join_matrixes(self.collList, piece.pieceShape, (piece.piece_x, piece.piece_y))
        
        return self.collList

    def checkCollisionRotate(self, piece):
        return self.checkCollisionMatrix(piece.rotateClockwise(), (piece.piece_x, piece.piece_y))

    def checkCollisionRotateMultipiece(self, piece, pieceList):
        if self.regenerateCollList:
            self.generateCollisionList(pieceList)

            if piece in pieceList:
                self.collList = self.join_matrixes(self.collList, piece.negatePiece(), (piece.piece_x, piece.piece_y))

        return self.checkCollisionGivenBoard(piece.rotateClockwise(), self.collList, (piece.piece_x, piece.piece_y))
        
    def setBoardToColor(self):
        for y, row in enumerate(self.board):
            for x in enumerate(row):
                self.board[y][x[0]] = rand(1,7)

#holds board, pieces and score, contains functions for modifying state
class tetrisData():
    currentBoard = tetrisBoard()
    pieceList = list()
    config = default_config
    score = 0

    #Denotes if the last line elimination was a 'tetris'
    tetrisCount = 0

    def __init__(self, config = None):
        if config != None:
            self.config = config
        else:
            self.config = default_config
        
        self.currentBoard = tetrisBoard(self.config)
        self.pieceList = list()
        self.score = 0
    
    def landPiece(self, piece):
        if piece in self.pieceList:
            self.currentBoard.placePiece(piece)
            self.pieceList.remove(piece)
    
    def attemptAddPiece(self, shape = None, loc = None):
        if len(self.pieceList) < self.config['numPieces']:
            piece = tetrisPiece()
            if shape == None:
                piece.assignRandomShape()
            else:
                piece.pieceShape = shape

            if loc == None:
                piece.piece_x = rand(self.config['cols'] - (len(piece.pieceShape[0])-1))
            else:
                piece.piece_x = loc
            
            piece.piece_y = 0

            if self.config['numPieces'] > 1:
                if self.currentBoard.checkCollisionOffsetMultiPiece(piece, self.pieceList, 0, 0):
                    if len(self.pieceList) == 0:
                        return False #piece cannot be placed
                else:
                    self.pieceList.append(piece)
            else:
                if self.currentBoard.checkCollision(piece):
                    if len(self.pieceList) == 0:
                        return False #piece cannot be placed
                else:
                    self.pieceList.append(piece)
            
        return True
    
    def decodeScore(self, rows):
        if rows != 4:
            self.tetrisCount = 0
        if rows == 0:
            return 0
        elif rows == 1:
            return 100
        elif rows == 2:
            return 400
        elif rows == 3:
            return 900
        elif rows == 4:
            if self.tetrisCount != 0:
                self.tetrisCount += 1
                return 1200 * self.tetrisCount
            else:
                self.prevTetris = 1
                return 800
    
    def generateListBoard(self):
        tempBoard = [ [ 0 for x in range(self.config['cols']) ]
                for y in range(self.config['rows']) ]

        tempBoard = self.currentBoard.join_matrixes(tempBoard, self.currentBoard.board, (0,0))
        for piece in self.pieceList:
            tempBoard = self.currentBoard.join_matrixes(tempBoard, piece.pieceShape, (piece.piece_x, piece.piece_y))
        
        return tempBoard
    
    def printListBoard(self):
        listBoard = self.generateListBoard()
        for row in listBoard:
            print(row)
        print('\n\n')

    #return piece from list that matches given piece
    def getPieceMatch(self, givenPiece):
        for piece in self.pieceList:
            if piece.testEquivalent(givenPiece):
                return piece
        return None

#draws tetris game and relevant info
class tetrisView():
    boardMargin = 10
    displayArea = 50
    config = default_config

    def __init__(self):
        pygame.init()
        pygame.key.set_repeat(250,25)
        self.width = self.config['cell_size']*self.config['cols'] + 2 * self.boardMargin + self.displayArea
        self.height = self.config['cell_size']*self.config['rows'] + 4 * self.boardMargin

        self.boardWidth = self.config['cell_size']*self.config['cols']
        self.boardHeight = self.config['cell_size']*self.config['rows']

        self.borderTopRight = (self.boardMargin/2, self.boardMargin/2)
        self.borderTopLeft = (self.boardMargin*3/2 + self.boardWidth, self.boardMargin/2)
        self.borderBottomRight = (self.boardMargin/2, self.boardMargin*3/2 + self.boardHeight) 
        self.borderBottomLeft = (self.boardMargin*3/2 + self.boardWidth, self.boardMargin*3/2 + self.boardHeight)
        
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.event.set_blocked(pygame.MOUSEMOTION) 

    def drawCurrentGame(self, currentData):
        self.resetScreen()
        self.drawCurrentBoard(currentData)
        self.drawCurrentPieces(currentData)
        self.drawBorder(currentData)
        self.drawScore(str(currentData.score))

    def resetScreen(self):
        self.screen.fill((0,0,0))

    def drawCurrentBoard(self, currentData):
        for y, row in enumerate(currentData.currentBoard.board):
            for x, val in enumerate(row):
                if val:
                    pygame.draw.rect(
                        self.screen,
                        colors[val],
                        pygame.Rect(x * self.config['cell_size'] + self.boardMargin, 
                                    y * self.config['cell_size'] + self.boardMargin, 
                                    self.config['cell_size'], self.config['cell_size']) ,0)
                    if self.config['cell_size'] > 4:
                        pygame.draw.rect(
                            self.screen,
                            colors[8],
                            pygame.Rect( x * self.config['cell_size'] + self.boardMargin, 
                                        y * self.config['cell_size'] + self.boardMargin, 
                                        self.config['cell_size'], self.config['cell_size']) ,1)
                    if self.config['cell_size'] > 6:
                        pygame.draw.rect(
                            self.screen,
                            colors[0],
                            pygame.Rect( x * self.config['cell_size'] + self.boardMargin+1, 
                                        y * self.config['cell_size'] + self.boardMargin+1, 
                                        self.config['cell_size']-2, self.config['cell_size']-2) ,1)

    def drawBorder(self, currentData):
        pygame.draw.line(self.screen, colors[8], self.borderTopRight, self.borderTopLeft , 1)
        pygame.draw.line(self.screen, colors[8], self.borderTopRight, self.borderBottomRight , 1)
        pygame.draw.line(self.screen, colors[8], self.borderBottomLeft, self.borderTopLeft , 1)
        pygame.draw.line(self.screen, colors[8], self.borderBottomLeft, self.borderBottomRight , 1)
        
    def drawScore(self, score):
        for i, line in enumerate(score.splitlines()):
            msg_image =  pygame.font.Font(
                pygame.font.get_default_font(), 12).render(
                    line, False, (255,255,255), (0,0,0))
		
            msgim_center_x, msgim_center_y = msg_image.get_size()
            msgim_center_x //= 2
            msgim_center_y //= 2
		
            self.screen.blit(msg_image, (
            self.boardWidth + 2*self.boardMargin,
            self.boardMargin+i*22))

    def draw_matrix(self, matrix, offset):
        off_x, off_y  = offset
        for y, row in enumerate(matrix):
            for x, val in enumerate(row):
                if val:
                    pygame.draw.rect(
                        self.screen,
                        colors[val],
                        pygame.Rect(
                            (off_x+x) *
                                self.config['cell_size'],
                            (off_y+y) *
                                self.config['cell_size'], 
                            self.config['cell_size'],
                            self.config['cell_size']),0)

    def drawCurrentPieces(self, currentData):
        for piece in currentData.pieceList:
            self.drawPiece(piece)

    def drawPiece(self, piece):
        for y, row in enumerate(piece.pieceShape):
            for x, val in enumerate(row):
                if val:
                    pygame.draw.rect(
                        self.screen,
                        colors[val],
                        pygame.Rect( (x + piece.piece_x) * self.config['cell_size'] + self.boardMargin, 
                                     (y + piece.piece_y) * self.config['cell_size'] + self.boardMargin, 
                                     self.config['cell_size'], self.config['cell_size']) ,0)
                    if self.config['cell_size'] > 4:
                        pygame.draw.rect(
                            self.screen,
                            colors[8],
                            pygame.Rect( (x + piece.piece_x) * self.config['cell_size'] + self.boardMargin, 
                                        (y + piece.piece_y) * self.config['cell_size'] + self.boardMargin, 
                                        self.config['cell_size'], self.config['cell_size']) ,1)
                    if self.config['cell_size'] > 6:
                        pygame.draw.rect(
                            self.screen,
                            colors[0],
                            pygame.Rect( (x + piece.piece_x) * self.config['cell_size'] + self.boardMargin+1, 
                                        (y + piece.piece_y) * self.config['cell_size'] + self.boardMargin+1, 
                                        self.config['cell_size']-2, self.config['cell_size']-2) ,1)
    
#issues commands to each piece
class pieceController():

    possibleMoves = {'LEFT':False,'RIGHT':False,'DOWN':False,'UP':False}

    def getMoves(self, piece, board):
        moves = dict()
        if not board.checkCollisionOffset(piece, 1, 0):
            moves['RIGHT'] = True
        else:
            moves['RIGHT'] = False

        if not board.checkCollisionOffset(piece, -1, 0):
            moves['LEFT'] = True
        else:
            moves['LEFT'] = False

        if not board.checkCollisionOffset(piece, 0 , 1):
            moves['DOWN'] = True
        else:
            moves['DOWN'] = False

        if not board.checkCollisionRotate(piece):
            moves['UP'] = True
        else:
            moves['UP'] = False

        self.possibleMoves = moves
        return moves

    def getMovesMultipiece(self, piece, pieceList, board):
        moves = dict()

        #Only need to generate collision list on first offset check.
        board.regenerateCollList = True
        if not board.checkCollisionOffsetMultiPiece(piece, pieceList, 1, 0):
            moves['RIGHT'] = True
        else:
            moves['RIGHT'] = False

        board.regenerateCollList = False
        if not board.checkCollisionOffsetMultiPiece(piece, pieceList, -1, 0):
            moves['LEFT'] = True
        else:
            moves['LEFT'] = False

        if not board.checkCollisionOffsetMultiPiece(piece, pieceList, 0 , 1):
            moves['DOWN'] = True
        else:
            moves['DOWN'] = False

        if not board.checkCollisionRotateMultipiece(piece, pieceList):
            moves['UP'] = True
        else:
            moves['UP'] = False

        board.regenerateCollList = True

        self.possibleMoves = moves
        return moves
    
    def applyMove(self, piece, board, move):
        if self.possibleMoves[move]:
            if move == 'RIGHT':
                piece.piece_x += 1
            elif move =='LEFT':
                piece.piece_x -= 1
            elif move =='DOWN':
                piece.piece_y += 1
            elif move =='UP':
                piece.pieceShape = piece.rotateClockwise()
            return True
        else:
            return False

    def combinedApply(self, piece, board, move):
        self.getMoves(piece, board)
        return self.applyMove(piece, board, move)
    
    def combinedApplyMultipiece(self, piece, pieceList, board, move):
        self.getMovesMultipiece(piece, pieceList, board)
        return self.applyMove(piece, board, move)

#gets moves for piece either from human input or external function.
class moveProvider():
    clock = pygame.time.Clock()
    key_actions = {
			'ESCAPE',
			'LEFT',
			'RIGHT',
			'DOWN',
			'UP',
			'p',
			'SPACE'
		}

    def keyboardMove(self):
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    for key in self.key_actions:
                        if event.key == eval("pygame.K_"+key):
                            return key
                        elif event.type == pygame.QUIT:
                            sys.quit()

                elif event.type == pygame.USEREVENT+1:
                    return 'DOWN'
        return 'NONE'
    
#evaluates game states
class evaluator():
    currentSef = 0
    tempData = tetrisData()
    currentData = []

    def __init__(self, sef = None, tData = None):
        if sef != None:
            self.currentSef = sef
        if tData != None:
            self.currentData = tData

    def evaluate(self, tData = None):
        sefs = {
            0 : self.sef0,
            1 : self.sef1,
            2 : self.sef2,
            3 : self.sef3,
            4 : self.sef4,
            5 : self.sef5
        }

        if tData != None:
            self.currentData = tData


        return sefs[self.currentSef]()

    #return a duplicate of the gameboard where every piece is projected downward
    def projectPieces(self):
        tempGame = tetrisGame(self.currentData.config)
        tempGame.manual = True
        tempGame.display = False
        tempGame.gameData = copy.deepcopy(self.currentData)
        while tempGame.gameData.pieceList != []:
            tempGame.drop()

        return tempGame.gameData.currentBoard.board

    def getSefData(self, tData):
        if tData == None:
            return self.currentData
        else:
            return tData

    #amalgam of sefs with projected pieces and weighted combinations
    def sef0(self):
        self.tempData.currentBoard.board = self.projectPieces()
        #self.currentData.printListBoard()

        #scores and weights of each function found via genetic algorithm given by Yiyuan Lee at:
        #https://codemyroad.wordpress.com/2013/04/14/tetris-ai-the-near-perfect-player/
        return self.sef2(self.tempData) * -0.510066 + self.sef3(self.tempData) * 0.760666 + self.sef4(self.tempData) * -0.35663 + self.sef5(self.tempData) * -0.184483

    #Board height
    def sef1(self, tData = None):
        sefData = self.getSefData(tData)
        height = 0
        for row in reversed(sefData.currentBoard.board):
            if all(val == 0 for val in row):
                return height
            else:
                height += 1
        return height
        
    #aggregate height
    def sef2(self, tData = None):
        sefData = self.getSefData(tData)
        total = 0
        colHeight = 0
        for x in range(len(sefData.currentBoard.board[0])):
            for y in reversed(range(len(sefData.currentBoard.board))):
                if sefData.currentBoard.board[y][x] != 0:
                    colHeight = len(sefData.currentBoard.board) - y
            total += colHeight
            colHeight = 0
        return total

    #number of lines
    def sef3(self, tData = None):
        sefData = self.getSefData(tData)
        total = 0
        for x in sefData.currentBoard.board:
            if 0 not in x:
                total += 1
        return total

    #Number of holes
    def sef4(self, tData = None):
        sefData = self.getSefData(tData)
        total = 0
        holes = 0
        for x in range(len(sefData.currentBoard.board[0])):
            for y in reversed(range(len(sefData.currentBoard.board))):
                if sefData.currentBoard.board[y][x] == 0:
                    holes += 1
                if sefData.currentBoard.board[y][x] != 0:
                    total += holes
                    holes = 0
            holes = 0
        return total

    #Bumpiness
    def sef5(self, tData = None):
        sefData = self.getSefData(tData)
        total = 0
        colHeight = 0
        prevColHeight = 0
        xRange = len(sefData.currentBoard.board[0])
        yRange = len(sefData.currentBoard.board)
        for x in range(xRange):
            for y in reversed(range(yRange)):
                if sefData.currentBoard.board[y][x] != 0:
                    colHeight = yRange - y
            total += abs(colHeight - prevColHeight)
            prevColHeight = colHeight
            colHeight = 0
        return total

#Makes moves autonomously
class AIPlayer():

    AIActions = [
        'LEFT',
        'RIGHT',
        'DOWN',
        'UP'
    ]

    scoreEval = evaluator(0)
    controller = pieceController()

    #returns a move based on game state, searchning to a particular depth
    #TODO: Search deeper than 1
    def chooseMove(self, piece, tData, depth = 1):
        evaluatedStates = dict()
        statesToEvaluate = [tData.generateListBoard()]
        currentDepth = 0
        controller = pieceController()

        if piece not in tData.pieceList:
            return None
        
        if len(tData.pieceList) > 1:
            controller.getMovesMultipiece(piece, tData.pieceList, tData.currentBoard)
        else:
            controller.getMoves(piece, tData.currentBoard)

        bestScore = -100000
        bestMove = 'NONE'
        for move, value in controller.possibleMoves.items():
            if value:
                score = self.scoreSingleMove(tData, piece, move)[0]
                if score > bestScore:
                    bestScore = score
                    bestMove = move

        return bestMove


    def scoreSingleMove(self, tData, piece, move):
        self.scoreEval.currentData = tData
        if piece not in tData.pieceList:
            return self.scoreEval.evaluate(tData), tData
        
        if len(tData.pieceList) > 1:
            self.controller.getMovesMultipiece(piece, tData.pieceList, tData.currentBoard)
        else:
            self.controller.getMoves(piece, tData.currentBoard)
        
        if not self.controller.possibleMoves[move]:
            return self.scoreEval.evaluate(tData), tData
        
        dataCopy = copy.deepcopy(tData)
        pieceCopy = dataCopy.getPieceMatch(piece)
        self.controller.applyMove(pieceCopy, dataCopy.currentBoard, move)

        return self.scoreEval.evaluate(dataCopy), dataCopy

    def makeRandomMove(self):
        return self.AIActions[rand(4)]
    
    
    #move piece to left and right max in all different orientations to find best one.
    #only guaranteed to find best when 1 piece is in play.
    def bruteForceBest(self, tetrisData):
        None

#Manages progression of entire game
class tetrisGame():
    config = default_config
    view = tetrisView()
    controller = pieceController()
    gameData = tetrisData() 
    mover = moveProvider()
    gameOver = False
    paused = False
    display = True
    manual = False
    dont_burn_my_cpu = pygame.time.Clock()
    maxNDM = 3

    #counts how many Non-down moves each piece made
    moveCounter = dict()

    autoPlayer = AIPlayer()

    def __init__(self, config = None):
        if config != None:
            self.config = config
        
    def run(self):
        pygame.time.set_timer(pygame.USEREVENT+1, self.config['delay'])
        while 1: #not self.gameOver:
            self.advanceGame()
    
    def advanceGame(self):

        #add/replenish pieces
        self.gameOver = self.gameData.attemptAddPiece(None, None)

        #display game state, or metrics if AI is running.
        if self.display:
            self.displayGame()

        if not self.gameOver:
            self.resetGame()
            return

        #get moves from controller (Human or AI)
        self.movePieces()

        #update score and remove lines
        self.gameData.score += self.gameData.decodeScore(self.gameData.currentBoard.checkRows())
     
    def displayGame(self):
        self.view.drawCurrentGame(self.gameData)
        pygame.display.update()
        self.dont_burn_my_cpu.tick(self.config['maxfps'])

    def movePieces(self):
        for piece in self.gameData.pieceList:
            command = ''
            if self.manual:
                command = self.mover.keyboardMove()
            else:
                command = self.autoPlayer.chooseMove(piece, self.gameData)
                #command = self.autoPlayer.makeRandomMove()
                if self.processKeyInput() == 'ESCAPE':
                    command = 'ESCAPE'
                #get command from AI controller
            
            if command == 'ESCAPE':
                sys.exit()

            if command != 'NONE':
                if len(self.gameData.pieceList) > 1:
                    self.controller.getMovesMultipiece(piece, self.gameData.pieceList, self.gameData.currentBoard)
                else:
                    self.controller.getMoves(piece, self.gameData.currentBoard)

                if piece in self.moveCounter:
                    self.moveCounter[piece] += 1
                else:
                    self.moveCounter[piece] = 0

                if command == 'DOWN':
                    self.moveCounter[piece] = 0
                elif self.moveCounter[piece] > self.maxNDM:
                    self.moveCounter[piece] = 0
                    command = 'DOWN'

                if command == 'DOWN' and not self.controller.possibleMoves['DOWN']:
                    #land piece
                    #keeps pieces from landing because of downward facing multi-piece collision
                    if len(self.gameData.pieceList) > 1:
                        self.controller.getMoves(piece, self.gameData.currentBoard)
                        if not self.controller.possibleMoves['DOWN']:
                            self.gameData.landPiece(piece)
                    else:
                        self.gameData.landPiece(piece)
                        del self.moveCounter[piece]
                else:
                    self.controller.applyMove(piece, self.gameData.currentBoard, command)

    #only used for AI projections of pieces
    def drop(self):
        for piece in self.gameData.pieceList:
            if len(self.gameData.pieceList) > 1:
                self.controller.getMovesMultipiece(piece, self.gameData.pieceList, self.gameData.currentBoard)
            else:
                self.controller.getMoves(piece, self.gameData.currentBoard)
            
            if not self.controller.possibleMoves['DOWN']:
                #land piece
                #keeps pieces from landing because of downward facing multi-piece collision
                if len(self.gameData.pieceList) > 1:
                    self.controller.getMoves(piece, self.gameData.currentBoard)
                    if not self.controller.possibleMoves['DOWN']:
                        self.gameData.landPiece(piece)
                else:
                    self.gameData.landPiece(piece)
            else:
                self.controller.applyMove(piece, self.gameData.currentBoard, 'DOWN')
                
    def processKeyInput(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                for key in self.mover.key_actions:
                    if event.key == eval("pygame.K_"+key):
                        return key
                    elif event.type == pygame.QUIT:
                        sys.quit()
        return 'NONE'
                        

    def resetGame(self):
        self.gameData = tetrisData()
        self.gameOver = False



#testGame = tetrisGame()
#testGame.run()