#from timeit import Timer
from threading import Timer
import arcade
import random
import os



"""
Compiti per casa: La scorpacciata di Babbo Natalee
Dato questo giochino come partenza, aggiungere le seguenti modifiche:
1 - Scaricare, disegnare o generare con AI un'immagine di sfondo                                #fatto
     e mostrarla poi come background                                                            
2 - Premendo il tasto "M", il suono verrà mutato. Premendolo di nuovo                           #fatto
     il suono deve tornare. Avete due possibilità: o evitate proprio
     di far partire il suono, o vi guardate come funziona play_sound
     e vedete se c'è qualcosa che vi può essere utile
3 - Contate quanti biscotti vengono raccolti, salvatelo in una variabile                        #fatto
4 - Mostrate con draw_text il punteggio (numero di biscotti raccolti)                           #fatto
5 - Fate in modo che il nuovo biscotto venga sempre creato almeno a 100 pixel                   #fatto
    di distanza rispetto al giocatore

6 - Ogni volta che babbo natale mangia 5 biscotti, dalla prossima volta                         #fatto
    in  poi verranno creati 2 biscotti per volta. Dopo averne mangiati
    altri 5, vengono creati 3 biscotti per volta, poi 4, e via dicendo

7 - (Opzionale) Ogni volta che genero un biscotto, al 3% di possibilità potrebbe essere un      #fatto
         "golden cookie". Il golden cookie rimane solo 3 secondi sullo schermo
        ma vale 100 punti. 

        - Crea una nuova immagine per il golden cookie
        - Gestisci la creazione, il timer, ecc
        - Gestisci il punteggio

Fate questo esercizio in una repository su git e mandate il link al vostro account sul form
"""


class BabboNatale(arcade.Window):


    COOKIE_HEIGHT = 32
    COOKIE_WIDTH = 32
    GOLDEN_COOKIE_HEIGHT = 32
    GOLDEN_COOKIE_WIDTH = 32
    SCREEN_HEIGHT = 600
    SCREEN_WIDTH = 900
    sound_player = None
    TIMER_GOLDEN_COOKIE_SHOW = 3.0  # secondi
    TIMER_COOKIE_SHOW = 7.5  # secondi




    def __init__(self, larghezza, altezza, titolo):
        super().__init__(larghezza, altezza, titolo)
        self.babbo = None
        #self.cookie = None
        #self.Golden_cookie = None
        self.lista_babbo = arcade.SpriteList()
        self.lista_cookie = arcade.SpriteList()
        self.suono_munch = arcade.load_sound("./assets/munch.mp3")
        
        

        self.conta_biscotti_mangiati = 0  # punteggio

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.up_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.right_pressed = False
        
        self.velocita = 4

        self.testo_score = None
      
       
        self.setup()
    



    def setup(self):
        self.babbo = arcade.Sprite("./assets/babbo.png")
        self.babbo.center_x = BabboNatale.SCREEN_WIDTH // 2
        self.babbo.center_y = BabboNatale.SCREEN_HEIGHT // 2
        self.babbo.scale = 1.0
        self.lista_babbo.append(self.babbo)

        self.crea_cookie(tipo = "normal")
        



        self.background = arcade.load_texture("assets/Immagine_rovagnenim.jpg")

        self.testo_score = arcade.Text( #testo del punteggio
            text="Punteggio: " + str(self.conta_biscotti_mangiati),
            x = BabboNatale.SCREEN_WIDTH // 2, # Centro dello schermo
            y = BabboNatale.SCREEN_HEIGHT - 50, # Vicino in alto
            color = arcade.color.WHITE,
            font_size = 24,
            font_name = "Arial", # O il nome del tuo font caricato
            anchor_x = "center" # Allinea il testo al centro
        )

    def crea_cookie(self, tipo):

        #print("[" + str(self.conta_biscotti_mangiati) + "][" + tipo + "] == > Creazione cookie...")


        next_x = self.babbo.center_x

        while abs(next_x - self.babbo.center_x) < 100 :
            next_x = (BabboNatale.COOKIE_WIDTH/2) + (self.babbo.center_x + random.randint(100, (BabboNatale.SCREEN_WIDTH - BabboNatale.COOKIE_WIDTH)))%(BabboNatale.SCREEN_WIDTH - BabboNatale.COOKIE_WIDTH)


        next_y = self.babbo.center_y

        while abs(next_y - self.babbo.center_y) < 100 :
            next_y = (BabboNatale.COOKIE_HEIGHT/2) + (self.babbo.center_y + random.randint(100, (BabboNatale.SCREEN_HEIGHT - BabboNatale.COOKIE_HEIGHT)))%(BabboNatale.SCREEN_HEIGHT - BabboNatale.COOKIE_HEIGHT)
        
        #print("[",self.babbo.center_x,"][", self.babbo.center_y,"] = > Cookie creato in: [",next_x, "] [", next_y, "]")

        if tipo == "normal":
            cookie = arcade.Sprite("./assets/cookie.png")
        
            cookie.center_x = next_x
            cookie.center_y = next_y
            cookie.scale = 0.2
            cookie.tipo = "normal"
            cookie.timer = Timer(BabboNatale.TIMER_COOKIE_SHOW, self.rimuovi_cookie, [cookie])
            cookie.timer.start()
            self.lista_cookie.append(cookie)

        elif tipo == "golden":
            cookie = arcade.Sprite("./assets/golden_cookie.png")
        
            cookie.center_x = next_x
            cookie.center_y = next_y
            cookie.scale = 0.2
            cookie.tipo = "golden"
            cookie.golden_timer = Timer(BabboNatale.TIMER_GOLDEN_COOKIE_SHOW, self.rimuovi_golden_cookie, [cookie])
            cookie.golden_timer.start()
            self.lista_cookie.append(cookie)

    def rimuovi_golden_cookie(self, Sprite_cookie):
        Sprite_cookie.remove_from_sprite_lists()
        #print("Golden Cookie scomparso!")

    def rimuovi_cookie(self, Sprite_cookie):
        Sprite_cookie.remove_from_sprite_lists()
        #print("Cookie scomparso!")



    
        
    
    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.background, arcade.types.Viewport( 0, 0, BabboNatale.SCREEN_WIDTH, BabboNatale.SCREEN_HEIGHT))
        self.lista_cookie.draw()
        self.lista_babbo.draw()
        self.testo_score.draw()
        
    
    
    


    def on_update(self, delta_time):
        # Calcola movimento in base ai tasti premuti
        change_x = 0
        change_y = 0
        
        if self.up_pressed:
            change_y += self.velocita
        if self.down_pressed:
            change_y -= self.velocita
        if self.left_pressed:
            change_x -= self.velocita
        if self.right_pressed:
            change_x += self.velocita
        
        # Applica movimento
        self.babbo.center_x += change_x
        self.babbo.center_y += change_y
        
        # Flip orizzontale in base alla direzione
        if change_x < 0: 
            self.babbo.scale = (-1, 1)
        elif change_x > 0:
            self.babbo.scale = (1, 1)
        
        # Limita movimento dentro lo schermo
        if self.babbo.center_x < 0:
            self.babbo.center_x = 0
        elif self.babbo.center_x > self.width:
            self.babbo.center_x = self.width
        
        if self.babbo.center_y < 0:
            self.babbo.center_y = 0
        elif self.babbo.center_y > self.height:
            self.babbo.center_y = self.height
        
        # Gestione collisioni
        collisioni = arcade.check_for_collision_with_list(self.babbo, self.lista_cookie)        
        if len(collisioni) > 0: # Vuol dire che il personaggio si è scontrato con qualcosa
            if self.sound_player == None:
                self.sound_player = arcade.play_sound(self.suono_munch)
            else:    
                arcade.sound.play_sound( self.suono_munch, volume=self.suono_munch.get_volume(self.sound_player) )

            if collisioni[0].tipo == "normal":
                self.conta_biscotti_mangiati += 1
                self.testo_score.text = f"Punteggio: {self.conta_biscotti_mangiati}"
                collisioni[0].remove_from_sprite_lists()
                #print("Biscotto mangiato! Punteggio:", self.conta_biscotti_mangiati)

            elif collisioni[0].tipo == "golden":
                self.conta_biscotti_mangiati += 100
                self.testo_score.text = f"Punteggio: {self.conta_biscotti_mangiati}"
                collisioni[0].remove_from_sprite_lists()
                #print("Golden Biscotto mangiato! Punteggio:", self.conta_biscotti_mangiati)
            # Creazione nuovi biscotti in base al punteggio
            self.crea_biscotti()
                
            
       
    def crea_biscotti(self):
        #print("chiamato crea biscotti")      
        x = 1 + (self.conta_biscotti_mangiati // 5)
        while x > 0:
            #print("dentro il while")
            if self.mostra_golden_cookie():
                self.crea_cookie(tipo = "golden")
            else:
                self.crea_cookie(tipo = "normal")
            x -= 1

    def mostra_golden_cookie(self):
        return random.randint(1, 100) <= 3

    def on_key_press(self, tasto, modificatori):
        if tasto in (arcade.key.UP, arcade.key.W):
            self.up_pressed = True
        elif tasto in (arcade.key.DOWN, arcade.key.S):
            self.down_pressed = True
        elif tasto in (arcade.key.LEFT, arcade.key.A):
            self.left_pressed = True
        elif tasto in (arcade.key.RIGHT, arcade.key.D):
            self.right_pressed = True
        elif tasto == arcade.key.M:
            if self.sound_player != None:
                if self.suono_munch.get_volume(self.sound_player) == 0:
                    self.suono_munch.set_volume(1.0, self.sound_player)
                else:
                    self.suono_munch.set_volume(0.0, self.sound_player)

        

    def on_key_release(self, tasto, modificatori):
        """Gestisce il rilascio dei tasti"""
        if tasto in (arcade.key.UP, arcade.key.W):
            self.up_pressed = False
        elif tasto in (arcade.key.DOWN, arcade.key.S):
            self.down_pressed = False
        elif tasto in (arcade.key.LEFT, arcade.key.A):
            self.left_pressed = False
        elif tasto in (arcade.key.RIGHT, arcade.key.D):
            self.right_pressed = False


    


    def aggiorna_punteggio(self, nuovo_punteggio):
        self.testo_score.text = f"Punteggio: {self.conta_biscotti_mangiati}"

def main():
    gioco = BabboNatale(BabboNatale.SCREEN_WIDTH, BabboNatale.SCREEN_HEIGHT, "Babbo Natale")
    arcade.run()

if __name__ == "__main__":
    main()

