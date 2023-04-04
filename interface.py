import tkinter as tk
from board import Board, King
from constant import *
from minimax import minimax
import time
from threading import Thread
from PIL import Image, ImageTk
import simpleaudio as sa

def restartGame(event):
    global board
    if board.checkWin() != None:
        board = Board(BOARD_SIZE)
        drawBoard(board)
        threadGameLoop()

def drawPiece(piece):
    x, y = piece.x, piece.y

    piece_img = None
    if piece.color == WHITE:
        if isinstance(piece, King):
            piece_img = white_king_img
        else:
            piece_img = white_queen_img
    else:
        if isinstance(piece, King):
            piece_img = black_king_img
        else:
            piece_img = black_queen_img

    canvas.create_image(
        x * CASE_SIZE + 5, 
        y * CASE_SIZE + 5, 
        image=piece_img,
        anchor="nw"
    )

def drawBoard(board):
    canvas.delete("all")

    for y in range(0, board.size, 2):
        for x in range(0, board.size, 2):
            canvas.create_image(x * CASE_SIZE, y * CASE_SIZE, image=tile_img, anchor="nw")
    
    for y in range(board.size):
        for x in range(board.size):
            piece = board.getPieceAtPosition(x, y)
            if piece:
                drawPiece(piece)

    if board.selected_piece:
        for move in board.getValidMove(board.selected_piece):
            dest_x, dest_y, piece_to_eat = move
            canvas.create_image(dest_x * CASE_SIZE + CASE_SIZE // 2, dest_y * CASE_SIZE  + CASE_SIZE // 2, image=move_selector_img, anchor="center")
    canvas.update()

def makeGameLoop():

    # On rentre seulement dans la boucle de jeu si au moins un des deux joueurs est un bot
    if player_black_type == BOT or player_white_type == BOT:

        # si joueur blanc est un bot, on attend avant de jouer pour le voir le coup
        if player_white_type == BOT:
            time.sleep(MIN_TIME_TURN / 1000)

        while not board.checkWin():

            type_player = player_white_type
            if board.turn == BLACK:
                type_player = player_black_type

            if type_player == BOT:

                if player_white_type != player_black_type:
                    time.sleep(MIN_TIME_TURN / 1000)

                start = time.time()
                new_board = minimax(board, MINMAX_DEPTH, float('-inf'), float('inf'), board.turn)[1]
                board.pieces = new_board.pieces
                board.changeTurn()
                playSoundMove()
                drawBoard(board)
                
                duration = (MIN_TIME_TURN / 1000) - (time.time() - start)
                if duration > 0:
                    time.sleep(duration)
            time.sleep(0.1)
        
        canvas.create_image(
            WINDOW_SIZE // 2, 
            WINDOW_SIZE // 2,
            image=gui_win_menu,
            anchor="center"
        )
        canvas.create_text(WINDOW_SIZE // 2, WINDOW_SIZE // 2 - 10, text=f'{board.checkWin()} WIN !', fill="black", font=('Helvetica 22 bold'), justify=tk.CENTER)
        canvas.create_text(WINDOW_SIZE // 2, WINDOW_SIZE // 2 + 15, text=f'press R to Restart', fill="black", font=('Helvetica 14 bold'), justify=tk.CENTER)

def boardClick(event):
    x, y = event.x // CASE_SIZE, event.y // CASE_SIZE
    piece = board.getPieceAtPosition(x, y)

    if piece:
        if piece.color == board.turn:
            if board.turn == WHITE and player_white_type == HUMAN:
                board.selected_piece = piece
                drawBoard(board)
            elif board.turn == BLACK and player_black_type == HUMAN:
                board.selected_piece = piece
                drawBoard(board)
    else:
        if board.selected_piece:
            moves = board.getValidMove(board.selected_piece)
            for move in moves:
                dest_x, dest_y, piece_to_eat = move
                if dest_x == x and dest_y == y:
                    board.movePiece(board.selected_piece, x, y)
                    board.selected_piece = None
                    playSoundMove()
                    drawBoard(board)

def playSoundMove():
    wave_obj = sa.WaveObject.from_wave_file(SOUND_PIECE_PLAY)
    play_obj = wave_obj.play()

def threadGameLoop():
    t1=Thread(target=makeGameLoop)
    t1.start()

def startBotVsBot():
    global player_white_type, player_black_type
    player_white_type, player_black_type = BOT, BOT
    root.destroy()

def startHumanVsBot():
    global player_white_type, player_black_type
    player_white_type, player_black_type = HUMAN, BOT
    root.destroy()

def startHumanVsHuman():
    global player_white_type, player_black_type
    player_white_type, player_black_type = HUMAN, HUMAN
    root.destroy()

player_white_type, player_black_type = None, None
root = tk.Tk()
root.geometry('300x200')
root.title("Checker Minimax Alpha-Beta Prunning")
button1 = tk.Button(root, text="Player against Player", command=startHumanVsHuman)
button2 = tk.Button(root, text="Player against Computer", command=startHumanVsBot)
button3 = tk.Button(root, text="Computer against Computer", command=startBotVsBot)
button1.place(relx=0.5, rely=0.35, anchor=tk.CENTER)
button2.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
button3.place(relx=0.5, rely=0.65, anchor=tk.CENTER)
root.mainloop()

root = tk.Tk()
root.geometry(f'{WINDOW_SIZE}x{WINDOW_SIZE}')
root.resizable(False,False)
root.title("Checker Minimax Alpha-Beta Prunning")

tile_img = Image.open(TILE_FILE)
tile_img = tile_img.resize((CASE_SIZE * 2, CASE_SIZE * 2), Image.LANCZOS)
tile_img = ImageTk.PhotoImage(tile_img)

white_queen_img = Image.open(WHITE_QUEEN_FILE)
white_queen_img = white_queen_img.resize((CASE_SIZE - 10, CASE_SIZE - 10), Image.LANCZOS)
white_queen_img = ImageTk.PhotoImage(white_queen_img)

black_queen_img = Image.open(BLACK_QUEEN_FILE)
black_queen_img = black_queen_img.resize((CASE_SIZE - 10, CASE_SIZE - 10), Image.LANCZOS)
black_queen_img = ImageTk.PhotoImage(black_queen_img)

white_king_img = Image.open(WHITE_KING_FILE)
white_king_img = white_king_img.resize((CASE_SIZE - 10, CASE_SIZE - 10), Image.LANCZOS)
white_king_img = ImageTk.PhotoImage(white_king_img)

black_king_img = Image.open(BLACK_KING_FILE)
black_king_img = black_king_img.resize((CASE_SIZE - 10, CASE_SIZE - 10), Image.LANCZOS)
black_king_img = ImageTk.PhotoImage(black_king_img)

move_selector_img = Image.open(MOVE_SELECTOR_FILE)
move_selector_img = move_selector_img.resize((CASE_SIZE // 4 , CASE_SIZE // 4), Image.LANCZOS)
move_selector_img = ImageTk.PhotoImage(move_selector_img)

gui_win_menu = Image.open(GUI_WIN_FILE)
gui_win_menu = ImageTk.PhotoImage(gui_win_menu)

canvas = tk.Canvas(root, height = WINDOW_SIZE, width = WINDOW_SIZE)
canvas.pack()
canvas.bind("<Button-1>", boardClick)
root.bind("r", restartGame)

board = Board(BOARD_SIZE)
drawBoard(board)

root.after(100, threadGameLoop)
root.mainloop()