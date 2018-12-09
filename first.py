import pandas as pd


class Car:
    n = 1 # Global id of the car
    def __init__(self, l=0, x=0, y=0, free=True, full = False): # Initializing of the car class
        self.l = l # Passed length
        self.x, self.y = x, y # Position of the car
        self.free = free # Whether the car is already in use
        self.rides = [] # Completed rides
        self.full = full # Whether the car has already started the ride
        self.id = Car.n # Id of the car
        Car.n += 1 # Increase id for the next car

    def add_ride(self, ride): # Add ride to the list of rides
        if len(self.rides) == 0: # If the car in started position
            x = 0 # Set x
            y = 0 # Set y
        else: # If the car has already finished almost one ride
            x = self.rides[-1]['x0'] # Set x
            y = self.rides[-1]['y0'] # Set y
        self.l = abs(x - ride['x0']) + abs(y - ride['y0']) # Find the length which the car will pass after during the ride
        self.free = False # The car in use
        self.rides.append(ride) # Add the ride to the list of all rides

    def pick_guy(self, tick): # Pick someone
        self.full = True # The car is started the ride
        ride = self.rides[-1] # Get the last ride
        self.l = abs(ride['x0']-ride['x1']) + abs(ride['y0']-ride['y1']) + max(ride['start']-tick, 0) # Get the length of the ride + time of waiting

    def get_coor(self): # Get the coordinates of the position of the car
        if len(self.rides) == 0: # If the car has not completed almost 1 ride
            return 0, 0
        x = self.rides[-1]['x1'] # Get the coordinates of the finish of the last ride
        y = self.rides[-1]['y1']
        return x, y

    def __str__(self): # Return the class in the string format
        s = ''
        for ride in self.rides:
            s += ' ' + str(ride['id'])
        s='{}'.format(len(self.rides)) + s
        return s


class Ride:
    def __init__(self, row):
        self.x0 = row['x0'] # Set the started position of the ride: x
        self.y0 = row['y0'] # Set the started position of the ride: y
        self.x1 = row['x1'] # Set the finished position of the ride: x
        self.y1 = row['x2'] # Set the finished position of the ride: y
        self.start = row['start'] # Earliest start
        self.finish = row['finish'] # Latest finish
        self.id = row['id'] # Id of the ride

    def __str__(self): # Return the class in the string format
        return '{} {} {} {} {} {}'.format(self.x0, self.y0, self.x1, self.y1, self.start, self.finish)

def get_closest_id(car, rides): # Find the closest car to the car
    x, y = car.get_coor() # Get coordinates of the car
    mi = 99999999 # Just a big value
    mi_i = 0 # Just a small value
    for i, ride in rides.iterrows(): # Iterate over not completed rides
        dist = abs(x-ride['x0']) + abs(y-ride['y0'])  # Find the distance from the car to the ride
        if(dist)<mi: # Check whether it is better than the previous one
            mi_i = i # Put the index of the better ride
            mi = dist # Distance of the better ride
    return mi_i # Return the index of the closes ride

def distance(ride): # Find the distance between two coordinates
    return abs(ride[0] - ride[2]) + abs(ride[1] - ride[3])


def readFromFile(filename): # Read data from the file
    filename = "input/" + filename + ".in" # Get the path to the file
    with open(filename) as f: # Open the file
        lst = [] # Empty list to store data from the file
        for i in f: # Iterate over rows in the file
            lst.append(list(map(int,i.split()))) # Add row to the file
    r, c, f, n, b, t = tuple(lst[0]) # Uncover first rows
    new_lst = [] # Empty list to store rides
    for i, ride in enumerate(lst[1:]): # Iterate over rows of rides
        new_lst.append( # Add the ride to the list
            {'x0': ride[0], 'y0': ride[1], 'x1': ride[2], 'y1': ride[3], 'start': ride[4], 'finish': ride[5], 'id': i, 'dist': distance(ride[:4])})
    rides = pd.DataFrame(new_lst, dtype='int32').sort_values('dist') # Store all rides in the pandas dataframe and sort them by distance
    rides['index'] = range(n) # Add indexes to the file
    rides = rides.set_index('index') # Set indexes for the rides

    cars = [] # List to store cars
    for i in range(f): # Create f(number) of cars
        cars.append(Car())
    return t, rides, cars # Return steps, rides and cars


def writeToFile(filename, cars): # Write rides to the file
    filename = "output/" + filename + "Out.txt" # Get the path to the file
    with open(filename, mode='w') as file: # Open that file
        for car in cars: # Write to the file completed rides of every car
            file.write(car.__str__() + '\n')



def main(filename): # Main function
    print("Reading from file...") # Just an output
    t, rides, cars = readFromFile(filename) # Call the function to read data from file

    print("\nSelecting cars for the ride...") # Just an output
    i = 0
    for car in cars: # Iterate over cars
        if rides.shape[0] <= 0: # If it is some rides in the list
            break
        car.add_ride(rides.loc[i]) # Add the ride for the car
        rides = rides.drop(i) # Delete the row with that ride from the table
        i += 1 # Get the index of the next ride from the table


    print("\nCompleting the task...") # Just an output
    tick = 0 # Number of steps
    while len(rides) > 0: # Loop till some rides in the table
        if tick % 100 == 0: # Just to know how many percent completed
            print(tick / len(rides)) # Percent
        for car in cars: # Iterate over cars
            if not car.full: # If the car is empty
                car.pick_guy(tick) # Pick someone
            else: # If the car is full
                car.add_ride(rides.loc[i]) # Add the ride to the car
                rides = rides.drop(i) # Drop it from the table
                i += 1 # Get the index of the next ride
            car.l = 0 # Set length for the car
        tick += 1 # Increase tick

    print("\nWriting to the file...") # Just an output

    writeToFile(filename, cars) # Write data to the file

    print("\nDone!") # Just an output

from time import time
start = time()
main("e_high_bonus")
print(time() - start)
