import tkinter as tk
import random
import json


class UzayOyunu:
    def __init__(self):
        # Create window
        self.pencere = tk.Tk()
        self.pencere.title("Uzay Oyunu")
        self.pencere.geometry("600x800")

        # Game canvas
        self.canvas = tk.Canvas(self.pencere, width=600, height=800, bg='black')
        self.canvas.pack()

        # Load score data
        self.skor_yukle()

        # Show main menu
        self.ana_menu()

    def skor_yukle(self):
        """Load saved score data"""
        try:
            with open('skorlar_i.json', 'r') as dosya:
                self.skor_verileri = json.load(dosya)
        except:
            self.skor_verileri = {"yuksek_skor": 0}

    def skor_kaydet(self):
        """Save score data"""
        with open('skorlar_i.json', 'w') as dosya:
            json.dump(self.skor_verileri, dosya)

    def ana_menu(self):
        """Display main menu"""
        self.canvas.delete('all')

        # Game title
        self.canvas.create_text(
            300, 200,
            text="UZAY OYUNU",
            fill='white',
            font=('Arial', 36, 'bold')
        )

        # High score
        self.canvas.create_text(
            300, 300,
            text=f"En Yüksek Skor: {self.skor_verileri['yuksek_skor']}",
            fill='yellow',
            font=('Arial', 20)
        )

        # Start instruction
        self.canvas.create_text(
            300, 400,
            text="Başlamak için SPACE'e basın",
            fill='white',
            font=('Arial', 20)
        )

        # Controls
        self.canvas.create_text(
            300, 500,
            text="Kontroller:\n← → : Hareket\nSPACE : Ateş",
            fill='white',
            font=('Arial', 16)
        )

        # Bind space key
        self.pencere.bind('<space>', self.oyunu_baslat)

    def oyunu_baslat(self, event=None):
        """Start the game"""
        self.pencere.unbind('<space>')
        self.skor = 0
        self.can = 3
        self.oyun_aktif = True

        # Game objects
        self.gemi_x = 300
        self.gemi_y = 700
        self.meteorlar = []
        self.mermiler = []

        # Clear game area
        self.canvas.delete('all')

        # Create spaceship
        self.gemi = self.canvas.create_polygon(
            self.gemi_x, self.gemi_y - 20,
            self.gemi_x - 15, self.gemi_y + 10,
            self.gemi_x + 15, self.gemi_y + 10,
            fill='white'
        )

        # Score display
        self.skor_label = self.canvas.create_text(
            50, 30, text=f"Skor: {self.skor}",
            fill='white', font=('Arial', 14)
        )

        # Lives display
        self.can_label = self.canvas.create_text(
            550, 30, text=f"Can: {self.can}",
            fill='white', font=('Arial', 14)
        )

        # Bind controls
        self.pencere.bind('<Left>', self.sola_git)
        self.pencere.bind('<Right>', self.saga_git)
        self.pencere.bind('<space>', self.ates_et)

        # Start game loop
        self.oyun_dongusu()

    def sola_git(self, event):
        """Move ship left"""
        if self.gemi_x > 20:
            self.gemi_x -= 10
            self.canvas.move(self.gemi, -10, 0)

    def saga_git(self, event):
        """Move ship right"""
        if self.gemi_x < 580:
            self.gemi_x += 10
            self.canvas.move(self.gemi, 10, 0)

    def ates_et(self, event):
        """Fire weapon"""
        mermi = self.canvas.create_oval(
            self.gemi_x - 2, self.gemi_y - 20,
            self.gemi_x + 2, self.gemi_y - 15,
            fill='yellow'
        )
        self.mermiler.append(mermi)

    def meteor_olustur(self):
        """Create new meteor"""
        x = random.randint(20, 580)
        meteor = self.canvas.create_oval(
            x - 10, -10, x + 10, 10,
            fill='red'
        )
        self.meteorlar.append({'id': meteor, 'x': x, 'y': -10})

    def oyun_dongusu(self):
        """Main game loop"""
        if not self.oyun_aktif:
            return

        # Move meteors
        for meteor in self.meteorlar[:]:
            self.canvas.move(meteor['id'], 0, 3)
            meteor['y'] += 3

            # Check if meteor is off screen
            if meteor['y'] > 800:
                self.canvas.delete(meteor['id'])
                self.meteorlar.remove(meteor)
            # Check collision with ship
            elif abs(meteor['y'] - self.gemi_y) < 30 and abs(meteor['x'] - self.gemi_x) < 20:
                self.can -= 1
                self.canvas.delete(meteor['id'])
                self.meteorlar.remove(meteor)
                self.canvas.itemconfig(self.can_label, text=f"Can: {self.can}")

                if self.can <= 0:
                    self.oyun_bitti()
                    return

        # Move bullets
        for mermi in self.mermiler[:]:
            self.canvas.move(mermi, 0, -5)
            mermi_konum = self.canvas.coords(mermi)

            # Check if bullet is off screen
            if mermi_konum[1] < 0:
                self.canvas.delete(mermi)
                self.mermiler.remove(mermi)
                continue

            # Check meteor hits
            for meteor in self.meteorlar[:]:
                meteor_konum = self.canvas.coords(meteor['id'])
                if (abs(mermi_konum[1] - meteor['y']) < 20 and
                        abs(mermi_konum[0] - meteor['x']) < 20):
                    self.skor += 10
                    self.canvas.itemconfig(self.skor_label, text=f"Skor: {self.skor}")
                    self.canvas.delete(mermi)
                    self.canvas.delete(meteor['id'])
                    self.mermiler.remove(mermi)
                    self.meteorlar.remove(meteor)
                    break

        # Create new meteor
        if random.random() < 0.03:
            self.meteor_olustur()

        # Continue loop
        self.pencere.after(20, self.oyun_dongusu)

    def oyun_bitti(self):
        """Show game over screen"""
        self.oyun_aktif = False

        # Unbind controls
        self.pencere.unbind('<Left>')
        self.pencere.unbind('<Right>')
        self.pencere.unbind('<space>')

        # Check high score
        if self.skor > self.skor_verileri['yuksek_skor']:
            self.skor_verileri['yuksek_skor'] = self.skor
            self.skor_kaydet()

        # Game over screen
        self.canvas.delete('all')
        self.canvas.create_text(
            300, 300,
            text=f"OYUN BİTTİ!\nSkorunuz: {self.skor}\n" +
                 f"En Yüksek Skor: {self.skor_verileri['yuksek_skor']}\n\n" +
                 "Tekrar oynamak için SPACE'e basın",
            fill='white',
            font=('Arial', 20),
            justify='center'
        )

        # Rebind space key
        self.pencere.bind('<space>', self.oyunu_baslat)

    def baslat(self):
        """Start the game"""
        self.pencere.mainloop()


if __name__ == "__main__":
    oyun = UzayOyunu()
    oyun.baslat()