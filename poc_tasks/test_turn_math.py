##turns to the angle provided

def turnTo(toDegree, initDegree = 0):
    print("@turn: initDegree = ", initDegree)
    change = 0
    #begin to turn

    #go cw -> right
    if(toDegree < 0):
        change = -2

    #go ccw -> left
    elif(toDegree > 0):
        change = 2
    else:
        print("@turn ERROR !!!!! no turn by 0 degree")
        return 0

    currDegree = initDegree + change
    print("@turn: currDegree = ", currDegree, "running: ", abs(currDegree) - abs(initDegree), " < ", abs(toDegree) - abs(initDegree))

    while(abs(currDegree) - abs(initDegree) < abs(toDegree) - abs(initDegree)):
        currDegree += change
        print("@turn: currDegree = ", currDegree, "running: ", abs(currDegree) - abs(initDegree), " < ", abs(toDegree) - abs(initDegree))

    print("@turn: stopping")
    print("Final: ", currDegree)



def turn(delta, initDegree = 0):
    print("@turn: initDegree = ", initDegree)
    change = 0
    target = initDegree + delta

    currDegree = initDegree
    #begin to turn

    #go cw -> right
    if(delta < 0):
        change = -2
        while(currDegree > target):
            currDegree += change
            print("@turn: currDegree = ", currDegree, "running: ", abs(currDegree) - abs(initDegree), " < ", abs(delta))

    #go ccw -> left
    elif(delta > 0):
        change = 2
        while(currDegree < target):
            currDegree += change
        print("@turn: currDegree = ", currDegree, "running: ", abs(currDegree) - abs(initDegree), " < ", abs(delta))
    else:
        print("@turn ERROR !!!!! no turn by 0 degree")
        return 0

    

   


    print("@turn: stopping")
    print("Final: ", currDegree)

# def turn(delta, initDegree = 0):
#     print("@turn: initDegree = ", initDegree)
#     change = 0
#     #begin to turn

#     #go cw -> right
#     if(delta < 0):
#         change = -2

#     #go ccw -> left
#     elif(delta > 0):
#         change = 2
#     else:
#         print("@turn ERROR !!!!! no turn by 0 degree")
#         return 0

#     currDegree = abs(initDegree)
#     print("@turn: currDegree = ", currDegree, "running: ", abs(currDegree) - abs(initDegree), " < ", abs(delta))

#     while(abs(currDegree) - abs(initDegree) < abs(delta)):
#         currDegree += change
#         print("@turn: currDegree = ", currDegree, "running: ", abs(currDegree) - abs(initDegree), " < ", abs(delta))

#     print("@turn: stopping")
#     print("Final: ", currDegree)


##Test cases

#turnTo(90, 0)

#turnTo(-180,0)

#turnTo(90, 36)

#turnTo(90, -36)

#turn(90,36)
#turn(90, -36)
#turn(-90, -45)
#turn(360, 720)
#turn(-360, 720)

#turnTo()