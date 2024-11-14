from matplotlib import pyplot
from matplotlib.animation import FuncAnimation
import matplotlib.patches as mpatches
import matplotlib as mpl
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
from copy import deepcopy

# Class representing point
class Point:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
         return f"({self.x} {self.y} {self.z})"

    def __add__(self, y):
        if type(y) is int or type(y) is float:
            self.x = self.x + y
            self.y = self.y + y
            self.z = self.z + y
            return self
        
        if type(y) is Point or type(y) is PointPSO:
            self.x = self.x + y.x
            self.y = self.y + y.y
            self.z = self.z + y.z
            return self
        raise TypeError
    
    def __radd__(self, y):
        return self + y
    
    def __sub__(self, y):
        a = deepcopy(self)
        if type(y) is int or type(y) is float:
            self.x = self.x - y
            self.y = self.y - y
            self.z = self.z - y
            return self
        
        if type(y) is Point or type(y) is PointPSO:
            a.x = self.x - y.x
            a.y = self.y - y.y
            a.z = self.z - y.z
            return a
        
        raise TypeError
    
    def __rsub__(self, y):
        return -self + y
    
    def __neg__(self):
        self.x = -self.x
        self.y = -self.y
        self.z = -self.z
        return self
    
    def __mul__(self, y):
        if type(y) is int or type(y) is float:
            self.x = self.x * y
            self.y = self.y * y
            self.z = self.z * y
            return self
        
        if type(y) is Point or type(y) is PointPSO:
            self.x = self.x * y.x
            self.y = self.y * y.y
            self.z = self.z * y.z
            return self
        
        raise TypeError
    
    def __rmul__(self, y):
        return self * y
    
    def __getitem__(self, key):
        if key == 0: return self.x
        elif key == 1: return self.y
        elif key == 2: return self.z
        else: raise Exception

    def __setitem__(self, key, value):
        if key == 0: self.x = value
        elif key == 1: self.y = value
        elif key == 2: self.z = value
        else: raise Exception

    def clip_boundaries(self, config):
        if self.x < config.range_min: self.x = config.range_min
        if self.x > config.range_max: self.x = config.range_max
        if self.y < config.range_min: self.y = config.range_min
        if self.y > config.range_max: self.y = config.range_max
        if self.z < config.range_min: self.z = config.range_min
        if self.z > config.range_max: self.z = config.range_max

    def clip_velocity(self, config):
        if self.x < config.velocity_min: self.x = config.velocity_min
        if self.x > config.velocity_max: self.x = config.velocity_max
        if self.y < config.velocity_min: self.y = config.velocity_min
        if self.y > config.velocity_max: self.y = config.velocity_max
        if self.z < config.velocity_min: self.z = config.velocity_min
        if self.z > config.velocity_max: self.z = config.velocity_max

class PointPSO(Point):
    def __init__(self, x: float, y: float, z: float, velocity: Point):
        Point.__init__(self, x, y, z)
        self.velocity = velocity
        self.pbest = Point(x,y,z)

    def clip_velocity(self, config):
        if self.velocity.x < config.velocity_min: self.velocity.x = config.velocity_min
        if self.velocity.x > config.velocity_max: self.velocity.x = config.velocity_max
        if self.velocity.y < config.velocity_min: self.velocity.y = config.velocity_min
        if self.velocity.y > config.velocity_max: self.velocity.y = config.velocity_max
        if self.velocity.z < config.velocity_min: self.velocity.z = config.velocity_min
        if self.velocity.z > config.velocity_max: self.velocity.z = config.velocity_max

# Configuration class that holds general information
class Configuration:
    def __init__(self, range_min: float, range_max: float, point_spacing: float, function: float, surface_x: float, surface_y: float, surface_z: float, surface_z_min: float):
        self.range_min = range_min
        self.range_max = range_max
        self.point_spacing = point_spacing
        self.function = function
        self.surface_x = surface_x
        self.surface_y = surface_y
        self.surface_z = surface_z
        self.surface_z_min = surface_z_min

# Modified configuration class for Particle Swarm Optimization
class PSOConfiguration(Configuration):
    def __init__(self, range_min: float, range_max: float, point_spacing: float, function: float, surface_x: float, surface_y: float, surface_z: float, surface_z_min: float, velocity_min: float, velocity_max: float):
        Configuration.__init__(self, range_min, range_max, point_spacing, function, surface_x, surface_y, surface_z, surface_z_min)
        self.velocity_min = velocity_min
        self.velocity_max = velocity_max

# Class containing all plots
class PlotNonInteractive:
    def __init__(self, config: Configuration, name: str, interactive: bool):
        self.figure = pyplot.figure(figsize=(16,10))
        self.figure.canvas.manager.set_window_title(name)
        self.plot_1 = self.figure.add_subplot(131, projection="3d", computed_zorder=False)
        self.plot_1.plot_surface(config.surface_x, config.surface_y, config.surface_z, cmap='plasma', alpha=0.5, zorder=1)
        self.plot_2 = self.figure.add_subplot(132, projection="3d", computed_zorder=False)
        self.plot_3 = self.figure.add_subplot(133, projection="3d", computed_zorder=False)
        self.plot_2.plot_surface(config.surface_x, config.surface_y, config.surface_z, cmap='plasma', alpha=1, zorder=1)
        self.plot_3.plot_surface(config.surface_x, config.surface_y, config.surface_z, cmap='jet', alpha=1, zorder=1)
        self.plot_2.view_init(elev=0, azim=0, roll=0)
        self.plot_3.view_init(elev=90, azim=0, roll=0)

    # Add to plot single point
    def add_point(self, point: list, color: str, size: float, zorder: float):
        self.plot_1.scatter(point.x, point.y, point.z, c=color, s=size, zorder=zorder)
        self.plot_2.scatter(point.x, point.y, point.z, c=color, s=size, zorder=zorder)
        self.plot_3.scatter(point.x, point.y, point.z, c=color, s=size, zorder=zorder)
    
    # Add to plot multiple point
    def add_points(self, point: list, color: str, size: float, zorder: float):
        self.plot_1.scatter(point, c=color, s=size, zorder=zorder)
        self.plot_2.scatter(point, c=color, s=size, zorder=zorder)
        self.plot_3.scatter(point, c=color, s=size, zorder=zorder)

    # Add to plots whole collection of points
    def add_points_separated(self, x: list, y: list, z: list, color: str, size: float, zorder: float):
        self.plot_1.scatter(x, y, z, c=color, s=size, zorder=zorder)
        self.plot_2.scatter(x, y, z, c=color, s=size, zorder=zorder)
        self.plot_3.scatter(x, y, z, c=color, s=size, zorder=zorder)

    def set_title(self, text: str):
        self.figure.suptitle(text, fontsize=16)

# Class containing all plots
class PlotInteractiveAnimated:
    def __init__(self, config, name, interactive):
        self.interactive = interactive
        if interactive == True:
            self.figure = pyplot.figure(figsize=(10,10))
            self.figure.canvas.manager.set_window_title(name)
            self.plot_1 = self.figure.add_subplot(111, projection="3d", computed_zorder=False)
            self.plot_1.plot_surface(config.surface_x, config.surface_y, config.surface_z, cmap='plasma', alpha=0.5, zorder=1)

    # Add to plot single point
    def add_point(self, point, color, size, zorder):
        self.sc = self.plot_1.scatter(point.x, point.y, point.z, c=color, s=size, zorder=zorder, cmap="autumn")
        pyplot.pause(0.002)

    # Add to plots whole collection of points
    def add_points_separated(self, x, y, z, color, size, zorder):
        self.sc = self.plot_1.scatter(x, y, z, c=color, s=size, zorder=zorder)

    def set_title(self, text):
        self.figure.suptitle(text, fontsize=16)

    def update(self, num, ax, scat):
        ax.view_init(elev=10, azim=num*3)
        return scat, ax
    
    def animate(self):
        pyplot.colorbar(self.sc)
        ani = FuncAnimation(self.figure, self.update, fargs=(self.plot_1, self.sc), frames=360, interval=1)
        return ani
    
class PlotLine:
    def __init__(self, data):
        # Main colors on plot
        self.color1 = (13, 37, 255)
        self.color1_normalized = (0.06, 0.145, 1)
        self.color2 = (255, 62, 48)
        self.color2_normalized = (1, 0.243, 0.188)

        # Variable and settings initialization
        self.z: list = [p.z for p in data]
        self.z_max: float = np.max(self.z)
        self.label_frequency: float = len(self.z) / 10
        self.previous_val: float = self.z_max
        self.cm = LinearSegmentedColormap.from_list("Custom", [self.color1_normalized, self.color2_normalized], N=100)
        self.norm = mpl.colors.Normalize(0, self.z_max)

        # Plot initialization and colorbar init
        self.fig, self.ax = pyplot.subplots(figsize=(12, 6))
        self.fig.colorbar(mpl.cm.ScalarMappable(norm=self.norm, cmap=self.cm), ax=self.ax)
        pyplot.axhline(y=0, color='#b8b8b8', linestyle='dotted')

        # Add points and lines into plot and calculate their color based on result value pyplot.annotate(f"First: {round(p.z, 4)}", (i + 2, p.z), c=hex_color)
        for i, p in enumerate(data):
            intensity: float = p.z / self.z_max
            color: tuple = self.calc_color(intensity, self.color1, self.color2)
            hex_color: str = '#{:02x}{:02x}{:02x}'.format(*color)
            if (self.previous_val - p.z) >= 0.5 or i % self.label_frequency == 2: 
                pyplot.annotate(round(p.z, 4), (i, p.z+0.2), c=hex_color)

            pyplot.scatter(i, p.z, c=hex_color)
            self.previous_val: float = p.z
            try:
                pyplot.plot([i, i+1], [data[i].z, data[i+1].z], c=hex_color)
            except:
                pass

        pyplot.annotate(f"First: {round(data[0].z, 4)}", (len(data) - 17, self.z_max), c='#ff3e30')
        pyplot.annotate(f"Last: {round(data[-1].z, 10)}", (len(data) - 17, self.z_max-0.2), c='#0d25ff')

        self.red_patch = mpatches.Patch(color='#ff3e30', label='Bad')
        self.blue_patch = mpatches.Patch(color='#0d25ff', label='Good')
        pyplot.legend(handles=[self.red_patch, self.blue_patch])
        pyplot.xlabel('Generations')
        pyplot.ylabel('Z coordinate (rounded to 4 decimals)')
        pyplot.title('Particle Swarm Optimization progress (lower is better)')

    # Calculate color based on two colors and value
    def calc_color(self, value: float, color1: tuple, color2: tuple):
        return (
            int(color1[0] * (1 - value) + color2[0] * value),
            int(color1[1] * (1 - value) + color2[1] * value),
            int(color1[2] * (1 - value) + color2[2] * value)
        )
    
    def show(self):
        pyplot.show()