import tkinter as tk
from PIL import Image, ImageTk
import chess
import random

SQ = 80
BOARD_SIZE = SQ * 8
PIECE_FOLDER = r"imagens"

PIECE_FILES = {
    "P": "white_pawn.png",
    "R": "white_rook.png",
    "N": "white_knight.png",
    "B": "white_bishop.png",
    "Q": "white_queen.png",
    "K": "white_king.png",
    "p": "black_pawn.png",
    "r": "black_rook.png",
    "n": "black_knight.png",
    "b": "black_bishop.png",
    "q": "black_queen.png",
    "k": "black_king.png",
}

PIECE_VALUES = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 1000
}


class ZeldaChess:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Zelda Chess IA")
        self.root.geometry("1200x850")
        self.root.configure(bg="#1f4d2a")

        self.player_color = chess.WHITE
        self.board = chess.Board()
        self.images = {}
        self.selected_square = None
        self.highlight_id = None
        self.captured_white = []
        self.captured_black = []
        self.ai_level = 2

        self.create_menu()
        self.root.mainloop()

    # MENU

    def create_menu(self):
        self.clear()
        frame = tk.Frame(self.root, bg="#1f4d2a")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text="Zelda Chess", font=("Papyrus", 36, "bold"),
                 fg="#f8f3d4", bg="#1f4d2a").pack(pady=30)

        tk.Label(frame, text="Escolha o nível da IA:", font=("Arial", 18, "bold"),
                 fg="#f8f3d4", bg="#1f4d2a").pack(pady=10)

        self.level_var = tk.IntVar(value=2)
        tk.Radiobutton(frame, text="Fácil", variable=self.level_var, value=1,
                       bg="#1f4d2a", fg="#f8f3d4", selectcolor="#000000", font=("Arial", 14)).pack()
        tk.Radiobutton(frame, text="Médio", variable=self.level_var, value=2,
                       bg="#1f4d2a", fg="#f8f3d4", selectcolor="#000000", font=("Arial", 14)).pack()
        tk.Radiobutton(frame, text="Difícil", variable=self.level_var, value=3,
                       bg="#1f4d2a", fg="#f8f3d4", selectcolor="#000000", font=("Arial", 14)).pack()

        tk.Button(frame, text="Iniciar Jogo", width=20, font=("Arial", 16, "bold"),
                  bg="#f8f3d4", fg="#1f4d2a", command=self.start_game).pack(pady=30)

    # INICIAR JOGO
    
    def start_game(self):
        self.clear()
        self.board = chess.Board()
        self.captured_white = []
        self.captured_black = []
        self.ai_level = self.level_var.get()
        self.load_images()

        self.canvas = tk.Canvas(self.root, width=BOARD_SIZE, height=BOARD_SIZE, bg="#1f4d2a")
        self.canvas.place(relx=0.5, rely=0.5, anchor="center")
        self.canvas.bind("<Button-1>", self.on_click)

        self.draw_board()
        self.draw_pieces()

        if self.player_color == chess.BLACK:
            self.root.after(300, self.ai_move)

    # CARREGAR IMAGENS

    def load_images(self):
        for piece, filename in PIECE_FILES.items():
            img = Image.open(f"{PIECE_FOLDER}/{filename}")
            img = img.resize((SQ, SQ), Image.NEAREST)
            self.images[piece] = ImageTk.PhotoImage(img)

    # ORIENTAÇÃO DO TABULEIRO

    def orient_coords(self, file, rank):
        return (file, 7 - rank) if self.player_color == chess.WHITE else (7 - file, rank)

    # DESENHAR TABULEIRO


    def draw_board(self):
        self.canvas.delete("square")
        light = "#a3d8a5"
        dark = "#3b6d35"
        for rank in range(8):
            for file in range(8):
                x, y = self.orient_coords(file, rank)
                x1, y1 = x * SQ, y * SQ
                x2, y2 = x1 + SQ, y1 + SQ
                color = light if (file + rank) % 2 == 0 else dark
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="", tags="square")

    # DESENHAR PEÇAS


    def draw_pieces(self):
        self.canvas.delete("piece")
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                file = chess.square_file(square)
                rank = chess.square_rank(square)
                x, y = self.orient_coords(file, rank)
                x, y = x * SQ, y * SQ
                self.canvas.create_image(x, y, image=self.images[piece.symbol()], anchor="nw", tags="piece")

    # ============================
    # CLIQUE DO JOGADOR
    # ============================

    def on_click(self, event):
        if self.board.turn != self.player_color or self.board.is_game_over():
            return

        self.check_game_over()

        file, rank = event.x // SQ, event.y // SQ
        square = chess.square(file, 7 - rank)

        piece = self.board.piece_at(square)
        if piece and piece.color == self.player_color:
            self.selected_square = square
            self.animate_selection(square)
            return

        if self.selected_square is not None:
            move = chess.Move(self.selected_square, square)

            p = self.board.piece_at(self.selected_square)
            if p.piece_type == chess.PAWN and (chess.square_rank(square) == 7):
                promotion_piece = self.ask_promotion()
                if promotion_piece:
                    move.promotion = promotion_piece
                else:
                    self.selected_square = None
                    self.remove_highlight()
                    return

            if move in self.board.legal_moves:
                captured_piece = self.board.piece_at(move.to_square)
                if captured_piece:
                    self.add_captured(captured_piece)

                self.board.push(move)
                self.selected_square = None
                self.remove_highlight()
                self.draw_pieces()
                self.check_game_over()
                self.root.after(300, self.ai_move)
            else:
                self.selected_square = None
                self.remove_highlight()

    # SELEÇÃO DE PEÇA

    def animate_selection(self, square):
        self.remove_highlight()
        file = chess.square_file(square)
        rank = chess.square_rank(square)
        x, y = self.orient_coords(file, rank)
        x, y = x * SQ, y * SQ
        self.highlight_id = self.canvas.create_rectangle(
            x, y, x + SQ, y + SQ, outline="#f8f3d4", width=4
        )

    def remove_highlight(self):
        if self.highlight_id:
            self.canvas.delete(self.highlight_id)
            self.highlight_id = None

    # IA

    def ai_move(self):
        if self.board.is_game_over():
            return

        moves = list(self.board.legal_moves)
        if not moves:
            self.check_game_over()
            return

        if self.ai_level == 1:
            move = random.choice(moves)
        else:
            depth = 2 if self.ai_level == 2 else 3
            move, _ = self.minimax_root(depth)

        captured_piece = self.board.piece_at(move.to_square)
        if captured_piece:
            self.add_captured(captured_piece)

        self.board.push(move)
        self.draw_pieces()
        self.check_game_over()

    def minimax_root(self, depth):
        best_move = None
        best_score = -9999
        for move in self.board.legal_moves:
            self.board.push(move)
            score = self.minimax(depth - 1, False)
            self.board.pop()
            if score > best_score:
                best_score = score
                best_move = move
        return best_move, best_score

    def minimax(self, depth, is_maximizing):
        if depth == 0 or self.board.is_game_over():
            return self.evaluate_board()
        if is_maximizing:
            max_eval = -9999
            for move in self.board.legal_moves:
                self.board.push(move)
                eval = self.minimax(depth - 1, False)
                self.board.pop()
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = 9999
            for move in self.board.legal_moves:
                self.board.push(move)
                eval = self.minimax(depth - 1, True)
                self.board.pop()
                min_eval = min(min_eval, eval)
            return min_eval

    def evaluate_board(self):
        score = 0
        for sq in chess.SQUARES:
            p = self.board.piece_at(sq)
            if p:
                v = PIECE_VALUES[p.piece_type]
                score += v if p.color != self.player_color else -v
        return score

    # CAPTURAS E PROMOÇÃO

    def add_captured(self, piece):
        if piece.color == chess.WHITE:
            self.captured_white.append(piece.symbol())
        else:
            self.captured_black.append(piece.symbol())

    def ask_promotion(self):
        available = self.captured_black if self.player_color == chess.WHITE else self.captured_white
        if not available:
            return None
        win = tk.Toplevel(self.root)
        win.title("Escolha a peça")
        chosen = {"piece": None}
        def select(p):
            mapping = {"q": chess.QUEEN, "r": chess.ROOK, "b": chess.BISHOP, "n": chess.KNIGHT}
            chosen["piece"] = mapping[p.lower()]
            win.destroy()
        tk.Label(win, text="Escolha a peça disponível:").pack()
        for p in available:
            tk.Button(win, image=self.images[p], command=lambda p=p: select(p)).pack(side="left")
        self.root.wait_window(win)
        return chosen["piece"]

    # FIM DE JOGO

    def check_game_over(self):
        if self.board.is_checkmate():
            winner = self.board.turn != self.player_color
            self.show_result(winner)
            self.board.clear()
        elif self.board.is_stalemate() or self.board.is_insufficient_material():
            self.show_result(False)
            self.board.clear()
        elif not list(self.board.legal_moves):
            if self.board.turn == self.player_color:
                self.show_result(False)
            else:
                self.show_result(True)
            self.board.clear()

    def show_result(self, winner):
        self.clear()
        result_frame = tk.Frame(self.root, bg="#1f7f00", width=1200, height=850)
        result_frame.pack(fill="both", expand=True)

        img_file = "ganhou.png" if winner else "perdeu.png"
        try:
            img = Image.open(f"{PIECE_FOLDER}/{img_file}")
            img = img.resize((600, 400), Image.NEAREST)
            img_tk = ImageTk.PhotoImage(img)
            tk.Label(result_frame, image=img_tk, bg="#1f7f00").pack(pady=50)
            result_frame.image = img_tk
        except Exception as e:
            tk.Label(result_frame, text=f"Não foi possível abrir a imagem: {e}",
                     bg="#1f7f00", fg="white", font=("Arial", 16)).pack(pady=50)

        tk.Button(result_frame, text="Voltar ao Início", font=("Arial", 18, "bold"),
                  bg="#f8f3d4", fg="#1f4d2a", command=self.create_menu).pack(pady=20)

    # UTILS

    def clear(self):
        for w in self.root.winfo_children():
            w.destroy()


if __name__ == "__main__":
    ZeldaChess()
