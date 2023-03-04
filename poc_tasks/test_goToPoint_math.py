import math
from helpers import angle_between
from test_turn_math import turn
GRID_SIZE_CONVERSION = 1
ORIGIN = (0,0)
Y_AXIS = (0,1)

P1 = (1,1)




def goToPoint(fromPt, toPt, initRotation):

    xMove = toPt[0] - fromPt[0]
    yMove = toPt[1] - fromPt[1]

    distance = pow((GRID_SIZE_CONVERSION * xMove)**2 + (GRID_SIZE_CONVERSION * yMove)**2,.5)
    targetAngle = angle_between(Y_AXIS, (xMove, yMove))
    currRotation = initRotation

    print(distance, targetAngle, currRotation)

    turnAngle = targetAngle + currRotation

    turn(turnAngle, initRotation)

    #move(distance)
    print("moves the distance ", distance, "by turning ", turnAngle)

    return toPt
# goToPoint(ORIGIN, P1, 0)
# goToPoint(P1, ORIGIN, 45)
# goToPoint(ORIGIN, (-1, 1), 225)
# goToPoint((-1,1),ORIGIN, 495 )

def angle_between(v1, v2):
    dot_product = v1[0]*v2[0] + v1[1]*v2[1]
    v1_mag = math.sqrt(v1[0]**2 + v1[1]**2)
    v2_mag = math.sqrt(v2[0]**2 + v2[1]**2)
    cos_angle = dot_product / (v1_mag * v2_mag)
    angle_in_radians = math.acos(cos_angle)
    return math.degrees(angle_in_radians)


print(angle_between((0,1), (1,1)))

#change hte turnAngle to a +