import os
from tqdm import tqdm


def whitespace_removal():
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

    with tqdm(total=total) as pbar:
        for filename in dataset:

            # Source for the code:
            # A. & Anda, H. E. (2016, Dec 7) Open a text file and remove any blank lines. Stackexchange.com.
            # https://codereview.stackexchange.com/questions/145126/open-a-text-file-and-remove-any-blank-lines

            # If the file cannot be found it will print that it does not exist
            if not os.path.isfile(filename):
                print("{} does not exist ".format(filename))
                return
            # Open the file and put all lines in a list
            with open(filename, encoding = "utf-8") as filehandle:
                lines = filehandle.readlines()

            # Open the file in write mode and strip all empty elements in the lines list
            with open(filename, 'w', encoding = "utf-8") as filehandle:
                lines = filter(lambda x: x.strip(), lines)
                filehandle.writelines(lines)


            pbar.update(1)  # Update pbar by 1
