from Board import Board
from Pawn import Pawn
from Rook import Rook
from King import King
from Queen import Queen
from Bishop import Bishop
from Knight import Knight
from Coordinate import Coordinate as C
from Move import Move
from Piece import Piece
from AI import AI
from InputParser import InputParser
import time
import random
import sys

WHITE = True
BLACK = False


def askForPlayerSide():
    playerChoiceInput = input("What side would you like to play as? ").lower()
    if 'w' in playerChoiceInput:
        print("You will play as white")
        return WHITE
    else:
        print("You will play as black")
        return BLACK


def askForDepthOfAI():
    depthInput = 2
    try:
        depthInput = int(input("How deep should the AI look for moves? Warning : values above 3 will be very slow. "))
    except:
        print("Invalid input, defaulting to 2")
    return depthInput


def printCommandOptions():
    undoOption = 'u : undo last move'
    printLegalMovesOption = 'l : show all legal moves'
    randomMoveOption = 'r : make a random move'
    moveOption = 'a3, Nc3, Qxa2, etc : make the move'
    options = [undoOption, printLegalMovesOption, randomMoveOption, moveOption]
    for option in options:
        print(option)


def printAllLegalMoves(board, parser):
    for move in parser.getLegalMovesWithShortNotation(board.currentSide):
        print(move.notation)


def getRandomMove(board, parser):
    legalMoves = board.getAllMovesLegal(board.currentSide)
    randomMove = random.choice(legalMoves)
    randomMove.notation = parser.notationForMove(randomMove)
    return randomMove


def makeMove(move, board):
    print()
    print("Making move : " + move.notation)
    board.makeMove(move)


def printPointAdvantage(board):
    print("Currently, the point difference is : " + str(board.getPointAdvantageOfSide(board.currentSide)))


def undoLastTwoMoves(board):
    if len(board.history) >= 2:
        board.undoLastMove()
        board.undoLastMove()


def startGame(board, playerSide, ai):
    parser = InputParser(board, playerSide)
    while True:
        print(board)
        print()
        if board.isCheckmate():
            if board.currentSide == playerSide:
                print("Checkmate, you lost")
            else:
                print("Checkmate! You won!")
            return

        if board.isStalemate():
            if board.currentSide == playerSide:
                print("Stalemate")
            else:
                print("Stalemate")
            return

        if board.currentSide == playerSide:
            printPointAdvantage(board)
            move = None
            command = input("It's your move, what do you want to do? Type '?' for options. ").lower()
            if command == 'u':
                undoLastTwoMoves(board)
                continue
            elif command == '?':
                printCommandOptions()
                continue
            elif command == 'l':
                printAllLegalMoves(board, parser)
                continue
            elif command == 'r':
                move = getRandomMove(board, parser)
            else:
                move = parser.moveForShortNotation(command)
            if move:
                makeMove(move, board)
            else:
                print("Couldn't parse input, make sure you entered a valid command or move")

        else:
            print("AI thinking...")
            move = ai.getBestMove()
            move.notation = parser.notationForMove(move)
            makeMove(move, board)

board = Board()
playerSide = askForPlayerSide()
print()
aiDepth = askForDepthOfAI()
opponentAI = AI(board, not playerSide, aiDepth)
startGame(board, playerSide, opponentAI)
