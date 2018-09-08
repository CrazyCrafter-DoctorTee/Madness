import random
import math

#define the map size to generate

# generated maps are squares
class Mapgenerator:

    def __init__(self, size):
        self.size = size

    #generates default map with random fill generated from a weighted list
    def genBasicMatrix(self):
        matrix = []
        choiceList = []
        for i in range(28):
            choiceList.append('g')
        for i in range(3):
            choiceList.append('t')
        for i in range(1):
            choiceList.append('b')
        for x in range(self.size):
            line = []
            for y in range(self.size):
                line.append(random.choice(choiceList))
            matrix.append(line)

        return matrix

    #Outputs the map to file
    def makemap(self,matrix):
        garbo = open("assets/map.map", "w")
        height = str(len(matrix))
        width = str(len(matrix[0]))
        garbo.write(height + " " + width + "\n")
        for line in matrix:
            for char in line:
                garbo.write(char + " ")
            garbo.write('\n')

    #draws a river across the map with a numper of random points to intersect
    def makeRiver(self, matrix, midpoints):
        #first generate our list of points, including the start and end
        points = []
        gapping = self.size // (midpoints + 1)
        points.append((0, random.randint(0, self.size - 1)))
        for i in range(midpoints):
            point = [0,0]
            point[0] = int((i + 1) * gapping)
            bottom = points[i][1] - gapping
            if bottom < gapping // 2:
                bottom = gapping // 2
            top = points[i][1] + gapping
            if top > self.size - gapping //2:
                top = self.size - gapping //2
            point[1] = random.randint(bottom, top)
            points.append(point)
        bottom = points[i][1] - gapping
        if bottom < 0:
            bottom = 0
        top = points[i][1] + gapping
        if top > self.size - 1:
            top = self.size - 1
        points.append((self.size - 1, random.randint(bottom, top)))
        #now traverse from point to point:
        self.draw4connectedLine(matrix, points, 'r')

    #draws a four-connectd line through a list of points
    def draw4connectedLine(self, matrix, points, char):
        for i in range(len(points) - 1):
            x = points[i][0]
            y = points[i][1]
            steps = 0
            nextx = points[i + 1][0]
            nexty = points[i + 1][1]
            xdist = abs(nextx - x)
            ydist = abs(nexty - y)
            error = 0
            if y > nexty:
                ystep = -1
            else:
                ystep = 1
            for i in range(xdist + ydist + 1):
                matrix[x][y] = char
                error1 = error + ydist
                error2 = error - xdist
                if abs(error1) < abs(error2):
                    x += 1
                    error = error1
                else:
                    y += ystep
                    error = error2

    #generates a random walk of a tile on the map
    def randomPath(self, matrix, tile):
        gary = True
        eecks = random.randint(0,self.size - 1)
        wye = 0
        counter = 0
        while gary:
            matrix[eecks][wye] = tile
            dire = random.choice(((1,0),(0,1),(1,0),(1,0),(0,1),(0,1)))
            eecks += dire[0]
            wye += dire[1]
            if wye < 0 or wye > self.size - 1:
                if counter < 20:
                    wye = 0
                else:
                    gary = False
            if eecks < 0 or eecks > self.size - 1:
                if counter < 20:
                    eecks = 0
                else:
                    gary = False
            #add ability to seek edge on reaching step cap
            if counter > 300:
                gary = False
            counter += 1

    #counts the number of each entry and prints them
    def countEntries(self, matrix):
        keys = {}
        for key in ('g','b','g','r','p','t'):
            keys[key] = 0
        for x in matrix:
            for y in x:
                keys[y] += 1

    def placeExit(self, matrix):
        self.exitCoords = (random.randint(self.size / 2, self.size - 1), random.randint(self.size / 2, self.size - 1))
        matrix[self.exitCoords[0]][self.exitCoords[1]] = 'x'

    def generate_map(self):
        matero = []
        while matero == [] or (not self.map_is_valid(matero)):
            print(matero)
            print('start loop')
            matero = self.genBasicMatrix()
            self.makeRiver(matero, 8)
            self.randomPath(matero, 'p')
            self.countEntries(matero)
            self.placeExit(matero)
            print('end loop')
        return matero

    # only works when completedMatrix is square
    def get_surronding_tiles(self, x, y, completedMatrix):
        size = len(completedMatrix)
        tiles = []
        if x > 0 and completedMatrix[x-1][y] == False:
            completedMatrix[x-1][y] = True
            tiles.append((x-1, y))
        if x < size-1 and completedMatrix[x+1][y] == False:
            completedMatrix[x+1][y] = True
            tiles.append((x+1, y))
        if y > 0 and completedMatrix[x][y-1] == False:
            completedMatrix[x][y-1] = True
            tiles.append((x, y-1))
        if y < size-1 and completedMatrix[x][y+1] == False:
            completedMatrix[x][y+1] = True
            tiles.append((x, y+1))
        return tiles

    def map_is_valid(self, matrix):
        impassableTiles = ('r','b','t')
        if matrix[0][0] in impassableTiles:
            return False
        completed = [[False]*self.size for _ in range(self.size)]
        completed[0][0] = True
        frontier = []
        print('hi')
        for i in range(len(matrix)):
            frontier += self.get_surronding_tiles(0, 0, completed)
        while frontier != []:
            currCoords = frontier.pop()
            if matrix[currCoords[0]][currCoords[1]] == 'x':
                return True
            frontier += self.get_surronding_tiles(currCoords[0], currCoords[1], completed)
        return False