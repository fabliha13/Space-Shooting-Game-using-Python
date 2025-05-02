import turtle
import random
import winsound
import os
import time

# Set up screen
wn = turtle.Screen()
wn.setup(800, 600)
wn.bgcolor("black")
wn.title("Space Shooting")
wn.tracer(0)

# Register shapes (images)
current_dir = os.path.dirname(__file__)
images = ["player.gif", "enemy.gif", "boss.gif", "missile.gif",
          "red_star.gif", "white_star.gif", "yellow_star.gif"]

for image in images:
    full_path = os.path.join(current_dir, image)
    wn.register_shape(full_path)

# Create classes
class Pen(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.penup()
        self.color("green")
        self.width(2)
        self.speed(0)

    def ammo_counter(self):
        ammo = 0
        for missile in missiles:
            if missile.state == "ready":
                ammo += 1

        for x in range(ammo):
            self.goto(300 + 30 * x, 280)
            self.shape(os.path.join(current_dir, "missile.gif"))
            self.stamp()

    def draw_score(self):
        self.goto(-80, 270)
        self.color("cyan")
        self.write(f"Score: {player.score}  Kills: {player.kills}", font=("Courier New", 22, "bold"))

class Player(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape(os.path.join(current_dir, "player.gif"))
        self.penup()
        self.speed(0)
        self.goto(-350, 0)
        self.dy = 0
        self.dx = 0
        self.score = 0
        self.max_health = 20
        self.health = self.max_health
        self.kills = 0

    def up(self):
        self.dy = 1.75

    def down(self):
        self.dy = -1.75

    def move_left(self):
        self.dx = -1.75

    def move_right(self):
        self.dx = 1.75

    def move(self):
        self.sety(self.ycor() + self.dy)
        self.setx(self.xcor() + self.dx)

        if self.ycor() > 280:
            self.sety(280)
            self.dy = 0
        elif self.ycor() < -280:
            self.sety(-280)
            self.dy = 0

        if self.xcor() < -380:
            self.setx(-380)
            self.dx = 0
        elif self.xcor() > -180:
            self.setx(-180)
            self.dx = 0

class Missile(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape(os.path.join(current_dir, "missile.gif"))
        self.penup()
        self.speed(0)
        self.goto(0, 1000)
        self.dx = 0
        self.state = "ready"

    def fire(self):
        self.state = "firing"
        self.goto(player.xcor(), player.ycor())
        self.dx = 2.5

    def move(self):
        if self.state == "firing":
            self.setx(self.xcor() + self.dx)
        if self.xcor() > 400:
            self.state = "ready"
            self.sety(1000)

class Enemy(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape(os.path.join(current_dir, "enemy.gif"))
        self.penup()
        self.speed(0)
        self.goto(random.randint(400, 480), random.randint(-280, 280))
        self.dx = random.randint(1, 5) / -3
        self.dy = 0
        self.max_health = random.randint(5, 15)
        self.health = self.max_health

    def move(self):
        self.setx(self.xcor() + self.dx)
        self.sety(self.ycor() + self.dy)

        if self.xcor() < -400:
            self.goto(random.randint(400, 480), random.randint(-280, 280))

        if self.ycor() < -280 or self.ycor() > 280:
            self.dy *= -1

    def boss_spawn(self):
        self.shape(os.path.join(current_dir, "boss.gif"))
        self.max_health = 50
        self.health = self.max_health
        self.dy = random.randint(-5, 5) / 3

    def enemy_respawn(self):
        self.dy = 0
        self.shape(os.path.join(current_dir, "enemy.gif"))
        self.max_health = random.randint(5, 15)
        self.health = self.max_health
        self.goto(random.randint(400, 480), random.randint(-280, 280))

class Star(turtle.Turtle):
    def __init__(self):
        super().__init__()
        star_images = ["yellow_star.gif", "red_star.gif", "white_star.gif"]
        self.shape(os.path.join(current_dir, random.choice(star_images)))
        self.penup()
        self.speed(0)
        self.goto(random.randint(-400, 400), random.randint(-290, 290))
        self.dx = random.randint(1, 5) / -20

    def move(self):
        self.setx(self.xcor() + self.dx)
        if self.xcor() < -400:
            self.goto(random.randint(400, 480), random.randint(-290, 290))

# Create game objects
pen = Pen()
player = Player()
missiles = [Missile(), Missile(), Missile()]
enemies = [Enemy() for _ in range(5)]
stars = [Star() for _ in range(30)]

# Functions
def fire_missile():
    for missile in missiles:
        if missile.state == "ready":
            missile.fire()
            winsound.PlaySound("SS_missile.wav", winsound.SND_ASYNC)
            break

def quit_game():
    global running
    running = False

# Keyboard binding
wn.listen()
wn.onkeypress(quit_game, "q")
wn.onkeypress(player.up, "Up")
wn.onkeypress(player.down, "Down")
wn.onkeypress(player.move_left, "Left")
wn.onkeypress(player.move_right, "Right")
wn.onkeypress(fire_missile, "space")

# Show the storyline
pen.goto(0, 50)
pen.color("white")
pen.write("You are an astronaut... Aliens are attacking the world...", align="center", font=("Comic sans", 16, "normal"))
# pen.goto(0, 0)
# pen.write("You need to save the Earth. Defeat 10 aliens before your life runs out to win.", align="center", font=("Comic sans", 16, "normal"))
pen.goto(0, 0)
pen.color("cyan")  # Futuristic color for the font
pen.write("You need to save the Earth.", align="center", font=("Courier New", 18, "bold"))

pen.goto(0, -50)
pen.color("cyan")  # Futuristic color for the font
pen.write('Defeat 10 aliens before your life runs out to win.', align="center", font=("Courier New", 18, "bold"))

# Wait for a key press to start
wn.update()
# wn.listen()
time.sleep(2)

# Main game loop
running = True
while running:
    wn.update()
    pen.clear()

    player.move()
    for missile in missiles:
        missile.move()
    for star in stars:
        star.move()

    for enemy in enemies:
        enemy.move()

        # Draw enemy health bar
        pen.goto(enemy.xcor() - 15, enemy.ycor() + 20)
        pen.setheading(0)
        pen.pendown()
        pen.color("red")
        pen.fd(30)
        pen.penup()

        pen.goto(enemy.xcor() - 15, enemy.ycor() + 20)
        pen.setheading(0)
        pen.pendown()
        pen.color("green")
        pen.fd(30 * (enemy.health / enemy.max_health))
        pen.penup()

        # Collision with missiles
        for missile in missiles:
            if missile.state == "firing" and enemy.distance(missile) < 20:
                winsound.PlaySound("SS_explosion.wav", winsound.SND_ASYNC)
                enemy.health -= 4
                missile.goto(0, 1000)
                missile.state = "ready"

                if enemy.health <= 0:
                    player.kills += 1
                    player.score += 10
                    if player.kills >= 10:  # Win condition
                        pen.goto(0, 0)
                        pen.color("cyan")  # Futuristic color for the font
                        pen.write("YOU WIN! You have saved the world!", align="center", font=("Courier New", 22, "bold"))
                        wn.update()
                        time.sleep(3)
                        running = False
                    else:
                        enemy.enemy_respawn()
                break

        # Collision with player
        if enemy.distance(player) < 20:
            winsound.PlaySound("SS_explosion.wav", winsound.SND_ASYNC)
            damage = random.randint(5, 10)
            player.health -= damage
            enemy.health -= damage

            if enemy.health <= 0:
                player.kills += 1
                player.score += 10
                enemy.enemy_respawn()
            else:
                enemy.setx(enemy.xcor() + 40)

            if player.health <= 0:  # Game Over condition
                pen.goto(0, 0)
                pen.color("cyan")  # Futuristic color for the font
                pen.write("GAME OVER :(", align="center", font=("Courier New", 22, "bold"))
                wn.update()
                time.sleep(3)
                running = False

    # Draw player health bar
    pen.goto(player.xcor() - 20, player.ycor() + 20)
    pen.setheading(0)
    pen.pendown()
    pen.color("red")
    pen.fd(40)
    pen.penup()

    pen.goto(player.xcor() - 20, player.ycor() + 20)
    pen.setheading(0)
    pen.pendown()
    pen.color("green")
    pen.fd(40 * (player.health / player.max_health))
    pen.penup()

    pen.ammo_counter()
    pen.draw_score()
