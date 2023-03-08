import numpy as np
import os
import pandas as pd
import sys

# Tell the script where to find the base autograder
sys.path.append("..")
sys.path.append(os.path.join("..", ".."))
from autograder_base import Base_Autograder

# Colors
W = '\033[0m'  # white (normal)
R = '\033[31m'  # red
O = '\033[33m'  # orange
Y = '\033[93m'  # yellow
G = '\033[32m'  # green

class Autograder_3_4(Base_Autograder):

    def __init__(self):
        super().__init__()

        # Student information
        self.student_name = "student"
        self.is_grad = True

        # Directory information
        self.student_files =    "Problem_4"
        self.test_files =       os.path.join("..", "test_data", "Problem_4")
        self.this_dir =         "."

        # Test information
        self.threads = [1, 4, 16]
        self.test_names = [
            # 1M
            [
                ["p4-1M"]
            ],

            # 4M
            [
                ["p4-4M"]
            ],

            # 16M
            [
                ["p4-16M"]
            ]
        ]


    def autograde(self):
        this_dir = os.path.abspath(self.this_dir)
        test_dir = os.path.abspath(self.test_files)

        # Print the test dir and project dir
        if self.DEBUG:
            print(f"{G} --> Test dir: {test_dir}{W}")
            print(f"{G} --> Project dir: {this_dir}{W}")

        # get num cols for threads
        columns = []
        for file in self.test_names:
            for program in file:
                for i in range(len(self.threads)):
                    columns.append(f"{program[0]}-T{self.threads[i]}")

        # student grades
        grade = pd.DataFrame(
            np.nan,
            index=[self.student_name],
            columns=columns
        )

        # student timing
        time = pd.DataFrame(
            np.nan,
            index=[self.student_name],
            columns=columns
        )

        # Input RNA files
        t_centroids = os.path.join(test_dir, "centroids.csv")
        t_points    = [
            os.path.join(test_dir, "points_1M.csv"),
            os.path.join(test_dir, "points_4M.csv"),
            os.path.join(test_dir, "points_16M.csv")
        ]

        # Expected output
        t_out = [
            os.path.join(test_dir, "p4_output_1M.csv"),
            os.path.join(test_dir, "p4_output_4M.csv"),
            os.path.join(test_dir, "p4_output_16M.csv")
        ]

        # Actual program output from the student
        t_dir = os.path.join(this_dir, self.student_files)
        t_p4_prefix = ["kmeans_clustering"]
        t_p4_get = [
            [[]],  # 1M
            [[]],  # 4M
            [[]]   # 16M
        ]
        t_p4_tim = [
            [[]],  # 1M
            [[]],  # 4M
            [[]]   # 16M
        ]
        points = ["1M", "4M", "16M"]
        for out in range(len(t_out)):
            for pre in range(len(t_p4_prefix)):
                for t in self.threads:
                    t_p4_get[out][pre].append(
                        os.path.join(t_dir, f"res_{t_p4_prefix[pre]}_{points[out]}_{t}th.csv")
                    )
                    t_p4_tim[out][pre].append(
                        os.path.join(t_dir, f"tim_{t_p4_prefix[pre]}_{points[out]}_{t}th.csv")
                    )

        #   generate the commands to run the tests here
        c_p4 = [
            [[]],  # 1M
            [[]],  # 4M
            [[]]   # 16M
        ]

        # TA) TODO: alternate program names, if needed
        p4_names = [
            "kmeans_clustering"
        ]

        input_values = [
            [1000000,  16],
            [4000000,  16],
            [16000000, 16]
        ]

        # generate the problems' command-variables
        for file in range(len(t_points)):         # For point input
            for program in range(len(p4_names)):  # For program
                for t in range(len(self.threads)):     # For num thread counts
                    c_p4[file][program].append([
                        p4_names[program],           # program type, like locks or sharing,
                        input_values[file][0],       # num points
                        t_points[file],              # points file
                        input_values[file][1],       # num centroids
                        t_centroids,                 # centroids file
                        t_p4_get[file][program][t],  # resulting output file
                        t_p4_tim[file][program][t],  # resulting time file
                        self.threads[t]                   # num threads
                    ])


        #  we have everything we need to test a problem now
        #   grade each individual problem here!
        # TA) TODO: specify each problem's test parameters
        # Problem 3
        test_params = [
            [[]],  # 1M
            [[]],  # 4M
            [[]]   # 16M
        ]
        for file in range(len(t_points)):         # For point input
            for program in range(len(p4_names)):  # For program names
                for t in range(len(self.threads)):     # For num thread counts
                    test_params[file][program].append(
                        [os.path.join(this_dir, "Problem_4"), t_out[file], t_p4_get[file][program][t], c_p4[file][program][t], False]
                    )

        # testing results
        test_results = [None] * len(columns)
        time_results = [None] * len(columns)

        # test every problem in a loop
        grade_index = 0
        for file in range(len(self.test_names)):
            for program in range(len(self.test_names[file])):
                for thread in range(len(self.threads)):
                    params = test_params[file][program][thread]
                    result = self.grade_problem(
                        params[0],  # Problem dir
                        [params[1]],  # Expected outputs of test i
                        [params[2]],  # Output file names
                        [params[3]],  # Command for getting test i results
                        params[4]   # Whether to let the differences have an error range
                    )

                    # set results
                    test_results[grade_index] = result[0]
                    time_results[grade_index] = result[1]

                    # add each result to the dataframes
                    grade.loc[self.student_name, columns[grade_index]] = test_results[grade_index][0]
                    time.loc[self.student_name,  columns[grade_index]] = time_results[grade_index][0]
                    grade_index = grade_index + 1

        return [grade, time]



def main():
    print("{G}Autograding for Project 3 Problem 4:\n{W}")
    
    p4 = Autograder_3_4()
    res = p4.autograde()
    total = str(len(res[0].columns))
    correct = str(int(res[0].sum(axis=1)[0]))

    print("{Y}\n Final grades:{W}")
    res[0].to_csv("P3_4_grades.csv")
    print(res[0])

    print("{Y}\n Final timings:{W}")
    res[1].to_csv("P3_4_times.csv")
    print(res[1])

    print(f"{R}\n --> {correct}/{total} problems correct\n{W}")


if __name__ == "__main__":
    main()