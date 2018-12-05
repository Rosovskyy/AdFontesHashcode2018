class Car:
    n = 0 # Global id of the car
    def __init__(self): # Initializing of the car class
        self.time = 0 # Time, which the car spend
        self.rides = [] # List of all completed rides of the certain car
        self.id = Car.n # Give the id for the certain car
        Car.n += 1 # Increase id

    def add_ride(self, ride, leftTime): # Selecting the ride for the car
        self.increaseTime(ride, leftTime)
        self.rides.append(ride) # Adding the ride to the list of completed rides

    def increaseTime(self, ride, leftTime): # Finding the total time in the road for the car
        self.time += leftTime + ride.time

    def getTheLastRide(self): # Return the last ride from rides list
        if len(self.rides) > 0: # If the car has already completed almost 1 ride
            return self.rides[-1]
        return None # If it is the first ride

    def solution(self): # The data about the instance, which will be written to the file
        return '{} {}\n'.format(len(self.rides), ' '.join([str(ride.id) for ride in self.rides]))

    def __str__(self): # String output of the instance of the class
        st = "Id: {}, Time: {}, Rides: {}"
        return st.format(self.id, self.time, self.rides)


class Ride:
    n = 0 # Global id of the ride
    def __init__(self, rows): # Initializing of the ride class
        x0, y0, x1, y1, t1, t2 = list(map(int, rows.split(' '))) # Get the values from the tuple
        self.start_position = (x0, y0) # Start position of the ride
        self.finish_position = (x1, y1) # Finish position of the ride
        self.start_time = t1+1 # Earliest start
        self.finish_time = t2-1 # Latest finish
        self.id = Ride.n # The id of the ride
        self.findTheTimeOfTheRide()
        Ride.n += 1 # Increasing the id

    def findTheTimeOfTheRide(self): # Find the time, which we need to get from start position to finish one
        self.time = self.distance(self.start_position, self.finish_position)

    @staticmethod
    def distance(start, finish): # Getting the distance from one position to another
        return abs(start[0] - finish[0]) + abs(start[1] - finish[1])

    def distToStartedPost(self): # Getting the distance from the position to the (0, 0)
        startPosition = (0, 0) # Started position
        dist = Ride.distance(startPosition, self.start_position) # Find distance between (0, 0) and the position of the ride start
        leftTime = self.start_time - dist # Check how many time we have to get to the start of the ride
        if leftTime <= 1:
            return dist
        return dist + leftTime # It is when we come earlier and we need to wait

    def __str__(self): # String output of the instance of the class
        st = 'Id: {}, Start: {}, Finish: {}, EarliestStart: {}, LatestFinish: {}'
        return st.format(self.id, self.start_position, self.finish_position, self.start_time, self.finish_time)


def compareRide(last_ride, ride, time):
    dist = Ride.distance(last_ride.finish_position, ride.start_position) # Find the distance
    if dist + time + ride.time > ride.finish_time:
        return float("inf") # Just return a big value
    leftTime = ride.start_time - (time + dist) # How many time we have to the latest finish
    leftTime = 0 if leftTime < 0 else leftTime
    return dist + leftTime


def findRide(last_ride, rides, time):
    best_ride, leftTime = -1, -1 # Just an initializing of the variables
    for i, ride in enumerate(rides): # Iterating over our rides
        tmp = compareRide(last_ride, ride, time) # Check whether we make it to the latest finish
        if (tmp < leftTime or leftTime == -1): # or leftTime == -1, because we need to choose at least 1 ride
            best_ride = i # Setting the rides list to the best ride
            leftTime = tmp # Time that we have before the earliest start
    return rides.pop(best_ride), leftTime


def read_from_file(path): # Getting the data from the file
    path = "input/" + path + ".in" # Get the path from which we need to get our data
    f = open(path) # Open the file
    params = tuple(map(int, f.readline().split(' '))) # Get our main data(first line of the file)
    rides = [Ride(line) for line in f] # Add rides to the list
    f.close() # Close thefile
    cars = [Car() for i in range(params[2])] # Create empty cars and add them to the list
    return rides, cars, params[-1] # Return rides, cars and number of steps


def write_to_file(path, cars): # Writing result to the file
    path = "output/" + path + "Out.txt" # Get the path in which we need to write results
    with open(path, mode='w') as f: # Open the file to write to it
        for car in cars: # Iterate over cars
            f.write(car.solution()) # Write rides of the certain car


def main(filename):
    print("Reading from the file...")
    rides, cars, steps = read_from_file(filename)    # Getting rides and cars
    rides = sorted(rides, key=Ride.distToStartedPost)  # Sort rides due to the distance from the started_pos to (0,0)

    print("\nSelecting cars for the ride...")
    for car in cars: # Give for cars the closest rides
        ride = rides.pop(0) # Get the the closest ride
        car.add_ride(ride, ride.distToStartedPost()) # Add the ride for the car

    print("\nCompleting the task...")
    step = 0 # Define the first step
    while len(rides) > 0 and step < steps: # While we have any possible rides, which we haven't already finished
        for car in cars: # Going through cars
            if len(rides) > 0: # Check whether it is possible rides
                last = car.getTheLastRide() # Get the ride, which the car has already been finished
                if last is not None: # If the car has already completed any ride
                    ride, time = findRide(last, rides, car.time) # Sorting for the starting time
                    car.add_ride(ride, time) # Add the ride for the car
                else:
                    ride = rides.pop(0) # Get the closest ride to the (0, 0) coordinate
                    time = ride.distToStartedPost() # Get the distance to the started position
                    car.add_ride(ride, time) # Add the ride for the car
            else: # If it is no rides
                break
        step += 1 # Increase the step

    print("\nWriting to the file...")
    write_to_file(filename, cars) # Write results to the file

    print("\nDone!")


from time import time
start = time()
main("e_high_bonus")
print(time() - start)