import unittest
from tetrisgame import *

class TetrisPieceTests(unittest.TestCase):

    def test_testPieceInit(self):
        testval = tetrisPiece(5, [[1]])

        expected = 5
        actual = testval.piece_x

        self.assertEqual(expected, actual)

    def test_testPieceInit_2(self):
        testval = tetrisPiece(5, [[1]])

        expected = [[1]]
        actual = testval.pieceShape

        self.assertEqual(expected, actual)

    def test_testPieceAssigns(self):
        testVal = tetrisPiece()
        testVal.assignRandomShape()
        expected = True

        actual = len(testVal.pieceShape) > 0 and len(testVal.pieceShape[0]) > 0

        self.assertEqual(expected, actual)

    def test_testRotatePiece(self):
        testVal = tetrisPiece()
        testVal.pieceShape = [[1],[1]]
        expected = [[1,1]]

        actual = testVal.rotateClockwise()

        self.assertEqual(actual, expected)

    def test_testNegatePiece(self):
        testVal = tetrisPiece()
        testVal.pieceShape = [[1, 1, 0], 
                              [0, 1, 1]]
        expected = [[-1, -1,  0], 
                    [0,  -1, -1]]

        actual = testVal.negatePiece()

        self.assertEqual(actual, expected)


class TetrisBoardTests(unittest.TestCase):

    def test_testNewBoard(self):
        testVal = tetrisBoard()
        
        self.assertGreater(len(testVal.board), 0)
    
    def test_removeRow(self):
        testVal = tetrisBoard()
        expected = True

        testVal.board[0] = [1]
        testVal.remove_row(0)
        actual = [1] not in testVal.board

        self.assertEqual(expected, actual)

    def test_joinMatricies(self):
        testBoard = tetrisBoard()
        block = [[1,1,0],
                 [0,1,1]]
        board = [[0,0,0,0],
                 [0,0,0,0],
                 [0,0,0,0]]
        expected = [[1,1,0,0],
                    [0,1,1,0],
                    [0,0,0,0]]          

        actual = testBoard.join_matrixes(board, block, (0,0))

        self.assertEqual(expected, actual)

    def test_testCheckCollision_1(self):
        testBoard = tetrisBoard()
        testPiece = tetrisPiece(0, [[1,1]])
        testBoard.board = [
            [0,0],
            [1,1]]

        expected = False
        actual = testBoard.checkCollision(testPiece)

        self.assertEqual(expected, actual)

    def test_testCheckCollision_2(self):
        testBoard = tetrisBoard()
        testPiece = tetrisPiece(0, [[1,1]])
        testBoard.board = [
            [1,0],
            [1,0]]

        expected = True
        actual = testBoard.checkCollision(testPiece)

        self.assertEqual(expected, actual)
    
    def test_testCheckRows(self):
        testBoard = tetrisBoard({'cols':3})
        testBoard.board = [
            [1,0,0],
            [1,0,0],
            [1,1,1]]
        expected = [
            [0,0,0],
            [1,0,0],
            [1,0,0],
        ]
        
        testBoard.checkRows()
        actual = testBoard.board

        self.assertEqual(expected, actual)

    def test_testPlacePiece(self):
        testPiece = tetrisPiece(0, [[1,1]])
        testBoard = tetrisBoard({'cols':3})
        testBoard.board = [
            [0,0,0],
            [0,0,0],
            [0,0,0]]
        expected = [
            [1,1,0],
            [0,0,0],
            [0,0,0],
        ]

        testBoard.placePiece(testPiece)

        actual = testBoard.board

        self.assertEqual(actual, expected)

    def test_checkCollisionOffsetDoesntMutate(self):
        testPiece = tetrisPiece(0, [[1]])
        testBoard = tetrisBoard({'cols':3})
        testBoard.board = [
            [0,0,0],
            [0,0,0],
            [0,0,0]
        ]

        expected = testPiece
        testBoard.checkCollisionOffset(testPiece, 1, 1)
        actual = testPiece

        self.assertEqual(actual, expected)

    def test_checkCollisionOffsetRightSpace(self):
        testPiece = tetrisPiece(0, [[1]])
        testBoard = tetrisBoard({'cols':3})
        testBoard.board = [
            [0,0,0],
            [0,0,0],
            [0,0,0]]

        expected = False
        actual = testBoard.checkCollisionOffset(testPiece, 1, 0)

        self.assertEqual(actual, expected)

    def test_checkCollisionOffsetRightEdge(self):
        testPiece = tetrisPiece(0, [[1,1,1]])
        testBoard = tetrisBoard({'cols':3})
        testBoard.board = [
            [0,0,0],
            [0,0,0],
            [0,0,0]]
        expected = True

        actual = testBoard.checkCollisionOffset(testPiece, 1, 0)

        self.assertEqual(actual, expected)

    def test_checkCollisionOffsetBelow(self):
        testPiece = tetrisPiece(0, [[1,1]])
        testBoard = tetrisBoard({'cols':3})
        testBoard.board = [
            [0,0,0],
            [0,1,0],
            [0,0,0]]
        expected = True

        actual = testBoard.checkCollisionOffset(testPiece, 0, 1)

        self.assertEqual(actual, expected)

    def test_checkCollisionOffsetRight(self):
        testPiece = tetrisPiece(0, [[1,1]])
        testBoard = tetrisBoard({'cols':3})
        testBoard.board = [
            [0,0,1],
            [0,0,0],
            [0,0,0]]
        expected = True

        actual = testBoard.checkCollisionOffset(testPiece, 1, 0)

        self.assertEqual(actual, expected)

    def test_testGenerateCollisionBoard_1(self):
        testPiece_1 = tetrisPiece()
        testPiece_2 = tetrisPiece()
        testPiece_3 = tetrisPiece()
        testData = tetrisData()
        testBoard = tetrisBoard({'cols':3})
        testBoard.board = [
            [0,0,0],
            [0,0,0],
            [0,0,0]
            ]
        testPiece_1.pieceShape = [[1, 2]]
        testPiece_2.pieceShape = [[3]]
        testPiece_3.pieceShape = [[5]]
        testPiece_1.piece_x = 0
        testPiece_2.piece_x = 1
        testPiece_3.piece_x = 2
        testPiece_1.piece_y = 2
        testPiece_2.piece_y = 0
        testPiece_3.piece_y = 1
        testData.currentBoard = testBoard
        testData.pieceList.append(testPiece_1)
        testData.pieceList.append(testPiece_2)
        testData.pieceList.append(testPiece_3)
        expected = [
            [0,3,0],
            [0,0,5],
            [1,2,0]
            ]

        actual = testData.currentBoard.generateCollisionList(testData.pieceList)

        self.assertEqual(actual, expected)

    def test_testGenerateCollisionBoard_2(self):
        testData = tetrisData()
        testBoard = tetrisBoard({'cols':3})
        testPiece_1 = tetrisPiece(0, [[1, 2]])
        testBoard.board = [
            [0,0,0],
            [0,0,0],
            [0,0,0]
            ]
        testData.currentBoard = testBoard
        testData.pieceList.append(testPiece_1)
        expected = [
            [1,2,0],
            [0,0,0],
            [0,0,0]
            ]

        actual = testData.currentBoard.generateCollisionList(testData.pieceList)

        self.assertEqual(actual, expected)

    def test_testGenerateCollisionBoard_3(self):
        testData = tetrisData()
        testBoard = tetrisBoard({'cols':3})
        testBoard.board = [
            [0,0,0],
            [0,0,0],
            [0,0,0]
            ]
        testData.currentBoard = testBoard
        expected = [
            [0,0,0],
            [0,0,0],
            [0,0,0]
            ]

        actual = testData.currentBoard.generateCollisionList(testData.pieceList)

        self.assertEqual(actual, expected)
    
    def test_testGenerateCollisionBoard_4(self):
        #ensure collision list does not mutate board
        testData = tetrisData()
        testBoard = tetrisBoard({'cols':3})
        testPiece = tetrisPiece(0, [[1,1,1]])
        testData.pieceList.append(testPiece)
        testBoard.board = [
            [0,0,0],
            [0,0,0],
            [0,0,0]
            ]
        testData.currentBoard = testBoard
        expected = [
            [0,0,0],
            [0,0,0],
            [0,0,0]
            ]

        testData.currentBoard.generateCollisionList(testData.pieceList)
        actual = testBoard.board

        self.assertEqual(actual, expected)

    def test_testGenerateCheckCollisionGivenBoard(self):
        testBoard = tetrisBoard()
        testPiece = tetrisPiece()
        testPiece.pieceShape = [[1,1,0],[0,1,1]]
        testPiece.piece_x = 0
        testPiece.piece_y = 0
        testBoard.board = [
            [0,0,0,1],
            [0,0,0,1],
            [1,1,1,1]
            ]
        expected = False

        actual = testBoard.checkCollisionGivenBoard(testPiece.pieceShape, testBoard.board, (testPiece.piece_x, testPiece.piece_y))

        self.assertEqual(actual, expected)
    
    def test_testGenerateCheckCollisionGivenBoard_1(self):
        testBoard = tetrisBoard()
        testPiece = tetrisPiece()
        testPiece.pieceShape = [[1,1,0],[0,1,1]]
        testPiece.piece_x = 1
        testPiece.piece_y = 0
        testBoard.board = [
            [0,0,0,1],
            [0,0,0,1],
            [1,1,1,1]
            ]
        expected = True

        actual = testBoard.checkCollisionGivenBoard(testPiece.pieceShape, testBoard.board, (testPiece.piece_x, testPiece.piece_y))

        self.assertEqual(actual, expected)

    def test_testGenerateCheckCollisionGivenBoard_2(self):
        testBoard = tetrisBoard()
        testPiece = tetrisPiece()
        testPiece.pieceShape = [[1,1,0],[0,1,1]]
        testPiece.piece_x = 0
        testPiece.piece_y = 1
        testBoard.board = [
            [0,0,0,1],
            [0,0,0,1],
            [1,1,1,1]
            ]
        expected = True

        actual = testBoard.checkCollisionGivenBoard(testPiece.pieceShape, testBoard.board, (testPiece.piece_x, testPiece.piece_y))

        self.assertEqual(actual, expected)
        
    def test_testCheckCollisionOffsetMultiPiece(self):
        testPiece_1 = tetrisPiece()
        testPiece_2 = tetrisPiece()
        testBoard = tetrisBoard({'cols':4})
        testData = tetrisData
        testBoard.board = [
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0]]

        testData.currentBoard = testBoard
        testPiece_1.pieceShape = [[1,1]]
        testPiece_2.pieceShape = [[0,1],[1,1]]
        testPiece_1.piece_x = 1
        testPiece_2.piece_x = 2
        testData.pieceList.append(testPiece_1)
        testData.pieceList.append(testPiece_2)
        
        expected = True

        actual = testBoard.checkCollisionOffsetMultiPiece(testPiece_1, testData.pieceList, 1, 0)

        self.assertEqual(actual, expected)

    def test_testCheckCollisionOffsetMultiPiece_1(self):
        testPiece_1 = tetrisPiece()
        testPiece_2 = tetrisPiece()
        testBoard = tetrisBoard({'cols':4})
        testData = tetrisData()
        testBoard.board = [
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0]]

        testData.currentBoard = testBoard
        testPiece_1.pieceShape = [[1,1]]
        testPiece_2.pieceShape = [[0,1],[1,1]]
        testPiece_1.piece_x = 1
        testPiece_2.piece_x = 2
        testData.pieceList.append(testPiece_1)
        testData.pieceList.append(testPiece_2)
        
        expected = True

        actual = testBoard.checkCollisionOffsetMultiPiece(testPiece_1, testData.pieceList, 0, 1)

        self.assertEqual(actual, expected)

    def test_testCheckCollisionOffsetMultiPiece_2(self):
        testPiece_1 = tetrisPiece()
        testPiece_2 = tetrisPiece()
        testBoard = tetrisBoard({'cols':4})
        testData = tetrisData()
        testBoard.board = [
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0]]

        testData.currentBoard = testBoard
        testPiece_1.pieceShape = [[1,1]]
        testPiece_2.pieceShape = [[0,1],[1,1]]
        testPiece_1.piece_x = 1
        testPiece_2.piece_x = 2
        testData.pieceList.append(testPiece_1)
        testData.pieceList.append(testPiece_2)
        
        expected = False

        actual = testBoard.checkCollisionOffsetMultiPiece(testPiece_1, testData.pieceList, 0, 0)

        self.assertEqual(actual, expected)

    def test_testCheckCollisionOffsetMultiPiece_3(self):
        testPiece_1 = tetrisPiece()
        testPiece_2 = tetrisPiece()
        testBoard = tetrisBoard({'cols':4})
        testData = tetrisData()
        testBoard.board = [
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0]]

        testData.currentBoard = testBoard
        testPiece_1.pieceShape = [[1,1]]
        testPiece_2.pieceShape = [[0,1],[1,1]]
        testPiece_1.piece_x = 1
        testPiece_2.piece_x = 2
        testData.pieceList.append(testPiece_1)
        testData.pieceList.append(testPiece_2)
        expected = False

        actual = testBoard.checkCollisionOffsetMultiPiece(testPiece_1, testData.pieceList, -1, 0)

        self.assertEqual(actual, expected)

    def test_testCheckCollisionOffsetMultiPiece_4(self):
        testPiece_1 = tetrisPiece()
        testBoard = tetrisBoard({'cols':4})
        testData = tetrisData()
        testBoard.board = [
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0]]

        testData.currentBoard = testBoard
        testPiece_1.pieceShape = [[1,1]]
        testPiece_1.piece_x = 1
        testData.pieceList.append(testPiece_1)
        expected = False

        actual = testBoard.checkCollisionOffsetMultiPiece(testPiece_1, testData.pieceList, -1, 0)

        self.assertEqual(actual, expected)

    def test_testCheckCollisionOffsetMultiPiece_5(self):
        testPiece_1 = tetrisPiece()
        testBoard = tetrisBoard({'cols':4})
        testData = tetrisData()
        testBoard.board = [
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0]]

        testData.currentBoard = testBoard
        testPiece_1.pieceShape = [[1,1]]
        testPiece_1.piece_x = 1
        testData.pieceList.append(testPiece_1)
        expected = False

        actual = testBoard.checkCollisionOffsetMultiPiece(testPiece_1, testData.pieceList, 0, 1)

        self.assertEqual(actual, expected)

    def test_testCollListNegationRemoval_1(self):
        testPiece_1 = tetrisPiece()
        testPiece_2 = tetrisPiece()
        testPiece_3 = tetrisPiece()
        testData = tetrisData()
        testBoard = tetrisBoard({'cols':3})
        testBoard.board = [
            [0,0,0],
            [0,0,0],
            [0,0,0]
            ]
        testPiece_1.pieceShape = [[1, 2]]
        testPiece_2.pieceShape = [[3]]
        testPiece_3.pieceShape = [[5]]
        testPiece_1.piece_x = 0
        testPiece_2.piece_x = 1
        testPiece_3.piece_x = 2
        testPiece_1.piece_y = 2
        testPiece_2.piece_y = 0
        testPiece_3.piece_y = 1
        testData.currentBoard = testBoard
        testData.pieceList.append(testPiece_1)
        testData.pieceList.append(testPiece_2)
        testData.pieceList.append(testPiece_3)
        expected = [
            [0,3,0],
            [0,0,5],
            [0,0,0]
            ]

        collList = testData.currentBoard.generateCollisionList(testData.pieceList)
        collList = testData.currentBoard.join_matrixes(collList, testPiece_1.negatePiece(), (testPiece_1.piece_x,testPiece_1.piece_y))
        actual = collList

        self.assertEqual(actual, expected)


class tetrisDataTests(unittest.TestCase):
    None
    
class PieceControllerTests(unittest.TestCase):
    def test_testGetMoves_1(self):
        testBoard = tetrisBoard({'cols':3})
        testPiece = tetrisPiece()
        testcontroller = pieceController()
        testBoard.board = [
            [0,0,0],
            [0,0,0],
            [0,0,0]]
        testPiece.pieceShape = [[1]]
        testPiece.piece_x = 1
        expected = {'LEFT':True,'RIGHT':True,'DOWN':True,'UP':True}
        
        actual = testcontroller.getMoves(testPiece, testBoard)

        self.assertEqual(expected, actual)

    def test_testGetMoves_2(self):
        testBoard = tetrisBoard({'cols':3})
        testPiece = tetrisPiece()
        testcontroller = pieceController()
        testBoard.board = [
            [0,0,0],
            [0,0,0],
            [0,1,0]]
        testPiece.pieceShape = [[1]]
        testPiece.piece_x = 1
        testPiece.piece_y = 1
        expected = {'LEFT':True,'RIGHT':True,'DOWN':False,'UP':True}

        actual = testcontroller.getMoves(testPiece, testBoard)

        self.assertEqual(expected, actual)

    def test_testGetMoves_3(self):
        testBoard = tetrisBoard({'cols':3})
        testPiece = tetrisPiece()
        testcontroller = pieceController()
        testBoard.board = [
            [0,0,0],
            [0,1,0],
            [0,1,0]]
        testPiece.pieceShape = [[1],[1]]
        testPiece.piece_x = 2
        testPiece.piece_y = 0
        expected = {'LEFT':False,'RIGHT':False,'DOWN':True,'UP':False}

        actual = testcontroller.getMoves(testPiece, testBoard)

        self.assertEqual(expected, actual)

    def test_testApplyMoveRight(self):
        testBoard = tetrisBoard({'cols':3})
        testPiece = tetrisPiece()
        testcontroller = pieceController()
        testBoard.board = [
            [0,0,0],
            [0,0,0],
            [0,0,0]
        ]
        testPiece.pieceShape = [[1]]
        testPiece.piece_x = 0
        expected = 1

        testcontroller.combinedApply(testPiece, testBoard, 'RIGHT')
        actual = testPiece.piece_x

        self.assertEqual(expected, actual)

    def test_testApplyMoveRightWall(self):
        testBoard = tetrisBoard({'cols':3})
        testPiece = tetrisPiece()
        testcontroller = pieceController()
        testBoard.board = [
            [0,0,0],
            [0,0,0],
            [0,0,0]
        ]
        testPiece.pieceShape = [[1]]
        testPiece.piece_x = 2
        expected = 2

        testcontroller.applyMove(testPiece, testBoard, 'RIGHT')
        actual = testPiece.piece_x

        self.assertEqual(expected, actual)

    def test_testApplyMoveRightWall_2(self):
        testBoard = tetrisBoard({'cols':3})
        testPiece = tetrisPiece()
        testcontroller = pieceController()
        testBoard.board = [
            [0,0,0],
            [0,0,0],
            [0,0,0]
        ]
        testPiece.pieceShape = [[1]]
        testPiece.piece_x = 0
        expected = 2
        
        testcontroller.combinedApply(testPiece, testBoard, 'RIGHT')
        testcontroller.combinedApply(testPiece, testBoard, 'RIGHT')
        testcontroller.combinedApply(testPiece, testBoard, 'RIGHT')
        testcontroller.combinedApply(testPiece, testBoard, 'RIGHT')
        actual = testPiece.piece_x

        self.assertEqual(expected, actual)

    def test_testApplyMoveLeftWall_1(self):
        testBoard = tetrisBoard({'cols':3})
        testPiece = tetrisPiece()
        testcontroller = pieceController()
        testBoard.board = [
            [0,0,0],
            [0,0,0],
            [0,0,0]
        ]
        testPiece.pieceShape = [[1]]
        testPiece.piece_x = 1
        expected = 0

        testcontroller.combinedApply(testPiece, testBoard, 'LEFT')
        testcontroller.combinedApply(testPiece, testBoard, 'LEFT')
        testcontroller.combinedApply(testPiece, testBoard, 'LEFT')
        testcontroller.combinedApply(testPiece, testBoard, 'LEFT')
        actual = testPiece.piece_x

        self.assertEqual(expected, actual)

    def test_testGetMovesMultipiece_1(self):
        testBoard = tetrisBoard({'cols':3})
        testPiece_1 = tetrisPiece()
        testPiece_2 = tetrisPiece()
        testcontroller = pieceController()
        testBoard.board = [
            [0,0,0],
            [0,0,0],
            [0,0,0]]
        testPiece_1.pieceShape = [[1]]
        testPiece_2.pieceShape = [[1]]
        testPiece_1.piece_x = 0
        testPiece_2.piece_x = 1
        testPiece_1.piece_y = 0
        testPiece_2.piece_y = 0
        expected = {'LEFT':False,'RIGHT':False,'DOWN':True,'UP':True}

        actual = testcontroller.getMovesMultipiece(testPiece_1, [testPiece_1, testPiece_2], testBoard)

        self.assertEqual(expected, actual)
    
    def test_testGetMovesMultipiece_2(self):
        testBoard = tetrisBoard({'cols':3})
        testPiece_1 = tetrisPiece()
        testPiece_2 = tetrisPiece()
        testcontroller = pieceController()
        testBoard.board = [
            [0,0,0],
            [0,0,0],
            [0,0,0]]
        testPiece_1.pieceShape = [[1], [1]]
        testPiece_2.pieceShape = [[1]]
        testPiece_1.piece_x = 0
        testPiece_2.piece_x = 1
        testPiece_1.piece_y = 0
        testPiece_2.piece_y = 0
        expected = {'LEFT':False,'RIGHT':False,'DOWN':True,'UP':False}

        actual = testcontroller.getMovesMultipiece(testPiece_1, [testPiece_1, testPiece_2], testBoard)

        self.assertEqual(expected, actual)

    def test_testGetMovesMultipiece_3(self):
        testBoard = tetrisBoard({'cols':4})
        testPiece_1 = tetrisPiece()
        testPiece_2 = tetrisPiece()
        testcontroller = pieceController()
        testBoard.board = [
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0]]
        testPiece_1.pieceShape = [[1, 1]]
        testPiece_2.pieceShape = [[1]]
        testPiece_1.piece_x = 1
        testPiece_2.piece_x = 0
        testPiece_1.piece_y = 1
        testPiece_2.piece_y = 1
        expected = {'LEFT':False,'RIGHT':True,'DOWN':True,'UP':True}

        actual = testcontroller.getMovesMultipiece(testPiece_1, [testPiece_1, testPiece_2], testBoard)

        self.assertEqual(expected, actual)

    def test_testAttemptAddMultipiece_1(self):
        testBoard = tetrisBoard({'cols':5})
        testPiece_1 = tetrisPiece()
        testData = tetrisData({'cols':5, 'rows':3, 'numPieces':2})
        testBoard.board = [
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0]
        ]
        testData.currentBoard = testBoard
        expected = True
        actual = testData.attemptAddPiece()    

        self.assertEqual(expected, actual)

    def test_testAttemptAddMultipiece_2(self):
        testBoard = tetrisBoard({'cols':4})
        testPiece_1 = tetrisPiece(0, [[1,1,1]])
        testData = tetrisData({'cols':4, 'rows':3, 'numPieces':2})
        testBoard.board = [
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0]
        ]
        testData.currentBoard = testBoard
        testData.attemptAddPiece(testPiece_1.pieceShape, testPiece_1.piece_x)

        expected = testPiece_1.pieceShape
        actual = []
        if len(testData.pieceList) > 0:
            actual = testData.pieceList[0].pieceShape
            

        self.assertEqual(expected, actual)
    
    def test_testAttemptAddMultipiece_3(self):
        testBoard = tetrisBoard({'cols':4})
        testData = tetrisData({'cols':4, 'rows':3, 'numPieces':2})
        testBoard.board = [
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0]]
        testData.currentBoard = testBoard
        testData.attemptAddPiece()

        expected = 1
        actual = len(testData.pieceList)

        self.assertEqual(expected, actual)

class staticEvaluationFunctionTest(unittest.TestCase):
    def test_testProjectPieces_1(self):
        testData = tetrisData({'cols':4, 'numPieces':2})
        testPiece_1 = tetrisPiece(0, [[1,0],[1,1]])
        testPiece_2 = tetrisPiece(3, [[1],[1]])
        testData.pieceList = [testPiece_1, testPiece_2]
        testBoard = [
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0]
        ]
        testData.currentBoard.board = testBoard
        expected = [
            [0,0,0,0],
            [0,0,0,0],
            [1,0,0,1],
            [1,1,0,1]
        ]
        testEvaluator = evaluator(1, testData)

        actual = testEvaluator.projectPieces()

        self.assertEqual(expected, actual)

    def test_testProjectPieces_2(self):
        testData = tetrisData({'cols':4, 'numPieces':2})
        testPiece_1 = tetrisPiece(0, [[1,0],[1,1]])
        testPiece_2 = tetrisPiece(3, [[1],[1]])
        testData.pieceList = [testPiece_1, testPiece_2]
        testBoard = [
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0]
        ]
        testData.currentBoard.board = testBoard
        expected = copy.deepcopy(testData).currentBoard.board
        testEvaluator = evaluator(0, testData)
        

        testEvaluator.projectPieces()
        actual = testEvaluator.currentData.currentBoard.board

        self.assertEqual(expected, actual)

    def test_testProjectPieces_3(self):
        testData = tetrisData({'cols':6, 'numPieces':2})
        testPiece_1 = tetrisPiece(0, [[1,0],[1,1],[1,0]])
        testPiece_2 = tetrisPiece(1, [[2,2],[0,2]])
        testPiece_2.piece_y = 3
        testData.pieceList = [testPiece_1, testPiece_2]
        testBoard = [
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0]
        ]
        testData.currentBoard.board = testBoard
        expected = [
            [0,0,0,0],
            [0,0,0,0],
            [1,0,0,0],
            [1,1,0,0],
            [1,2,2,0],
            [0,0,2,0]
        ]
        testEvaluator = evaluator(0, testData)
        
        actual = testEvaluator.projectPieces()

        self.assertEqual(expected, actual)

    def test_testSEF1_1(self):
        testData = tetrisData()
        testBoard = [
            [0,0,0],
            [0,0,0],
            [0,1,0],
            [1,1,0]
        ]
        testData.currentBoard.board = testBoard
        expected = 2

        testEvaluator = evaluator(1, testData)
        actual = testEvaluator.evaluate()

        self.assertEqual(expected, actual)

    def test_testSEF1_2(self):
        testData = tetrisData()
        testBoard = [
            [0,0,0],
            [0,0,0],
            [0,0,0],
            [0,0,0]
        ]
        testData.currentBoard.board = testBoard
        expected = 0

        testEvaluator = evaluator(1, testData)
        actual = testEvaluator.evaluate()

        self.assertEqual(expected, actual)

    def test_testSEF1_3(self):
        testData = tetrisData()
        testBoard = [
            [1,0,0],
            [1,0,0],
            [1,0,0],
            [1,0,0]
        ]
        testData.currentBoard.board = testBoard
        expected = 4

        testEvaluator = evaluator(1, testData)
        actual = testEvaluator.evaluate()

        self.assertEqual(expected, actual)

    def test_testSEF2_1(self):
        testData = tetrisData({'rows':4})
        testBoard = [
            [0,0,0],
            [0,0,0],
            [0,1,0],
            [1,1,0]
        ]
        testData.currentBoard.board = testBoard
        expected = 3

        testEvaluator = evaluator(2, testData)
        actual = testEvaluator.evaluate()

        self.assertEqual(expected, actual)

    def test_testSEF3_1(self):
        testData = tetrisData({'rows':4})
        testBoard = [
            [0,0,0],
            [0,0,0],
            [1,1,1],
            [1,1,0]
        ]
        testData.currentBoard.board = testBoard
        expected = 1

        testEvaluator = evaluator(3, testData)
        actual = testEvaluator.evaluate()

        self.assertEqual(expected, actual)

    def test_testSEF4_1(self):
        testData = tetrisData()
        testBoard = [
            [0,0,0],
            [0,0,0],
            [1,1,1],
            [1,1,0]
        ]
        testData.currentBoard.board = testBoard
        expected = 1

        testEvaluator = evaluator(4, testData)
        actual = testEvaluator.evaluate()

        self.assertEqual(expected, actual)

    def test_testSEF4_2(self):
        testData = tetrisData()
        testBoard = [
            [0,0,0],
            [1,0,0],
            [0,1,0],
            [1,0,1],
            [1,0,0]
        ]
        testData.currentBoard.board = testBoard
        expected = 4

        testEvaluator = evaluator(4, testData)
        actual = testEvaluator.evaluate()

        self.assertEqual(expected, actual)

    def test_testSEF5_2(self):
        testData = tetrisData()
        testBoard = [
            [0,0,0],
            [1,0,0],
            [0,1,0],
            [1,0,1],
            [1,0,0]
        ]
        testData.currentBoard.board = testBoard
        expected = 6

        testEvaluator = evaluator(5, testData)
        actual = testEvaluator.evaluate()

        self.assertEqual(expected, actual)

    
unittest.main()