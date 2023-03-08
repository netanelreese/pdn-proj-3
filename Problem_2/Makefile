in=in.fna # starter input file name, can set like "make run_starter in=other.fna"

all: make_critical make_atomic make_locks make_schedule

# duplicate this for other files
make_critical: compute_average_TF_Exp1_critical.c
	gcc -fopenmp -g -Wall -o compute_average_TF_Exp1_critical compute_average_TF_Exp1_critical.c -lm -std=c99

	
make_atomic: compute_average_TF_Exp1_atomic.c
	gcc -fopenmp -g -Wall -o compute_average_TF_Exp1_atomic compute_average_TF_Exp1_atomic.c -lm -std=c99

make_locks: compute_average_TF_Exp1_locks.c
	gcc -fopenmp -g -Wall -o compute_average_TF_Exp1_locks compute_average_TF_Exp1_locks.c -lm -std=c99

make_schedule: compute_average_TF_Exp2_schedule.c
	gcc -fopenmp -g -Wall -o compute_average_TF_Exp2_schedule compute_average_TF_Exp2_schedule.c -lm -std=c99

clean:
	$(RM) compute_average_TF_Exp1_starter


# Below are commands to help you run your program easily.
# You will need to create more entries for your different files, such as for critical and locks.
run: run_starter

# duplicate this for other files
run_starter:
	./compute_average_TF_Exp1_starter $(in) OUTPUT_starter_1th.csv TIME_starter_1th.csv 1
	./compute_average_TF_Exp1_starter $(in) OUTPUT_starter_2th.csv TIME_starter_2th.csv 2
	./compute_average_TF_Exp1_starter $(in) OUTPUT_starter_4th.csv TIME_starter_4th.csv 4
	./compute_average_TF_Exp1_starter $(in) OUTPUT_starter_8th.csv TIME_starter_8th.csv 8
