import pandas as pd


class Car:
    n = 1
    def __init__(self, l=0, x=0, y=0, free=True, full = False):
        self.l = l
        self.x, self.y = x, y
        self.free = free
        self.rides = []
        self.full = full
        self.id = Car.n
        Car.n += 1

    def add_ride(self, ride):
        if len(self.rides) == 0:
            x = 0
            y = 0
        else:
            x = self.rides[-1]['x0']
            y = self.rides[-1]['y0']
        self.l = abs(x - ride['x0']) + abs(y - ride['y0'])
        self.free = False
        self.rides.append(ride)

    def pick_guy(self, tick):
        self.full = True
        ride = self.rides[-1]
        self.l = abs(ride['x0']-ride['x1']) + abs(ride['y0']-ride['y1']) + max(ride['start']-tick, 0)

    def get_coor(self):
        if len(self.rides) == 0:
            return 0, 0
        x =self.rides[-1]['x1']
        y = self.rides[-1]['y1']
        return x, y

    def __str__(self):
        s = ''
        for ride in self.rides:
            s += ' ' + str(ride['id'])
        s='{}'.format(len(self.rides)) + s
        return s


class Ride:
    def __init__(self, row):
        self.x0 = row['x0']
        self.y0 = row['y0']
        self.x1 = row['x1']
        self.y1 = row['x2']
        self.start = row['start']
        self.finish = row['finish']
        self.id = row['id']

    def __str__(self) -> str:
        return '{} {} {} {} {} {}'.format(self.x0, self.y0, self.x1, self.y1, self.start, self.finish)

def get_closest_id(car, rides):
    x, y = car.get_coor()
    mi = 99999999
    mi_i = 0
    for i, ride in rides.iterrows():
        dist = abs(x-ride['x0']) + abs(y-ride['y0'])
        if(dist)<mi:
            mi_i = i
            mi = dist
    return mi_i

def distance(ride):
    return abs(ride[0] - ride[2]) + abs(ride[1] - ride[3])


def readFromFile(filename):
    filename = "input/" + filename + ".in"
    with open(filename) as f:
        lst = []
        for i in f:
            lst.append(list(map(int,i.split())))
    r, c, f, n, b, t = tuple(lst[0])
    new_lst = []
    for i, ride in enumerate(lst[1:]):
        new_lst.append(
            {'x0': ride[0], 'y0': ride[1], 'x1': ride[2], 'y1': ride[3], 'start': ride[4], 'finish': ride[5], 'id': i, 'dist': distance(ride[:4])})
    rides = pd.DataFrame(new_lst, dtype='int32').sort_values('dist')
    rides['index'] = range(n)
    rides = rides.set_index('index')

    cars = []
    for i in range(f):
        cars.append(Car())
    return n, t, f, rides, cars


def writeToFile(filename, cars):
    filename = "output/" + filename + "Out.txt"
    with open(filename, mode='w') as file:
        for car in cars:
            file.write(car.__str__() + '\n')



def main(filename):
    print("Reading from file...")
    n, t, f, rides, cars = readFromFile(filename)

    print(rides)

    print("\nSelecting cars for the ride...")
    i = 0
    for car in cars:
        if rides.shape[0] <= 0:
            break
        car.add_ride(rides.loc[i])
        rides = rides.drop(i)
        car.l = 0
        i += 1


    print("\nCompleting the task...")
    tick = 0
    while len(rides) > 0:
        if tick % 100 == 0:
            print(tick / len(rides))
        find = False
        for car in cars:
            if not car.full:
                car.pick_guy(tick)
            else:
                if rides.shape[0] <= 0:
                    find = True
                    break
                car.add_ride(rides.loc[i])
                rides = rides.drop(i)
                i += 1
            car.l = 0
        if find:
            break
        tick += 1

    print("\nWriting to the file...")

    writeToFile(filename, cars)

    print("\nDone!")

from time import time
start = time()
main("e_high_bonus")
print(time() - start)
