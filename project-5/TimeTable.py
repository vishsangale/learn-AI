import argparse

from enum import Enum


class Objectives(Enum):
    NUMBER_OF_TIME_SLOTS = 0
    TOTAL_STUDENT_COST = 1


class TimeTable:
    def __init__(self, course_file, student_file, solution_file, objective):
        self.room_capacity, self.maximum_time_slots, self.courses = self.read_course_file(course_file)
        self.students = self.read_student_file(student_file)
        self.solution_file = solution_file
        if Objectives.NUMBER_OF_TIME_SLOTS == objective:
            self.objective = Objectives.NUMBER_OF_TIME_SLOTS
        elif Objectives.TOTAL_STUDENT_COST == objective:
            self.objective = Objectives.TOTAL_STUDENT_COST

    @staticmethod
    def read_course_file(filename):
        with open(filename, "r") as f:
            roomCapacity, maximum_time_slots = f.readline().split()
            courses = {line[0]: line[1] for line in f}
        return int(roomCapacity), int(maximum_time_slots), courses

    @staticmethod
    def read_student_file(filename):
        with open(filename, "r") as f:
            students = {count + 1: line for count, line in enumerate((line.strip().split() for line in f))}
        return students


def main():
    args = parse_arguments()
    time_table = TimeTable(args.course_file, args.student_file, args.solution_file, args.objective)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("course_file", help="Course file")
    parser.add_argument("student_file", help="Student file")
    parser.add_argument("solution_file", help="Solution file")
    parser.add_argument("objective", type=int, choices=[0, 1], help="Objective function 0 for reducing number of "
                                                                    "time slots and 1 for reducing total student cost")
    return parser.parse_args()


if __name__ == "__main__":
    main()
