from board import Board
from constant import BLACK, WHITE
from copy import deepcopy

def minimax(board, depth, alpha, beta, maximizingPlayer):
    if depth == 0 or board.checkWin() != None:
        return board.evaluate(), board

    if maximizingPlayer == WHITE:
        maxEval = float('-inf')
        bestBoard = None
        for next_board in getAllValidBoard(board, WHITE):
            eval = minimax(next_board, depth - 1, alpha, beta, BLACK)[0]
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            
            if maxEval == eval:
                bestBoard = next_board

            if alpha > beta:
                break
        
        return maxEval, bestBoard
    else:
        minEval = float('inf')
        bestBoard = None
        for next_board in getAllValidBoard(board, BLACK):
            
            eval = minimax(next_board, depth - 1, alpha, beta, WHITE)[0]
            minEval = min(minEval, eval)
            beta = min(beta, eval)

            if minEval == eval:
                bestBoard = next_board

            if alpha > beta:
                break

        return minEval, bestBoard

def getAllValidBoard(board, color):
    boards = []
    for piece in board.pieces:
        if piece.color == color:
            moves = board.getValidMove(piece)
            for move in moves:
                new_board = deepcopy(board)
                piece_to_move = new_board.getPieceAtPosition(piece.x, piece.y)
                new_board.movePiece(piece_to_move, move[0], move[1])
                boards.append(new_board)
    return boards
