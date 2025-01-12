import tkinter as tk
from tkinter import messagebox
import random

class WumpusWorld:
    def __init__(self, root):
        self.root = root
        self.root.title("Wumpus Dünyası")
        
        # Oyun durumu
        self.size = 4
        self.board = None
        self.player_pos = [0, 3]  # Başlangıç pozisyonu: sol alt köşe
        self.player_dir = 'sağ'
        self.score = 0
        self.game_over = False
        
        # Bilgi tabanı
        self.knowledge = []
        
        # Arayüz elemanlarını oluştur
        self.create_gui()
        
        # Oyunu başlat
        self.init_game()

    def create_gui(self):
        # Ana çerçeve
        main_frame = tk.Frame(self.root, bg="black")
        main_frame.pack(padx=10, pady=10)
        
        # Oyun tahtası çerçevesi
        self.board_frame = tk.Frame(main_frame, bg="black")
        self.board_frame.grid(row=0, column=0, padx=10)
        
        # Kontrol paneli
        control_frame = tk.Frame(main_frame, bg="black")
        control_frame.grid(row=1, column=0, pady=10)
        
        # Hareket düğmeleri
        tk.Button(control_frame, text="↑", command=lambda: self.move(0, -1), bg="darkblue", fg="white").grid(row=0, column=1)
        tk.Button(control_frame, text="↓", command=lambda: self.move(0, 1), bg="darkblue", fg="white").grid(row=2, column=1)
        tk.Button(control_frame, text="←", command=lambda: self.move(-1, 0), bg="darkblue", fg="white").grid(row=1, column=0)
        tk.Button(control_frame, text="→", command=lambda: self.move(1, 0), bg="darkblue", fg="white").grid(row=1, column=2)
        tk.Button(control_frame, text="Dön", command=self.rotate, bg="purple", fg="white").grid(row=1, column=1)
        
        # Bilgi tabanı ve mesajlar
        info_frame = tk.Frame(main_frame, bg="black")
        info_frame.grid(row=0, column=1, rowspan=2, padx=10)
        
        tk.Label(info_frame, text="Mantıksal Çıkarımlar:", bg="black", fg="white").pack()
        self.knowledge_text = tk.Text(info_frame, width=40, height=12, bg="darkgray", fg="black")
        self.knowledge_text.pack()
        
        tk.Label(info_frame, text="Puan:", bg="black", fg="white").pack()
        self.score_label = tk.Label(info_frame, text="0", bg="black", fg="white")
        self.score_label.pack()
        
        # Yeni oyun düğmesi
        tk.Button(info_frame, text="Yeni Oyun", command=self.init_game, bg="purple", fg="white").pack(pady=10)

    def init_game(self):
        # Boş tahta oluştur
        self.board = [[{
            'pit': False,
            'wumpus': False,
            'gold': False,
            'breeze': False,
            'stench': False,
            'visited': False
        } for _ in range(self.size)] for _ in range(self.size)]
        
        # Wumpus yerleştir
        wx, wy = random.randint(1, 3), random.randint(1, 3)
        self.board[wy][wx]['wumpus'] = True
        
        # Çukurlar yerleştir (2-3 çukur)
        for _ in range(random.randint(2, 3)):
            while True:
                px, py = random.randint(1, 3), random.randint(1, 3)
                if not (self.board[py][px]['wumpus'] or self.board[py][px]['pit']):
                    self.board[py][px]['pit'] = True
                    break
        
        # Altını yerleştir
        while True:
            gx, gy = random.randint(1, 3), random.randint(1, 3)
            if not (self.board[gy][gx]['wumpus'] or self.board[gy][gx]['pit']):
                self.board[gy][gx]['gold'] = True
                break
        
        # Algılar (esinti ve koku) ekle
        for y in range(self.size):
            for x in range(self.size):
                if self.board[y][x]['wumpus'] or self.board[y][x]['pit']:
                    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                        new_x, new_y = x + dx, y + dy
                        if 0 <= new_x < self.size and 0 <= new_y < self.size:
                            if self.board[y][x]['wumpus']:
                                self.board[new_y][new_x]['stench'] = True
                            if self.board[y][x]['pit']:
                                self.board[new_y][new_x]['breeze'] = True
        
        # Oyun durumu sıfırlanır
        self.player_pos = [0, 3]
        self.player_dir = 'sağ'
        self.score = 0
        self.game_over = False
        self.knowledge = []
        self.board[3][0]['visited'] = True
        
        # Görüntüleri güncelle
        self.update_display()
        self.update_knowledge(0, 3)

    def update_display(self):
        # Tahta çerçevesini temizle
        for widget in self.board_frame.winfo_children():
            widget.destroy()
        
        # Hücreleri oluştur
        for y in range(self.size):
            for x in range(self.size):
                cell = tk.Frame(self.board_frame, width=60, height=60, relief='raised', borderwidth=1, bg="black")
                cell.grid(row=y, column=x, padx=1, pady=1)
                cell.grid_propagate(False)
                
                if self.board[y][x]['visited']:
                    if self.board[y][x]['breeze']:
                        tk.Label(cell, text="E", fg="cyan", bg="black").place(x=5, y=5)
                    if self.board[y][x]['stench']:
                        tk.Label(cell, text="K", fg="red", bg="black").place(x=45, y=5)
                    if self.board[y][x]['pit']:
                        tk.Label(cell, text="Ç", fg="blue", bg="black").place(x=25, y=25)
                    if self.board[y][x]['wumpus']:
                        tk.Label(cell, text="W", fg="purple", bg="black").place(x=25, y=25)
                    if self.board[y][x]['gold']:
                        tk.Label(cell, text="A", fg="yellow", bg="black").place(x=25, y=25)
                else:
                    cell.configure(bg='gray')
                
                if self.player_pos == [x, y]:
                    directions = {'sağ': '→', 'sol': '←', 'yukarı': '↑', 'aşağı': '↓'}
                    tk.Label(cell, text=directions[self.player_dir], fg="white", bg="black").place(x=25, y=25)
        
        # Puanı güncelle
        self.score_label.configure(text=str(self.score))

    def update_knowledge(self, x, y):
        cell = self.board[y][x]
        if cell['visited']:
            if cell['breeze']:
                self.knowledge.append(f"Esinti algılandı ({x+1},{4-y}) - Yakında çukur olabilir.")
            if cell['stench']:
                self.knowledge.append(f"Koku algılandı ({x+1},{4-y}) - Yakında Wumpus olabilir.")
            if not cell['breeze'] and not cell['stench']:
                self.knowledge.append(f"Güvenli hücre ({x+1},{4-y})")
        
            # Bilgi tabanını güncelle
            self.knowledge_text.delete(1.0, tk.END)
            for k in self.knowledge[-10:]:  # Son 10 çıkarımı göster
                self.knowledge_text.insert(tk.END, k + '\n')

    def move(self, dx, dy):
        if self.game_over:
            return
            
        new_x = self.player_pos[0] + dx
        new_y = self.player_pos[1] + dy
        
        if 0 <= new_x < self.size and 0 <= new_y < self.size:
            self.player_pos = [new_x, new_y]
            self.board[new_y][new_x]['visited'] = True
            self.score -= 1
            
            # Oyun durumu kontrolü
            if self.board[new_y][new_x]['wumpus']:
                messagebox.showinfo("Oyun Bitti", "Wumpus seni öldürdü!")
                self.game_over = True
            elif self.board[new_y][new_x]['pit']:
                messagebox.showinfo("Oyun Bitti", "Bir çukura düştün!")
                self.game_over = True
            elif self.board[new_y][new_x]['gold']:
                self.score += 1000
                messagebox.showinfo("Tebrikler", "Altını buldun! Oyunu kazandın!")
                self.game_over = True
            
            self.update_knowledge(new_x, new_y)
            self.update_display()

    def rotate(self):
        directions = ['sağ', 'aşağı', 'sol', 'yukarı']
        current_index = directions.index(self.player_dir)
        self.player_dir = directions[(current_index + 1) % 4]
        self.update_display()

if __name__ == "__main__":
    root = tk.Tk()
    game = WumpusWorld(root)
    root.mainloop()
    
