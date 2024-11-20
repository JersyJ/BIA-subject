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
        
        if type(y) is Point or type(y) is PointPSO or type(y) is PointSOMA:
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
        
        if type(y) is Point or type(y) is PointPSO or type(y) is PointSOMA:
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
        
        if type(y) is Point or type(y) is PointPSO or type(y) is PointSOMA:
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

class PointSOMA(Point):
    def __init__(self, x: float, y: float, z: float, prt: Point):
        Point.__init__(self, x, y, z)
        self.prt = prt

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

# Modified configuration class for SOMA
class SOMAConfiguration(Configuration):
    def __init__(self, range_min: float, range_max: float, point_spacing: float, function: float, surface_x: float, surface_y: float, surface_z: float, surface_z_min: float):
        Configuration.__init__(self, range_min, range_max, point_spacing, function, surface_x, surface_y, surface_z, surface_z_min)

# Class containing all plots
class PlotInteractiveAnimated:
    def __init__(self, config, name, interactive, data):
        self.data = data
        self.frames = 0
        self.interactive = interactive
        self.figure = pyplot.figure(figsize=(10,10))
        self.figure.canvas.manager.set_window_title(name)
        self.plot_1 = self.figure.add_subplot(111, projection="3d", computed_zorder=False)
        self.plot_1.plot_surface(config.surface_x, config.surface_y, config.surface_z, cmap='plasma', alpha=0.5, zorder=1)
        self.points = self.plot_1.scatter([], [], [], c='black', label='idk')

    # Add to plot single point
    def add_point(self, point, color, size, zorder):
        self.sc = self.plot_1.scatter(point.x, point.y, point.z, c=color, s=size, zorder=zorder, cmap="autumn")

    # Add to plots whole collection of points
    def add_points_separated(self, x, y, z, color, size, zorder):
        self.sc = self.plot_1.scatter(x, y, z, c=color, s=size, zorder=zorder)

    def init(self):
        return self.points

    def set_title(self, text):
        self.figure.suptitle(text, fontsize=16)

    def update(self, num):
        self.plot_1.view_init(elev=25, azim=num*2)
        if num % 6 == 0:
            points = self.data[self.frames]
            self.frames += 1
            x = [p.x for p in points]
            y = [p.y for p in points]
            z = [p.z for p in points]
            self.points._offsets3d = (x,y,z)

        return self.points
    
    def animate(self):
        # pyplot.colorbar(self.sc)
        ani = FuncAnimation(self.figure, self.update, frames=len(self.data), interval=100, init_func=self.init)
        return ani