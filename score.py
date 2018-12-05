import pandas as pd


def distanceBetweenTwoCoord(first, second=None):
    if second == None:
        return abs(first[0] - first[2]) + abs(first[1] - first[3])
    return abs(first[0] - second[0]) + abs(first[1] + second[1])


def getPoints(data, rides, bonus):
    row = data.iloc[rides[0]]
    start_position = (row["x0"], row["y0"])
    current = distanceBetweenTwoCoord((0, 0), start_position)
    points = 0
    for ride in rides:
        row = data.iloc[ride]
        while current < row["start"]:
            current += 1
        if current == row["start"]:
            points = bonus
        if current <= row["finish"]:
            points += distanceBetweenTwoCoord((row["x1"], row["y1"]), (row["x0"], row["y0"]))
        current += distanceBetweenTwoCoord((row["x1"], row["y1"]), (row["x0"], row["y0"]))
    return points

def readOutputFile(filename):
    filename = "output/" + filename + "Out.txt"
    f = open(filename)
    completedRides = []
    for i in f:
        ride = list(map(int, i.split(" ")))
        completedRides.append(ride[1:])
    return completedRides


def readInputFile(filename):
    filename = "input/" + filename + ".in"
    with open(filename) as f:
        lst = []
        for i in f:
            lst.append(list(map(int, i.split())))
    r, c, f, n, b, t = tuple(lst[0])
    new_lst = []
    for i, ride in enumerate(lst[1:]):
        new_lst.append(
            {'x0': ride[0], 'y0': ride[1], 'x1': ride[2], 'y1': ride[3], 'start': ride[4], 'finish': ride[5], 'id': i,
             'dist': distanceBetweenTwoCoord(ride)})
    rides = pd.DataFrame(new_lst, dtype='int32') # .sort_values('start')
    rides['index'] = range(n)
    rides = rides.set_index('index')
    return lst[0], rides


def findScore(filename):
    params, rides = readInputFile(filename)
    completedRides = readOutputFile(filename)
    score = 0 #rides['dist'].sum()
    for number, i in enumerate(completedRides):
        if (number % 10 == 0):
            print(number / len(completedRides))
        score += getPoints(rides, i, params[-2])
    return score


def main():
    totalScore = 0
    for i in ["a_example", "b_should_be_easy", "c_no_hurry", "d_metropolis", "e_high_bonus"]:
        score = findScore(i)
        totalScore += score
        print(score)

    print(totalScore)


main()

