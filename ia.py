from copy import deepcopy

BLACK = 'Red'
WHITE = 'White'

class Piece():
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

class Queen(Piece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)

class King(Piece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)

class Board():
    def __init__(self, size = 10):
        self.pieces = []
        self.turn = WHITE
        self.size = size
        self.selected_piece = None
        self.num_white_queen = 0
        self.num_black_queen = 0
        self.num_white_king = 0
        self.num_black_king = 0
        self.lastMove = [None] * 4
        self.generateBoard()

    def addQueen(self, x, y, color):
        queen = Queen(x, y, color)
        self.pieces.append(queen)
        if queen.color == WHITE:
            self.num_white_queen += 1
        else:
            self.num_black_queen += 1
    
    def addKing(self, x, y, color):
        king = King(x, y, color)
        self.pieces.append(king)
        if king.color == WHITE:
            self.num_white_king += 1
        else:
            self.num_black_king += 1

    def removePiece(self, piece):
        if piece.color == WHITE:
            if isinstance(piece, King):
                self.num_white_king -= 1
            else:
                self.num_white_queen -= 1
        else:
            if isinstance(piece, King):
                self.num_black_king -= 1
            else:
                self.num_black_queen -= 1

        self.pieces.remove(piece)

    def changeTurn(self):
        if self.turn == WHITE:
            self.turn = BLACK
        else:
            self.turn = WHITE

    def generateBoard(self):
        for y in range(self.size):
            for x in range(self.size):
                if (x + y) % 2 != 0:
                    if y < (self.size / 2 - 1):
                        self.addQueen(x, y, BLACK)
                    if y >= (self.size / 2 + 1) - (self.size % 2):
                        self.addQueen(x, y, WHITE)

    def getPieceAtPosition(self, x, y):
        for p in self.pieces:
            if p.x == x and p.y == y:
                return p
            
    def getValidMove(self, piece):
        moves = []
        valid_moves = []
        
        if piece.color == WHITE or isinstance(piece, King):
            moves.append((1, -1))
            moves.append((-1, -1))
        if piece.color == BLACK or isinstance(piece, King):
            moves.append((1, 1))
            moves.append((-1, 1))

        for m in moves:
            dest_x, dest_y = piece.x + m[0], piece.y + m[1]
            if 0 <= dest_x <= self.size - 1 and 0 <= dest_y <= self.size - 1:
                dest = self.getPieceAtPosition(dest_x, dest_y)
                if dest == None:
                    valid_moves.append((dest_x, dest_y, None))
                elif dest.color != piece.color:
                    piece_to_eat = dest
                    dest_x, dest_y = piece.x + m[0] * 2, piece.y + m[1] * 2
                    if 0 <= dest_x <= self.size - 1 and 0 <= dest_y <= self.size - 1:
                        dest = self.getPieceAtPosition(dest_x, dest_y)
                        if dest == None:
                            valid_moves.append((dest_x, dest_y, piece_to_eat))    
        return valid_moves
            
    def movePiece(self, piece, x, y):
        moves = self.getValidMove(piece)
        for m in moves:
            dest_x, dest_y, piece_to_eat = m
            if dest_x == x and dest_y == y:
                self.lastMove = (piece.x, piece.y, x, y)
                piece.x = x
                piece.y = y
                if piece_to_eat:
                    self.removePiece(piece_to_eat)
        self.checkForPromotion()
        self.changeTurn()

    def checkWin(self):
        total_piece_white = self.num_white_queen + self.num_white_king
        total_piece_black = self.num_black_queen + self.num_black_king

        if total_piece_white == 0:
            return BLACK
        elif total_piece_black == 0:
            return WHITE
        else:
            num_moves = 0
            for piece in self.pieces:
                if piece.color == self.turn:
                    num_moves += len(self.getValidMove(piece))
            if num_moves == 0 and self.turn == BLACK:
                return WHITE
            if num_moves == 0 and self.turn == WHITE:
                return BLACK

    def evaluate(self):
        return (self.num_white_queen + self.num_white_king * 1.2) - (self.num_black_queen + self.num_black_king * 1.2)

    def turnQueenToKing(self, queen):
        self.addKing(queen.x, queen.y, queen.color)
        self.removePiece(queen)

    def checkForPromotion(self):
        for piece in self.pieces:
            if piece.color == WHITE and piece.y == 0:
                self.turnQueenToKing(piece)
            elif piece.color == BLACK and piece.y == self.size - 1:
                self.turnQueenToKing(piece)

def logicToWierd(x, y):
    return y * 5 + (x // 2)
 
def wierdToLogic(index):
    x = index  % 5 * 2
    y = index // 5
    if y % 2 == 0:
        x += 1
    return x, y

def plateauToBoard(plateau, turn):
    board = Board(10)
    board.pieces = []

    index = 0
    for p in plateau:
        if p:    
            x, y = wierdToLogic(index)
            color, isKing = plateau[index]          
            if isKing:
                if color == 1:
                    board.addKing(x, y, BLACK)
                else:
                    board.addKing(x, y, WHITE)
            else:
                if color == 1:
                    board.addQueen(x, y, BLACK)
                else:
                    board.addQueen(x, y, WHITE)
        index += 1

    if turn == 0:
        board.turn = WHITE
    else:
        board.turn = BLACK

    return board

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

def play(plateau : list, player : bool):
    board = plateauToBoard(plateau, player)
    new_board = minimax(board, 3, float('-inf'), float('inf'), board.turn)[1]
    x, y, dest_x, dest_y = new_board.lastMove
    src = logicToWierd(x, y)
    dest = logicToWierd(dest_x, dest_y)
    return src + 1, dest + 1 

if __name__ == "__main__":
    board = Board(10)

    plateau = [None] * 50
    for p in board.pieces:
        index = logicToWierd(p.x, p.y)
        color = int(p.color == BLACK)
        isKing = isinstance(p, King)
        plateau[index] = (color, isKing)

    result = play(plateau, 0)
    print(result)