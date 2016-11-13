# This file contains generic code exam time table scheduling.
# Checking constraints.
# Reading input files
import copy
import sys
import random
import math
import operator
import datetime

# Global variables-----------
# courses = dict()
students = dict()
nonConflictingCourses = []
maximumTimeSlots = 0
maximumSlotsPerDay = 5
allowedSlots = []


# Each course has one exam, which is conducted only once,
# and all students enrolled for the course must take the
# exam in the same time slot.
def check_hard_constraint1(time_table):
    return True


# The first day in the timetable is 1 and there are
# #numberOfTimeSlots available every day.
def check_hard_constraint2(time_table):
    return True


# There are no holidays! Also, there must be no unused
# timeslots between the first and the last day of exams
# in the timetable.
def check_hard_constraint3(time_table):
    sortedTimeTable = sorted(time_table.items(), key=operator.itemgetter(1))
    lastDay = sortedTimeTable[-1][1][0]
    lastSlot = sortedTimeTable[-1][1][1]
    allowed_slots = list()
    if lastDay is 1:
        allowed_slots += [[lastDay, j + 1] * 1 for j in range(lastSlot)]
    else:
        for i in range(1, lastDay + 1):
            allowed_slots += ([[i, j + 1] * 1 for j in range(maximumSlotsPerDay)])
    for slot in allowed_slots:
        if slot not in time_table.values():
            return False
    return True


# Exams with one or more common students cannot be assigned
# to the same time slot, i.e. a student cannot take more
# than one exam in the same time slot.
def check_hard_constraint4(time_table):
    for studentCourses in students.values():
        if len(studentCourses) > 1:
            for course1 in studentCourses:
                for course2 in studentCourses:
                    if course1 is not course2:
                        if time_table[course1] is time_table[course2]:
                            # print "Hard Constraint 4 violated"
                            return False
    return True


# Multiple exams can be assigned to a single time slot.
def check_hard_constraint5(time_table):
    # print "Hard Constraint 5 violated"
    return True


# Total number of students taking exams in a given time slot
# should not exceed the room capacity specified in the problem.
def check_hard_constraint6(time_table, room_capacity):
    # print "Hard Constraint 6 violated"
    for slot in allowedSlots:
        roomCount = 0
        for course in time_table.keys():
            if time_table[course] == slot:
                roomCount += int(courses[course])
                if roomCount > room_capacity:
                    return False
    return True


# The total number of time slots used by the timetable
# should not exceed the maximum number of timeslots
# specified in the problem.
def check_hard_constraint7(time_table):
    if maximumTimeSlots < calculate_total_number_of_time_slots(time_table):
        # print "Hard Constraint 7 violated"
        return False
    else:
        return True


# Generate solution  it is feasible.
def generate_feasible_solution(input_solution, room_capacity):
    solution = generate_solution(input_solution)
    while not is_solution_feasible(solution, room_capacity):
        solution = generate_solution(solution)
    return solution


# Check solution is feasible apply all constraints.
def is_solution_feasible(time_table, room_capacity):
    if not check_hard_constraint1(time_table):
        return False
    if not check_hard_constraint2(time_table):
        return False
    if not check_hard_constraint3(time_table):
        return False
    if not check_hard_constraint4(time_table):
        return False
    if not check_hard_constraint5(time_table):
        return False
    if not check_hard_constraint6(time_table, room_capacity):
        return False
    if not check_hard_constraint7(time_table):
        return False
    return True


# Generate solution which may not be feasible.
# May be just swapping the two courses.
def generate_solution(time_table):
    # print time_table
    """"for course in time_table.keys():
        time_table[course] = allowedSlots[random.randrange(0, len(allowedSlots))]
    return time_table"""
    """slots = allowedSlots
    keys = time_table.keys()
    random.shuffle(keys)
    assigned = []
    for course in keys:
        if not slots:
            return time_table
        slot = slots[0]
        del slots[0]
        time_table[course] = slot
        assigned.append(course)
        for course1 in nonConflictingCourses[course]:
            if course1 not in assigned:
                time_table[course1] = slot
                assigned.append(course1)
                if course1 in keys:
                    del keys[keys.index(course1)]
        del keys[keys.index(course)]
    return time_table"""
    tempTimeTable = copy.deepcopy(time_table)
    slots = copy.deepcopy(allowedSlots)
    keys = time_table.keys()
    random.shuffle(keys)
    assigned = []
    # print nonConflictingCourses
    # print sorted(nonConflictingCourses.items())
    for course in keys:
        problem = False
        if course not in assigned:
            if not slots:
                slots = copy.deepcopy(allowedSlots)
            course1 = random.choice(nonConflictingCourses[course])
            i = 0
            while course1 in assigned:
                course1 = random.choice(nonConflictingCourses[course])
                i += 1
                if i == len(keys) / 2:
                    problem = True
                    break
            if not problem:
                tempTimeTable[course] = slots[0]
                tempTimeTable[course1] = slots[0]
                del slots[0]
                assigned.append(course)
                assigned.append(course1)
            else:
                tempTimeTable[course] = slots[0]
                del slots[0]
                assigned.append(course)
    return tempTimeTable


# Soft Constraint
# Objective Function 1
# Total number of timeslots used by the timetable should be minimized.
def calculate_total_number_of_time_slots(time_table):
    assignedSlots = list()
    for course in time_table.keys():
        if not time_table[course] in assignedSlots:
            assignedSlots.append(time_table[course])
    return len(assignedSlots)


# Calculate Consecutive Assignment Penalty.
# Consecutive assignment penalty is calculated only
# for exams occurring on the same day.
def calculate_consecutive_assignment_penalty(time_table):
    cost = 0
    if not time_table:
        return cost
    for student in students.keys():
        if len(students[student]) > 1:
            for course1 in students[student]:
                for course2 in students[student]:
                    if course1 != course2 and time_table[course1][0] == time_table[course2][0]:
                        cost += math.pow(2, -abs(time_table[course1][1] - time_table[course2][1]))
    return cost


# Overnight Assignment Penalty is calculated only
# for exams occurring on different days.
def calculate_overnight_assignment_penalty(time_table):
    cost = 0
    if not time_table:
        return cost
    for student in students.keys():
        if len(students[student]) > 1:
            for course1 in students[student]:
                for course2 in students[student]:
                    if course1 != course2 and time_table[course1][0] != time_table[course2][0]:
                        cost += math.pow(2, -abs(time_table[course1][0] - time_table[course2][0]))
    return cost


# Objective Function 2
# Total student cost should be minimized.
def calculate_total_student_cost(time_table):
    consecutiveAssignmentPenalty = calculate_consecutive_assignment_penalty(time_table)
    overnightAssignmentPenalty = calculate_overnight_assignment_penalty(time_table)
    return 10 * consecutiveAssignmentPenalty + overnightAssignmentPenalty


# Read course file.
# In the course file, the first row contains the room capacity
# and the maximum number of timeslots, respectively. The second
# row onward, every row has two columns, namely course code and
# total enrollment for that course. Enrollment represents the
# total number of students enrolled for that course.
def read_course_file(filename):
    # open course file and read and store in list of list by spliting each line.
    lines = [line.strip().split() for line in open(filename)]
    # extract room capacity and max number of time slots from first line
    roomCapacity, maximum_time_slots = lines[0]
    # delete first line
    del lines[0]
    # create dictionary from list of lists
    return int(roomCapacity), int(maximum_time_slots), {line[0]: line[1] for line in lines}


# Read student file.
# In the student file, every row represents courses that a student has enrolled for.
def read_student_file(filename):
    # Open student file and read and store student enrollment.
    lines = [line.strip().split() for line in open(filename)]
    # Create dict from list
    return {count + 1: line for count, line in enumerate(lines)}


# Write solution file.
# Write generated output to *.sol
# In the output file, the first row has two columns, representing the two
# objective functions: total number of timeslots and the total student cost.
# The second row and the rows that follow contain the course number, date and
# time slot assigned to the course exam, respectively.
def write_solution_file(filename, time_table, number_of_time_slots_used, total_student_cost):
    sf = open(filename, "w+")
    sf.write(str(number_of_time_slots_used) + '\t' + str(total_student_cost) + '\n')
    for course in time_table.keys():
        sf.write(course + '\t' + str(time_table[course][0]) + '\t' + str(time_table[course][1]) + '\n')


# Generate initial solution
# Assign random values to day and timeslot to each course.
def generate_initial_solution():
    timeTable = {course: allowedSlots[random.randrange(0, len(allowedSlots))] for course in courses.keys()}
    return timeTable


def generate_allowed_slots():
    A = []
    for i in range(0, maximumTimeSlots / maximumSlotsPerDay):
        for j in range(0, maximumSlotsPerDay):
            A.append([i + 1, j + 1])
    return A


def get_non_conflicting_courses():
    non_conflicting_courses = {course: courses.keys() for course in courses.keys()}
    # print nonConflictingCourses
    for course in non_conflicting_courses.keys():
        if course in non_conflicting_courses[course]:
            del non_conflicting_courses[course][non_conflicting_courses[course].index(course)]
        for student in students.keys():
            if len(students[student]) > 1:
                for course1 in students[student]:
                    for course2 in students[student]:
                        if course2 in non_conflicting_courses[course1]:
                            del non_conflicting_courses[course1][non_conflicting_courses[course1].index(course2)]
                            # print nonConflictingCourses
    return non_conflicting_courses


# ------------------------------Genetic Algorithm------------------------------------

def mate(parent1, parent2, room_capacity):
    # print parent1, parent2
    temp1 = copy.deepcopy(parent1)
    temp2 = copy.deepcopy(parent2)
    key1 = random.choice(parent1.keys())
    key2 = random.choice(parent1.keys())
    temp1[key1] = temp2[key1]
    temp1[key2] = temp2[key2]
    while not is_solution_feasible(temp1, room_capacity):
        key1 = random.choice(parent1.keys())
        key2 = random.choice(parent1.keys())
        temp1[key1] = temp2[key1]
        temp1[key2] = temp2[key2]
    return temp1


def mutate(child):
    # print child
    return child


def get_best_child(population, fitness_function):
    fitnesses = map(fitness_function, population)
    index = fitnesses.index(min(fitnesses))
    return population[index]


def create_initial_population(initial_state, population_size, room_capacity):
    # print initial_state
    population = []
    for i in range(population_size):
        thisSolution = generate_feasible_solution(initial_state, room_capacity)
        population.append(thisSolution)
    return population


def get_maximum_fit_parents(population, fitnesses):
    temp = copy.deepcopy(fitnesses)
    i1 = temp.index(min(temp))
    del temp[i1]
    i2 = temp.index(min(temp))
    # del population[i1]
    # del fitnesses[i1]
    return population[i1], population[i2]


def get_random_parents(population):
    i1 = random.randrange(0, len(population))
    i2 = random.randrange(0, len(population))
    return population[i1], population[i2]


def get_best_from_family(parent1, parent2, child, fitness_function):
    family = [parent1, parent2, child]
    familyFitness = map(fitness_function, family)
    i = familyFitness.index(min(familyFitness))
    # print familyFitness, i
    return family[i]


def genetic_algorithm(initial_state, fitness_function, room_capacity):
    numberOfGenerations = 100
    populationSize = 10
    probabilityOfMutation = 0.1
    population = create_initial_population(initial_state, populationSize, room_capacity)
    for _ in range(numberOfGenerations):
        newPopulation = []
        for generation in range(populationSize):
            fitnesses = map(fitness_function, population)
            # print fitnesses
            # parent1, parent2 = getMaximumFitParents(population, fitnesses)
            parent1, parent2 = get_random_parents(population)
            child = mate(parent1, parent2, room_capacity)
            if random.uniform(0, 1) < probabilityOfMutation:
                child = mutate(child)
            best = get_best_from_family(parent1, parent2, child, fitness_function)
            newPopulation.append(best)
        population = newPopulation
        bestSoFar = get_best_child(population, fitness_function)
        numberOfTimeSlotsUsed = calculate_total_number_of_time_slots(bestSoFar)
        totalStudentCost = calculate_total_student_cost(bestSoFar)
        write_solution_file(sys.argv[3], bestSoFar, numberOfTimeSlotsUsed, totalStudentCost)
        print totalStudentCost


# -----------------------Main function start-------------------
def main():
    t0 = datetime.datetime.now()
    print t0
    room_capacity, maximum_time_slots, courses = read_course_file(sys.argv[1])
    students = read_student_file(sys.argv[2])
    allowedSlots = generate_allowed_slots()
    nonConflictingCourses = get_non_conflicting_courses()
    timeTable = generate_initial_solution()
    if sys.argv[4] == '0':
        genetic_algorithm(timeTable, calculate_total_number_of_time_slots, room_capacity)
    elif sys.argv[4] == '1':
        genetic_algorithm(timeTable, calculate_total_student_cost, room_capacity)
    else:
        print 'Invalid argument!!!'
    print datetime.datetime.now() - t0


if __name__ == "__main__":
    main()
