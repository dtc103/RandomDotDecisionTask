from RandomDotDecisionTask import RandomDotDecisionTask
import tools


WIDTH, HEIGHT = 800, 800
MOTION_STRENGTHS = [0.0, 0.32, 0.64, 0.128, 0.256, 0.512]

def main():
    subject_name = input("Input the subject name: ")

    task = RandomDotDecisionTask(WIDTH, HEIGHT, MOTION_STRENGTHS)
    task.run(5)
    task.quit()

    data_header = ["Decision Time [s]", "Success", "Coherence", "Actual Direction"]
    tools.save_data(task.answers, header=data_header, subject_name=subject_name)

    print(task.answers)



if "__main__" == __name__:
    main()