# Tabu search algorithm for solving exam time-tabling problem
import cProfile
import time
import sys
import random
import math
from collections import deque
import copy

MAX_TIME_SLOTS_PER_DAY = 5

NUMBER_OF_TIME_SLOTS = 0

TOTAL_STUDENT_COST = 1


class TabuSearch:
    def __init__(self, course_file, student_file, output_file, objective):
        self.objective = objective
        self.roomCapacity = 0
        self.maxTimeSlots = 0
        self.courses = {}
        self.students = {}
        self.read_course_file(course_file)
        self.read_student_file(student_file)
        self.outputFile = output_file
        self.solution = []
        self.slots = []

    def read_course_file(self, course_file):
        cf = open(course_file, "r")
        first_line = cf.readline().split()
        self.roomCapacity = int(first_line[0])
        self.maxTimeSlots = int(first_line[1])
        while True:
            line = cf.readline().split()
            if not line:
                break
            self.courses[line[0]] = int(line[1])

    def read_student_file(self, student_file):
        sf = open(student_file, "r")
        # Student number starts from 1 not from 0.
        count = 1
        while True:
            line = sf.readline().split()
            if not line:
                break
            self.students[count] = line
            count += 1

    def write_output_file(self):
        output = self.generate_solution(self.slots)
        f = open(self.outputFile, "w")
        data = str(len(self.slots)) + '\t' + str(self.calculate_objective_function_cost(self.slots)) + '\n'
        f.write(data)
        for out in output:
            data = str(out[0]) + '\t' + str(out[1]) + '\t' + str(out[2]) + '\n'
            f.write(data)
        f.close()
        self.solution = output

    def generate_random_initial_solution(self):
        keys = self.courses.keys()
        while True:
            slots = []
            while len(keys) > 0:
                slot = []
                pick = random.randint(0, len(keys) - 1)
                slot.append(keys[pick])
                keys.remove(keys[pick])
                slot_sum = sum([self.courses[x] for x in slot])
                if self.roomCapacity - slot_sum > 0:
                    for k in keys:
                        if self.roomCapacity - slot_sum - self.courses[k] >= 0:
                            slot.append(k)
                            keys.remove(k)
                            slot_sum += self.courses[k]
                slots.append(slot)
            if len(slots) <= self.maxTimeSlots:
                self.slots = slots
                return slots

    def generate_neighbor(self, slots, tabu_list):
        count = 0
        while True and count < 100:
            temp_slots = copy.deepcopy(slots)
            length_of_slots = len(slots)
            slot1 = random.randint(0, length_of_slots - 1)
            slot2 = random.randint(0, length_of_slots - 1)
            while slot2 == slot1:
                slot2 = random.randint(0, length_of_slots - 1)
            slot1_value = random.randint(0, len(temp_slots[slot1]) - 1)
            slot2_value = random.randint(0, len(temp_slots[slot2]) - 1)
            temp_slots[slot1][slot1_value], temp_slots[slot2][slot2_value] = temp_slots[slot2][slot2_value], \
                                                                             temp_slots[slot1][slot1_value]
            if temp_slots not in tabu_list and self.is_given_slot_feasible(temp_slots):
                return temp_slots
            count += 1
        if count == 100:
            return self.generate_random_initial_solution()

    def is_given_slot_feasible(self, slots):
        for slot in slots:
            for student in self.students:
                if all(x in self.students[student] for x in slot):
                    return False
        return True

    def calculate_objective_function_cost(self, slots):
        total_cost = 0
        solution = self.generate_solution(slots)
        solution_map = {s[0]: s for s in solution}
        for student in self.students:
            consecutive_penalty = 0
            overnight_penalty = 0
            student_course_mapping = {}
            for course in self.students[student]:
                date = solution_map[course][1]
                if date not in student_course_mapping:
                    student_course_mapping[date] = []
                student_course_mapping[date].append(solution_map[course])
            for course in student_course_mapping:
                if len(student_course_mapping[course]) != 1:
                    consecutive_penalty += sum(
                        [math.pow(2, -abs(x[2] - y[2])) for x in student_course_mapping[course] for y in
                         student_course_mapping[course]
                         if x[0] != y[0] and x[1] == y[1]])
            for course1 in student_course_mapping:
                for course2 in student_course_mapping:
                    if course1 == course2:
                        continue
                    overnight_penalty += sum(
                        [math.pow(2, -abs(x[1] - y[1])) for x in student_course_mapping[course1] for y in
                         student_course_mapping[course2]
                         if x[0] != y[0] and x[1] != y[1]])
            total_cost += consecutive_penalty * 10 + overnight_penalty
        return total_cost

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

    def search_algorithm(self, max_iterations, max_candidates, max_tabu_list_size):
        initial_solution = self.generate_random_initial_solution()
        best = initial_solution
        best_cost = self.calculate_objective_function_cost(best)
        tabu_list = deque()
        costs = []
        slots = best
        while max_iterations > 0:
            candidates = [self.generate_neighbor(slots, tabu_list) for _ in range(max_candidates)]
            best_candidate = min(candidates, key=self.calculate_objective_function_cost)
            best_candidate_cost = self.calculate_objective_function_cost(best_candidate)
            print best_candidate_cost
            if best_cost > best_candidate_cost:
                best = best_candidate
                best_cost = best_candidate_cost
                if len(tabu_list) >= max_tabu_list_size:
                    tabu_list.popleft()
                tabu_list.append(best_candidate)
            max_iterations -= 1
            costs.append(best_candidate_cost)
            if len(costs) >= 3 and costs[-1] == costs[-2] == costs[-3]:
                slots = self.generate_random_initial_solution()
        print costs
        self.slots = best
        return best_cost


def main():
    # random.seed(0)
    t0 = time.time()

    tabu_instance = TabuSearch(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

    cost = tabu_instance.search_algorithm(100, 10, 10)

    tabu_instance.write_output_file()

    print tabu_instance.solution
    print cost
    print time.time() - t0


if __name__ == "__main__":
    cProfile.run('main()')
