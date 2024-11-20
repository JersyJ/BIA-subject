from matplotlib import pyplot as plt
from classes import Configuration
from matplotlib.animation import FuncAnimation
from IPython.display import HTML
import math

points = []

def visualize_animated(config: Configuration, answer: list):
    global points
    fig, ax = plt.subplots()
    plot_1 = fig.add_subplot(111, projection="3d", computed_zorder=False)
    
    def animate(frame):
        global points
        # ax.view_init(elev=10, azim=10)
        for p in points: p.remove()
        points = []
        for point in answer[frame]:
            points.append(plot_1.scatter(point.x, point.y, point.z, c='black', s=10))
            # ax.plot(x_data, y_data, linestyle='solid', linewidth=2, color=line_color)

    num_frames = len(answer)
    ani = FuncAnimation(fig, animate, frames=num_frames, repeat=False, interval=500)
    return ani