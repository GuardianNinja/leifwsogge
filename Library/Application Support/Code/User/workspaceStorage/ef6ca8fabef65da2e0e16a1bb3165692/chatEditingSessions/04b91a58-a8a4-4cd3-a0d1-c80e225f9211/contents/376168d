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

def relativistic_time(t_seconds: float, velocity: float) -> float:
    """
    Adjusts time for relativistic effects based on velocity.
    t_seconds: elapsed time in seconds (Earth reference)
    velocity: velocity of observer in m/s
    """
    factor = math.sqrt(1 - (velocity**2 / C**2))
    return t_seconds * factor




def gravitational_time_dilation(t_seconds: float, r_distance: float) -> float:
    """
    Adjusts time for gravitational effects relative to Earth.
    t_seconds: elapsed time in seconds
    r_distance: distance from Earth's center in meters
    """
    potential = 1 - (2 * G * EARTH_MASS) / (float(r_distance) * C**2)
    if potential < 0:
        raise ValueError("Potential under square root is negative, check input values.")
    return float(t_seconds) * math.sqrt(potential)

def space_clock(velocity: float, r_distance: float) -> float:
    """
    Returns the adjusted 'space clock' time relative to Earth.
    velocity: observer velocity in m/s
    r_distance: distance from Earth's center in meters
    Returns: adjusted time in seconds (float)
    """
    earth_time = time.time()  # current UTC seconds
    rel_time = float(relativistic_time(float(earth_time), float(velocity)))
    grav_time = gravitational_time_dilation(float(rel_time), float(r_distance))
    return grav_time

# Example usage:
if __name__ == "__main__":
    # Simulate astronaut at 7.8 km/s (LEO orbit) and 400 km above Earth
    velocity: float = 7800  # m/s
    r_distance: float = EARTH_RADIUS + 400_000  # meters
    print("Space Clock Time:", space_clock(velocity, r_distance))
