# Space Clock Prototype
# Author: Leif William Sogge
# Purpose: A mathematical clock for Earth + space navigation

import math
import time

# Constants
C = 299_792_458  # speed of light in m/s
EARTH_RADIUS = 6_371_000  # meters
EARTH_MASS = 5.972e24  # kg
G = 6.67430e-11  # gravitational constant

def relativistic_time(t_seconds, velocity):
    """
    Adjusts time for relativistic effects based on velocity.
    t_seconds: elapsed time in seconds (Earth reference)
    velocity: velocity of observer in m/s
    """
    factor = math.sqrt(1 - (velocity**2 / C**2))
    return t_seconds * factor

def gravitational_time_dilation(t_seconds, r_distance):
    """
    Adjusts time for gravitational effects relative to Earth.
    t_seconds: elapsed time in seconds
    r_distance: distance from Earth's center in meters
    """
    potential = 1 - (2 * G * EARTH_MASS) / (r_distance * C**2)
    return t_seconds * math.sqrt(potential)

def space_clock(velocity, r_distance):
    """
    Returns the adjusted 'space clock' time relative to Earth.
    velocity: observer velocity in m/s
    r_distance: distance from Earth's center in meters
    """
    earth_time = time.time()  # current UTC seconds
    rel_time = relativistic_time(earth_time, velocity)
    grav_time = gravitational_time_dilation(rel_time, r_distance)
    return grav_time

# Example usage:
if __name__ == "__main__":
    # Simulate astronaut at 7.8 km/s (LEO orbit) and 400 km above Earth
    velocity = 7800  # m/s
    r_distance = EARTH_RADIUS + 400_000  # meters
    print("Space Clock Time:", space_clock(velocity, r_distance))
