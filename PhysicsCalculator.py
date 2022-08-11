from math import *


def physicsCalculator(launchAngle, initialVelocity, height):
    # nagative velocity
    if(initialVelocity < 0):
        initialVelocity = -initialVelocity
        launchAngle += 180

    # vertical velocity component
    vy = -initialVelocity * (sin(radians(launchAngle)))
    # horizontal velocity component
    vx = initialVelocity * (cos(radians(launchAngle)))

    # acceleration due to gravity constant in  m/s**2
    g = 9.81

    # Time of Flight Calc
    # 2 * horizontal velocity / acceleration due to gravity.
    timeOfFlight = (-vy + sqrt(vy**2 + 2*g*height))/g

    # Horizontal Range Calc
    horizontalRange = timeOfFlight * vx

    # Vertical Velocity Calc
    landingVerticalVelocity = vy + g*timeOfFlight

    # Landing Angle Calc
    if(vx != 0):
        landingAngle = degrees(atan(landingVerticalVelocity/vx))
    else:
        landingAngle = 90

    # Only for consistency
    if(landingAngle < 0):
        landingAngle = 180 + landingAngle

    result = {
        "time": str(round(timeOfFlight, 8)),
        "hvelo": str(round(vx, 8)),
        "vvelo": str(round(landingVerticalVelocity, 8)),
        "landing_angle": str(round(landingAngle, 8)),
        "distance": str(round(horizontalRange, 8))

    }
    return result
