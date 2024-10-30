# draw cities and answer map
from matplotlib import pyplot as plt
from classes import City, Config
from matplotlib.animation import FuncAnimation
from IPython.display import HTML
import math

# Visualize final path on plot
def visualize(city: list, answer: list):
    j: City

    # Render points with label
    for j in city:
        plt.plot(j.x, j.y, "ko")
        plt.annotate(j.id, (j.x + 0.5, j.y + 0.5), fontsize=8)

    # Render city lines
    for i in range(len(answer)):
        try:
            first = answer[i]
            secend = answer[i + 1]
            plt.plot([first.x, secend.x], [first.y, secend.y], linestyle='dotted', linewidth=1, color="black")
        except:
            continue

    first = answer[0]
    secend = answer[-1]
    plt.plot([first.x, secend.x], [first.y, secend.y], linestyle='dotted', linewidth=1, color="black")

    plt.show()

# Visualize final path on plot
def visualize_animated(config: Config, answer: list):
    j: City
    fig, ax = plt.subplots()
    fig.suptitle(f'TSP solution ({len(config.cities)} cities, {config.generations} G, {config.population_size} PS, {config.mutation_rate} MR, {config.crossover_rate} CR)')
    points_line_1 = list()
    points_line_2 = list()

    for i in range(len(answer)):
        try:
            first = answer[i]
            secend = answer[i + 1]
            points_line_1.append([first.x, secend.x])
            points_line_2.append([first.y, secend.y])
        except:
            continue

    def animate(frame):
        if frame % 2 == 1:  line_color = "#14ad00"
        else:               line_color = "black"

        try:
            x_data = points_line_1[math.ceil(frame / 2)]
            y_data = points_line_2[math.ceil(frame / 2)]
            ax.plot(x_data, y_data, linestyle='solid', linewidth=2, color=line_color)
        except:
            ax.plot([answer[0].x, answer[-1].x], [answer[0].y, answer[-1].y], linestyle='solid', linewidth=2, color=line_color)
    
    # Render points with label
    for j in config.cities:
        ax.plot(j.x, j.y, "ko", markersize=4)
        ax.annotate(j.id, (j.x + 0.5, j.y + 0.5), fontsize=8)

    num_frames = len(answer) * 2
    ani = FuncAnimation(fig, animate, frames=num_frames, repeat=False, interval=100)
    return ani

# Visualize final path on plot
def visualize_animated_progress(config: Config, answer: list):
    j: City
    fig, ax = plt.subplots()
    fig.suptitle(f'TSP solution ({len(config.cities)} cities, {config.generations} G, {config.population_size} PS, {config.mutation_rate} MR, {config.crossover_rate} CR)')

    def animate(frame):
        ax.clear()
        for j in config.cities:
            ax.plot(j.x, j.y, "ko", markersize=4)
            ax.annotate(j.id, (j.x + 0.5, j.y + 0.5), fontsize=8)
        for idx, _ in enumerate(answer[frame]):
            try:
                ax.plot([answer[frame][idx].x, answer[frame][idx+1].x], [answer[frame][idx].y, answer[frame][idx+1].y], linestyle='solid', linewidth=2, color='black')
            except:
                ax.plot([answer[frame][-1].x, answer[frame][0].x], [answer[frame][-1].y, answer[frame][0].y], linestyle='solid', linewidth=2, color='black')
    
    # Render points with label
    for j in config.cities:
        ax.plot(j.x, j.y, "ko", markersize=4)
        ax.annotate(j.id, (j.x + 0.5, j.y + 0.5), fontsize=8)

    num_frames = len(answer)
    ani = FuncAnimation(fig, animate, frames=num_frames, repeat=False, interval=100)
    return ani