import math
import random
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk, messagebox
import os
import subprocess

root = tk.Tk()
root.title("Новогодняя ёлка")

DEFAULT_SIZE = 300
DEFAULT_FPS = 30
anim = None
is_playing = False
save_path = os.path.abspath("Ёлка.gif")

fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(111, projection="3d")
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(pady=10)

current_size = DEFAULT_SIZE
current_fps = DEFAULT_FPS


def init_animation():
    global anim
    if anim:
        anim.event_source.stop()

    anim = animation.FuncAnimation(
        fig,
        animate,
        init_func=init_plot,
        frames=100,
        interval=1000 // current_fps,
        blit=False,
        repeat=True
    )
    anim.event_source.stop()
    canvas.draw()


def init_plot():
    ax.clear()
    ax.set_xlim(-current_size * 2, current_size * 2)
    ax.set_ylim(-current_size * 2, current_size * 2)
    ax.set_zlim(0, current_size)
    return []


def update_animation():
    global current_size, current_fps, is_playing
    try:
        new_size = int(size_entry.get())
        new_fps = int(fps_entry.get())
        if new_size > 0 and new_fps > 0:
            current_size = new_size
            current_fps = new_fps
    except ValueError:
        pass

    init_animation()
    is_playing = False
    play_button.config(text="Старт")
    canvas.draw()


def toggle_animation():
    global is_playing
    if not anim:
        return

    if is_playing:
        anim.event_source.stop()
        play_button.config(text="Старт")
    else:
        anim.event_source.start()
        play_button.config(text="Пауза")
    is_playing = not is_playing


def save_animation():
    if anim:
        anim.save(save_path, writer='pillow')
        messagebox.showinfo("Сохранено", f"GIF сохранён по пути: {save_path}")


def open_folder():
    folder_path = os.path.dirname(save_path)
    if os.name == "nt":  # Windows
        subprocess.Popen(f'explorer /select,"{save_path}"')
    elif os.name == "posix":  # macOS/Linux
        subprocess.Popen(["xdg-open", folder_path])


controls = ttk.Frame(root)
controls.pack(padx=10, pady=10)

ttk.Label(controls, text="Высота ёлки:").grid(row=0, column=0)
size_entry = ttk.Entry(controls)
size_entry.insert(0, str(DEFAULT_SIZE))
size_entry.grid(row=0, column=1)

ttk.Label(controls, text="FPS:").grid(row=1, column=0)
fps_entry = ttk.Entry(controls)
fps_entry.insert(0, str(DEFAULT_FPS))
fps_entry.grid(row=1, column=1)

apply_button = ttk.Button(controls, text="Применить", command=update_animation)
apply_button.grid(row=0, column=2, padx=5)

play_button = ttk.Button(controls, text="Старт", command=toggle_animation)
play_button.grid(row=2, column=0)

save_button = ttk.Button(controls, text="Сохранить GIF", command=save_animation)
save_button.grid(row=2, column=1)

open_folder_button = ttk.Button(controls, text="Открыть в папке", command=open_folder)
open_folder_button.grid(row=2, column=2)


def animate(f):
    ax.clear()
    k = current_size

    X = [math.cos(i / 5 + f / 10) * (k - i) for i in range(k)]
    Y = [math.sin(i / 5 + f / 10) * (k - i) for i in range(k)]
    Z = [i for i in range(k)]
    scat1 = ax.scatter(X, Y, Z, c="green", marker="^")

    step = 3
    Z_deco = [i for i in range(1, k, step)]
    X_deco = [math.cos(i / 5 + 2 + f / 10) * (k - i + 10) for i in range(1, k, step)]
    Y_deco = [math.sin(i / 5 + 2 + f / 10) * (k - i + 10) for i in range(1, k, step)]
    scat2 = ax.scatter(X_deco, Y_deco, Z_deco,
                       c=colors[random.randint(0, 7)],
                       marker="o", s=40)

    ax.set_xlim(-k * 2, k * 2)
    ax.set_ylim(-k * 2, k * 2)
    ax.set_zlim(0, k)

    return [scat1, scat2]


# Генерация цветов
number_of_colors = 8
colors = ["#" + ''.join([random.choice('0123456789') for j in range(6)])
          for i in range(number_of_colors)]

# Первоначальная инициализация
init_plot()
canvas.draw()

root.mainloop()
