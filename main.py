from preprocess import preprocess
from fixing import fixing
import os

if __name__ == "__main__":
    # Reads out the dataset CSV files and creates the files needed for the experiments:
    # Normal (Baseline), Vocal (Vocal), Time (Temporal), Combined (Combined), & Sentences (German language target file)
    raw_files = create_file("datasets/")
    os.mkdir("datafiles/")
    raw_files.data_prepare("datafiles/", normal = True, vocal=True, time=True, combined=True, sentences=True)