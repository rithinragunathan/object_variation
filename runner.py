import multiprocessing as mp
from main import main
import obj_det

def run_obj_det():
    obj_det.main()  # or whatever entry function you have inside obj_det

if __name__ == "__main__":
    process1 = mp.Process(target=main)
    process2 = mp.Process(target=run_obj_det)

    process1.start()
    process2.start()

    process1.join()
    process2.join()
