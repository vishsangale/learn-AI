# Tabu search algorithm for solving exam time-tabling problem
import time
import sys
import random
import math
from collections import deque
import copy


MAX_TIME_SLOTS_PER_DAY = 5

NUMBER_OF_TIME_SLOTS = 0

TOTAL_STUDENT_COST = 1


# Class which represents the search problem
class TabuSearch:
    def __init__(self, courseFile, studentFile, outputFile, objective):
        self.objective = objective  # argument for objective functions
        self.roomCapacity = 0
        self.maxTimeSlots = 0
        self.courses = {}
        self.students = {}
        self.read_course_file(courseFile)
        self.readStudentFile(studentFile)
        self.outputFile = outputFile
        self.solution = []
        self.slots = []

    # Read course file
    def read_course_file(self, courseFile):
        cf = open(courseFile, "r")
        firstLine = cf.readline().split()
        self.roomCapacity = int(firstLine[0])
        self.maxTimeSlots = int(firstLine[1])
        while True:
            line = cf.readline().split()
            if not line:
                break
            self.courses[line[0]] = int(line[1])

    # Read student file
    def readStudentFile(self, studentFile):
        sf = open(studentFile, "r")
        # Student number starts from 1 not from 0.
        count = 1
        while True:
            line = sf.readline().split()
            if not line:
                break
            self.students[count] = line
            count += 1

    # Write solution to the output file.
    def writeOutputFile(self):
        output = self.generate_solution(self.slots)
        f = open(self.outputFile, "w")
        data = str(len(self.slots)) + '\t' + str(self.calculate_objective_function_cost(self.slots)) + '\n'
        f.write(data)
        for out in output:
            data = str(out[0]) + '\t' + str(out[1]) + '\t' + str(out[2]) + '\n'
            f.write(data)
        f.close()
        self.solution = output

    # Generate initial solution randomly.
    def generateRandomInitialSolution(self):
        keys = self.courses.keys()
        while True:
            slots = []
            while len(keys) > 0:
                slot = []
                pick = random.randint(0, len(keys) - 1)
                slot.append(keys[pick])
                keys.remove(keys[pick])
                slotSum = sum([self.courses[x] for x in slot])
                if self.roomCapacity - slotSum > 0:
                    for k in keys:
                        if self.roomCapacity - slotSum - self.courses[k] >= 0:
                            slot.append(k)
                            keys.remove(k)
                            slotSum += self.courses[k]
                slots.append(slot)
            if len(slots) <= self.maxTimeSlots:
                self.slots = slots
                return slots

    # Generate neighbor just by swapping time slots
    def generate_neighbor(self, slots, tabuList):
        while True:
            tempSlots = copy.deepcopy(slots)
            lengthOfSlots = len(slots)
            slot1 = random.randint(0, lengthOfSlots - 1)
            while True:
                slot2 = random.randint(0, lengthOfSlots - 1)
                if slot2 != slot1:
                    break
            slot1Value = random.randint(0, len(tempSlots[slot1]) - 1)
            slot2Value = random.randint(0, len(tempSlots[slot2]) - 1)
            tempSlots[slot1][slot1Value], tempSlots[slot2][slot2Value] = tempSlots[slot2][slot2Value], tempSlots[slot1][
                slot1Value]
            if self.is_given_slot_feasible(tempSlots) and tempSlots not in tabuList:
                return tempSlots

    # Check if assigned slots are feasible
    def is_given_slot_feasible(self, slots):
        for slot in slots:
            for student in self.students:
                if len(slot) == 1:
                    continue
                if all(x in self.students[student] for x in slot):
                    return False
        return True

    # Calculate the objective function cost.
    def calculate_objective_function_cost(self, slots):
        totalCost = 0
        solution = self.generate_solution(slots)
        solutionMap = {}
        for s in solution:
            solutionMap[s[0]] = s
        for student in self.students:
            consecutivePenalty = 0
            overnightPenalty = 0
            studentCourseMapping = {}
            for course in self.students[student]:
                date = solutionMap[course][1]
                if date in studentCourseMapping:
                    studentCourseMapping[date].append(solutionMap[course])
                else:
                    studentCourseMapping[date] = []
                    studentCourseMapping[date].append(solutionMap[course])
            for course in studentCourseMapping:
                if len(studentCourseMapping[course]) != 1:
                    consecutivePenalty += sum(
                        [math.pow(2, -abs(x[2] - y[2])) for x in studentCourseMapping[course] for y in
                         studentCourseMapping[course]
                         if x[0] != y[0] and x[1] == y[1]])
            for course1 in studentCourseMapping:
                for course2 in studentCourseMapping:
                    if course1 == course2:
                        continue
                    overnightPenalty += sum(
                        [math.pow(2, -abs(x[1] - y[1])) for x in studentCourseMapping[course1] for y in
                         studentCourseMapping[course2]
                         if x[0] != y[0] and x[1] != y[1]])
            totalCost += consecutivePenalty * 10 + overnightPenalty
        return totalCost

    # Generate solution i.e assign each course with date and time slot.
    @staticmethod
    def generate_solution(courses):
        output = []
        # Slot count starts from 1.
        slot = 1
        for courseGroup in courses:
            for course in courseGroup:
                if slot < MAX_TIME_SLOTS_PER_DAY:
                    output.append([course, 1, slot])
                else:
                    output.append([course, slot / MAX_TIME_SLOTS_PER_DAY + 1, slot - MAX_TIME_SLOTS_PER_DAY])
            slot += 1
        return output

    # Tabu search algorithm.
    def search_algorithm(self, max_iterations, max_candidates, maxTabuListSize):
        initialSolution = self.generateRandomInitialSolution()
        mov = len(initialSolution[0]) / 2
        if self.objective == '1':
            for i in range(len(initialSolution)):
                if len(initialSolution[i]) <= mov:
                    continue
                for j in range(mov):
                    tail = initialSolution[i].pop()
                    initialSolution.append([tail])
        elif self.objective == '0':
            pass
        best = initialSolution
        tabuList = deque()
        while max_iterations > 0:
            candidates = []
            for i in range(max_candidates):
                candidates.append(self.generate_neighbor(best, tabuList))
            bestCandidate = min(candidates, key=self.calculate_objective_function_cost)
            if self.calculate_objective_function_cost(bestCandidate) < self.calculate_objective_function_cost(best):
                best = bestCandidate
                if len(tabuList) < maxTabuListSize:
                    tabuList.append(bestCandidate)
                else:
                    tabuList.popleft()
                    tabuList.append(bestCandidate)
            max_iterations -= 1
        self.slots = best
        return best


if __name__ == "__main__":
    t0 = time.time()
    # Create the class object and pass the arguments.
    tabuInstance = TabuSearch(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    # Run the search algorithm on the given problem instance.
    solution = tabuInstance.search_algorithm(1000, len(tabuInstance.students), len(tabuInstance.courses))
    # Write the solution to the file
    tabuInstance.writeOutputFile()
    # Print solution
    print tabuInstance.solution
    print tabuInstance.calculate_objective_function_cost(solution)
    print time.time() - t0
