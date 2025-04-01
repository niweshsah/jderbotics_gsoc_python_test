import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

# Parameters
ARENA_SIZE = 10.0      # The arena is a square from 0 to ARENA_SIZE in both x and y.
DT = 0.1               # Time step (seconds)
SPEED = 3.0            # Linear speed (units per second)
ANGULAR_SPEED = np.deg2rad(90)  # Rotation speed when colliding (radians per second)

class BrownianRobot:
    def __init__(self, arena_size):
        # Start at the center of the arena
        self.arena_size = arena_size
        self.position = np.array([arena_size / 2, arena_size / 2])
        self.heading = np.random.uniform(0, 2 * np.pi)  # initial random heading
        self.rotating = False
        self.rotate_time = 0.0

    def update(self, dt):
        if self.rotating:
            # While in collision, rotate at a fixed angular speed
            self.heading += ANGULAR_SPEED * dt
            self.rotate_time -= dt
            if self.rotate_time <= 0:
                self.rotating = False
        else:
            # Move forward in the current heading
            displacement = np.array([np.cos(self.heading), np.sin(self.heading)]) * SPEED * dt
            self.position += displacement

            # Check for collision with the arena boundaries.
            if (self.position[0] <= 0 or self.position[0] >= self.arena_size or
                self.position[1] <= 0 or self.position[1] >= self.arena_size):
                self.rotating = True
                # Set a random rotation duration between 0.5 and 2.0 seconds.
                self.rotate_time = random.uniform(0.5, 2.0)
                # Reposition the robot inside the arena if it crosses the boundaries.
                self.position[0] = np.clip(self.position[0], 0, self.arena_size)
                self.position[1] = np.clip(self.position[1], 0, self.arena_size)

def animate(frame, robot, scatter):
    robot.update(DT)
    scatter.set_offsets(robot.position)
    return scatter,

def run_simulation():
    # Create a robot instance
    robot = BrownianRobot(ARENA_SIZE)
    
    # Set up the plot
    fig, ax = plt.subplots()
    ax.set_xlim(0, ARENA_SIZE)
    ax.set_ylim(0, ARENA_SIZE)
    ax.set_title("Brownian Motion Robot Simulation")
    scatter = ax.scatter(robot.position[0], robot.position[1], s=100, color='red')
    
    # Create animation
    ani = animation.FuncAnimation(fig, animate, fargs=(robot, scatter),
                                  frames=600, interval=50, blit=True)
    plt.show()
    # To save as video/gif, uncomment one of the following:
    ani.save("brownian_robot.mp4", writer="ffmpeg", fps=30)
    # ani.save("brownian_robot.gif", writer="imagemagick", fps=30)

if __name__ == "__main__":
    run_simulation()
