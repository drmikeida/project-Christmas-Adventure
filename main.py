import pyxel
import random

class app:
    def __init__(self):
        pyxel.init(160, 120,)
        pyxel.load("my_resource.pyxres")  
        pyxel.load("my_resource.pyxres") # Load your sound effects
        
       
        self.game_state = "start" 
        self.player_x = 75
        self.player_y = 55
        self.score = 0
        self.lives = 3
        # Create collectibles (presents)
        self.collectibles = [(random.randint(10, 150), random.randint(10, 110)) for _ in range(5)]
        # Create enemy (snowball)
        self.enemy_x = random.randint(0, 160)
        self.enemy_y = random.randint(0, 120)
        self.enemy_dx = random.choice([-2, 2])
        self.enemy_dy = random.choice([-2, 2])
        # Snowfall effect
        self.snowflakes = [(random.randint(0, 160), random.randint(0, 120)) for _ in range(30)]
        pyxel.run(self.update, self.draw)
    def reset_game(self):
        self.player_x = 75
        self.player_y = 55
        self.score = 0
        self.collectibles = [(random.randint(10, 150), random.randint(10, 110)) for _ in range(5)]
        self.enemy_x = random.randint(0, 160)
        self.enemy_y = random.randint(0, 120)
    def update(self):
        if self.game_state == "start":
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.game_state = "play"
        elif self.game_state == "play":
            # Player movement
            if pyxel.btn(pyxel.KEY_UP):
                self.player_y -= 2
            if pyxel.btn(pyxel.KEY_DOWN):
                self.player_y += 2
            if pyxel.btn(pyxel.KEY_LEFT):
                self.player_x -= 2
            if pyxel.btn(pyxel.KEY_RIGHT):
                self.player_x += 2
            # Wrap around
            self.player_x %= 160
            self.player_y %= 120
            # Collectible collision
            for collectible in self.collectibles[:]:
                if abs(self.player_x - collectible[0]) < 8 and abs(self.player_y - collectible[1]) < 8:
                    self.collectibles.remove(collectible)
                    self.score += 1
                    
            # Enemy movement
            self.enemy_x += self.enemy_dx
            self.enemy_y += self.enemy_dy
            
            # Bounce the enemy off the screen edges
            if self.enemy_x <= 0 or self.enemy_x >= 160:
                self.enemy_dx *= -1
            if self.enemy_y <= 0 or self.enemy_y >= 120:
                self.enemy_dy *= -1
                
            # Enemy collision
            if abs(self.player_x - self.enemy_x) < 8 and abs(self.player_y - self.enemy_y) < 8:
                self.lives -= 1
                if self.lives == 0:
                    self.game_state = "end"
                    
            # Snowfall update
            self.snowflakes = [(x, (y + 1) % 120) for x, y in self.snowflakes]
            
            # Win condition
            if not self.collectibles:
                self.game_state = "end"
        elif self.game_state == "end":
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.reset_game()
                self.game_state = "start"
                
    def draw(self):
        pyxel.cls(0)
        if self.game_state == "start":
            pyxel.text(50, 50, "Christmas Adventure", pyxel.frame_count % 16)
            pyxel.text(40, 70, "Press ENTER to start!", 7)
        elif self.game_state == "play":
            
            # Draw snowflakes
            for x, y in self.snowflakes:
                pyxel.pset(x, y, 7)
                
            # Draw player (Santa sprite)
            pyxel.blt(self.player_x, self.player_y, 0, 0, 0, 16, 16, 0)  
            # Draw collectibles (presents)
            for collectible in self.collectibles:
                pyxel.blt(collectible[0], collectible[1], 1, 16, 0, 5, 6, 1)  
            # Enemy collision
            if abs(self.player_x - self.enemy_x) < 8 and abs(self.player_y - self.enemy_y) < 8:
                if self.lives == 0:
                        self.game_state = "end"
            # Draw enemy 
            pyxel.circ(self.enemy_x, self.enemy_y, 5, 15)

            # Draw collectibles (circles)
            for collectible in self.collectibles:
                pyxel.circ(collectible[0], collectible[1], 4, 8)   
            

            # Display score
            pyxel.text(5, 5, f"Score: {self.score}", 7)
        elif self.game_state == "end":
            if not self.collectibles:
                pyxel.text(50, 50, "You Win!", pyxel.frame_count % 16)
            else:
                pyxel.text(50, 50, "Game Over!", pyxel.frame_count % 16)
            pyxel.text(40, 70, f"Final Score: {self.score}", 7)
            pyxel.text(40, 90, "Press ENTER to restart", 7)

    

    

app()