import tkinter as tk
import random

root = tk.Tk()
root.title("Flappy Bird - Python")
root.attributes("-fullscreen", True)
root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))

WIDTH = root.winfo_screenwidth()
HEIGHT = root.winfo_screenheight()
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, highlightthickness=0)
canvas.pack(fill="both", expand=True)

SCALE = min(WIDTH / 1920, HEIGHT / 1080)
def scale(value): return max(1, int(value * SCALE))

GRAVITY = 0.55 * SCALE
JUMP = -10 * SCALE
PIPE_SPEED = 6 * SCALE
PIPE_WIDTH = scale(100)
PIPE_GAP = scale(300)
BIRD_SIZE = scale(55)
GROUND_HEIGHT = scale(100)

bird_x = WIDTH * 0.25
bird_y = HEIGHT * 0.45
velocity = 0
score = 0
game_over = False
pipes = []

canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill="#70c5ce", outline="")

def create_cloud(x, y, size):
    canvas.create_oval(x, y, x + size, y + size * .6, fill="white", outline="")
    canvas.create_oval(x + size*.3, y - size*.2, x + size*.9, y + size*.5, fill="white", outline="")
    canvas.create_oval(x + size*.6, y, x + size*1.3, y + size*.6, fill="white", outline="")

create_cloud(WIDTH*.10, HEIGHT*.15, scale(100))
create_cloud(WIDTH*.55, HEIGHT*.10, scale(130))
create_cloud(WIDTH*.80, HEIGHT*.25, scale(90))

canvas.create_rectangle(0, HEIGHT-GROUND_HEIGHT, WIDTH, HEIGHT, fill="#ded895", outline="")
canvas.create_rectangle(0, HEIGHT-GROUND_HEIGHT, WIDTH, HEIGHT-GROUND_HEIGHT+scale(15), fill="#70c738", outline="")

bird = canvas.create_oval(bird_x, bird_y, bird_x+BIRD_SIZE, bird_y+BIRD_SIZE, fill="#ffd900", outline="#d49b00", width=scale(3))
wing = canvas.create_oval(bird_x+scale(8), bird_y+scale(25), bird_x+scale(30), bird_y+scale(42), fill="#f0b900", outline="#c99400", width=scale(2))
eye = canvas.create_oval(bird_x+scale(35), bird_y+scale(8), bird_x+scale(48), bird_y+scale(21), fill="white", outline="black")
pupil = canvas.create_oval(bird_x+scale(40), bird_y+scale(10), bird_x+scale(46), bird_y+scale(17), fill="black")
beak = canvas.create_polygon(bird_x+BIRD_SIZE, bird_y+scale(23), bird_x+BIRD_SIZE+scale(25), bird_y+scale(30), bird_x+BIRD_SIZE, bird_y+scale(37), fill="#ff8c00", outline="#c65d00", width=scale(2))
score_text = canvas.create_text(WIDTH/2, scale(80), text="0", font=("Arial", scale(55), "bold"), fill="white")

def create_pipe():
    gap_center = random.randint(int(HEIGHT*.30), int(HEIGHT*.65))
    gap_top = gap_center - PIPE_GAP//2
    gap_bottom = gap_center + PIPE_GAP//2
    top = canvas.create_rectangle(WIDTH, 0, WIDTH+PIPE_WIDTH, gap_top, fill="#4ecb3f", outline="#268b24", width=scale(4))
    top_cap = canvas.create_rectangle(WIDTH-scale(8), gap_top-scale(35), WIDTH+PIPE_WIDTH+scale(8), gap_top, fill="#4ecb3f", outline="#268b24", width=scale(4))
    bottom = canvas.create_rectangle(WIDTH, gap_bottom, WIDTH+PIPE_WIDTH, HEIGHT-GROUND_HEIGHT, fill="#4ecb3f", outline="#268b24", width=scale(4))
    bottom_cap = canvas.create_rectangle(WIDTH-scale(8), gap_bottom, WIDTH+PIPE_WIDTH+scale(8), gap_bottom+scale(35), fill="#4ecb3f", outline="#268b24", width=scale(4))
    pipes.append({"top": top, "top_cap": top_cap, "bottom": bottom, "bottom_cap": bottom_cap, "x": WIDTH, "scored": False})

def move_bird():
    global bird_y, velocity
    velocity += GRAVITY
    bird_y += velocity
    canvas.coords(bird, bird_x, bird_y, bird_x+BIRD_SIZE, bird_y+BIRD_SIZE)
    canvas.coords(wing, bird_x+scale(8), bird_y+scale(25), bird_x+scale(30), bird_y+scale(42))
    canvas.coords(eye, bird_x+scale(35), bird_y+scale(8), bird_x+scale(48), bird_y+scale(21))
    canvas.coords(pupil, bird_x+scale(40), bird_y+scale(10), bird_x+scale(46), bird_y+scale(17))
    canvas.coords(beak, bird_x+BIRD_SIZE, bird_y+scale(23), bird_x+BIRD_SIZE+scale(25), bird_y+scale(30), bird_x+BIRD_SIZE, bird_y+scale(37))

def move_pipes():
    global score
    for pipe in pipes[:]:
        pipe["x"] -= PIPE_SPEED
        for key in ("top", "top_cap", "bottom", "bottom_cap"):
            canvas.move(pipe[key], -PIPE_SPEED, 0)
        if not pipe["scored"] and pipe["x"] + PIPE_WIDTH < bird_x:
            pipe["scored"] = True
            score += 1
            canvas.itemconfig(score_text, text=str(score))
        if pipe["x"] + PIPE_WIDTH < 0:
            for key in ("top", "top_cap", "bottom", "bottom_cap"):
                canvas.delete(pipe[key])
            pipes.remove(pipe)

def collision():
    if bird_y <= 0 or bird_y+BIRD_SIZE >= HEIGHT-GROUND_HEIGHT:
        return True
    left, right, top_b, bottom_b = bird_x, bird_x+BIRD_SIZE, bird_y, bird_y+BIRD_SIZE
    for pipe in pipes:
        top = canvas.coords(pipe["top"])
        bottom = canvas.coords(pipe["bottom"])
        if right > top[0] and left < top[2] and top_b < top[3]: return True
        if right > bottom[0] and left < bottom[2] and bottom_b > bottom[1]: return True
    return False

def jump(event=None):
    global velocity
    if not game_over: velocity = JUMP

def show_game_over():
    canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill="black", stipple="gray50", tags="gameover")
    canvas.create_text(WIDTH/2, HEIGHT/2-scale(80), text="GAME OVER", font=("Arial", scale(70), "bold"), fill="red", tags="gameover")
    canvas.create_text(WIDTH/2, HEIGHT/2, text=f"Puntuación: {score}", font=("Arial", scale(35), "bold"), fill="white", tags="gameover")
    canvas.create_text(WIDTH/2, HEIGHT/2+scale(70), text="Presiona R para volver a jugar", font=("Arial", scale(25), "bold"), fill="white", tags="gameover")
    canvas.create_text(WIDTH/2, HEIGHT/2+scale(115), text="ESC = salir de pantalla completa", font=("Arial", scale(18)), fill="white", tags="gameover")

def restart(event=None):
    global bird_y, velocity, score, game_over
    if not game_over: return
    for pipe in pipes:
        for key in ("top", "top_cap", "bottom", "bottom_cap"): canvas.delete(pipe[key])
    pipes.clear()
    canvas.delete("gameover")
    bird_y, velocity, score, game_over = HEIGHT*.45, 0, 0, False
    canvas.itemconfig(score_text, text="0")
    game_loop()

def game_loop():
    global game_over
    if game_over: return
    move_bird(); move_pipes()
    if len(pipes) == 0 or pipes[-1]["x"] < WIDTH-scale(450): create_pipe()
    if collision():
        game_over = True
        show_game_over()
        return
    root.after(16, game_loop)

root.bind("<space>", jump)
root.bind("<r>", restart)
root.bind("<R>", restart)
game_loop()
root.mainloop()
