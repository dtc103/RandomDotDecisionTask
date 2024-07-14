from RandomDotDecisionTask import RandomDotDecisionTask
import tools


WIDTH, HEIGHT = 1980, 1080
MOTION_STRENGTHS = [0.0, 0.032, 0.064, 0.128, 0.256, 0.512]
TRIALS = 40

def main():
    subject_name = input("Input the subject name: ")

    task = RandomDotDecisionTask(WIDTH, HEIGHT, MOTION_STRENGTHS)
    task.run(TRIALS)
    task.quit()

    if len(task.answers) > 0:
        data_header = ["Decision Time [s]", "Success", "Coherence", "Actual Direction"]
        tools.save_data(task.answers, header=data_header, subject_name=subject_name)


if "__main__" == __name__:
    main()