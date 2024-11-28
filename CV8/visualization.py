# draw cities and answer map
from matplotlib import pyplot as plt
from classes import Config
from matplotlib.animation import FuncAnimation
from IPython.display import HTML
import math

# Visualize final path on plot
def visualize_animated(config: Config, cities: list, answer: list):
    fig, ax = plt.subplots()
    fig.suptitle(f'Animation of best ACO solution')
    points_line_1 = list()
    points_line_2 = list()

    for i in range(len(answer)):
        try:
            first = cities[answer[i]]
            secend = cities[answer[i + 1]]
            points_line_1.append([first[0], secend[0]])
            points_line_2.append([first[1], secend[1]])
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
            ax.plot([cities[answer[0]][0], cities[answer[-1]][0]], [cities[answer[0]][1], cities[answer[-1]][1]], linestyle='solid', linewidth=2, color=line_color)
    
    # Render points with label
    for j in cities:
        ax.plot(j[0], j[1], "ko", markersize=4)

    num_frames = len(answer) * 2
    ani = FuncAnimation(fig, animate, frames=num_frames, repeat=False, interval=100)
    return ani

# Visualize final path on plot
def visualize_animated_progress(config: Config, cities: list, answer: list):
    # j: City
    fig, ax = plt.subplots()
    fig.suptitle(f'Solution progress for ACO')

    def animate(frame):
        ax.clear()
        for j in cities:
            ax.plot(j[0], j[1], "ko", markersize=4)
            # ax.annotate(j.id, (j.x + 0.5, j.y + 0.5), fontsize=8)
        for idx, _ in enumerate(answer[frame]):
            try:
                city1 = cities[answer[frame][idx]]
                city2 = cities[answer[frame][idx+1]]
                ax.plot([city1[0], city2[0]], [city1[1], city2[1]], linestyle='solid', linewidth=2, color='black')
            except:
                city1 = cities[answer[frame][-1]]
                city2 = cities[answer[frame][0]]
                ax.plot([city1[0], city2[0]], [city1[1], city2[1]], linestyle='solid', linewidth=2, color='black')
    
    # Render points with label
    for j in cities:
        ax.plot(j[0], j[1], "ko", markersize=4)
        # ax.annotate(j.id, (j.x + 0.5, j.y + 0.5), fontsize=8)

    num_frames = len(answer)
    ani = FuncAnimation(fig, animate, frames=num_frames, repeat=False, interval=250)
    return ani