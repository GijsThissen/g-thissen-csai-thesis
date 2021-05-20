import os
from tqdm import tqdm

def fixing():
    """
    Fixes files by removing the extra \n that was created during the train_test_dev.py splitting of the data. OpenNMT
    does not handle empty lines well and will assign "translations".
    """
    # Get current working directory
    working_directory = str(os.getcwd())

    # Calculate the total amount of files in the working directory
    dataset = os.listdir(str(working_directory))
    total = len(dataset)

    print("\nDeleting white spaces in files\n")

    # Source (regarding the lines of code related to the tqdm-libary):
    # DDGG. (2018, Feb 22) tqdm not showing bar. Stackoverflow.com.
    # https://stackoverflow.com/questions/48935907/tqdm-not-showing-bar

    with tqdm(total = total) as pbar:
        for element in dataset:
            # Create new name
            new_name = "f-" + element
            with open(str(element), "r", encoding="utf-8") as f:  # Read from this file
                with open(str(new_name), "w+", encoding="utf-8") as fixed:  # Write in this file
                    # Removing all the extra white spaces
                    while True:
                        line = f.readline()
                        if line == "":
                            break
                        if line == "nan\n":
                            continue
                        if not line.isspace() and line != "nan":
                            fixed.write(line)
            pbar.update(1) # Update pbar by 1

if __name__ == '__main__':
    fixing()
