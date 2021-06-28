import pandas as pd
from os import listdir
from tqdm import tqdm
import numpy as np


class create_file(object):
    def __init__(self, path="datasets/"):
        self.path = path
        self.inputs = listdir(str(path))
        self.dataframe = self.drop_empty()

    def clean_dataframe(self, dataset):
        """
        Load the dataset into a frame, delete the "Unnamed" column,
        and replace all instances of nothing with a numpy nan.
        Requires the numpy library.

        :param dataset: str, input name of the dataset.csv
        :return: dataframe, a cleaned dataframe with only used columns
        """
        dataframe = pd.read_csv(self.path + str(dataset), sep=",")  # Read into a frame
        dataframe = dataframe.loc[:, ~dataframe.columns.str.contains("^Unnamed")]  # Drop the "^Unnamed" column
        dataframe.replace("", np.nan, inplace=True)  # Replace the empty values with a nan

        return dataframe

    def merge(self):
        """
        The EAF-files consist of different persons, this functions merges those
        into one dataframe.

        :return: Dataframe. A merged dataframe consisting of all users.
        """
        combined = pd.DataFrame()
        for dataset in self.inputs:
            temp = self.clean_dataframe(dataset)

            # Normalize the column names into the translated versions.
            column_list = list(temp.columns)
            normalized_names = ["Time", "Right", "Mouth", "Translation", "Left"]
            # A dictionary is created with the corresponding column_list name and the normalized name
            translation_dict = {column_list[n]: normalized_names[n] for n in range(len(normalized_names))}
            temp = temp.rename(columns=translation_dict)

            # Combine the dataframes into one universal dataframe
            combined = combined.append(temp, ignore_index=True, sort=False)

        return combined

    def list_definer(self, input_list):
        """
        Finds the True instances in a list and stores their indexes.

        :param input_list: list, a list of True's and False's.
        :return: list, the list of indexes that were true in the input_list.
        """
        output_list = []
        # Looping over a enumerated input_list
        for number, element in enumerate(input_list):
            # If the element is True append the index else continue the loop
            if element:
                output_list.append(number)
            continue
        return output_list

    def drop_empty(self):
        """
        Dropping the empty rows from the dataset causing it to become more information packed.
        Downsides of this approach may be the loss of important information present in the whitespaces.

        :return: dataframe, a dataframe where there are no empty rows.
        """
        combined = self.merge()

        # Find the empty rows for each respective token (time excluded since it is always present).
        left_sign = set(self.list_definer(list(combined['Left'].isnull().values)))
        right_sign = set(self.list_definer(list(combined['Right'].isnull().values)))
        mouth_token = set(self.list_definer(list(combined['Mouth'].isnull().values)))

        # Find the intersection of these tokens.
        signs = left_sign.intersection(right_sign)
        empty_rows = signs.intersection(mouth_token)
        signs_missing = list(empty_rows)

        # Dropping the empty rows
        final_dataframe = combined.drop(signs_missing)

        return final_dataframe

    def func(self, name, *text, encoding="utf-8"):
        """
        Creates a file containing the text from the *text parameter.
        Standard encoding = UTF-8

        :param encoding: string, specifying the encoding
        :param name: string, name of the output file
        :param text: iterable, an iterable of text
        """
        with open(str(name), mode="wt", encoding=str(encoding)) as my_file:
            for lines in text:
                my_file.write('\n'.join(str(line) for line in lines))
                my_file.write('\n')

    def data_prepare(self, output_path, normal=False, time=False, vocal=False, combined=False, sentences=False,
                     standardisation=False):
        """
        Loops over the dataset and applies the respective parameters specified in the initializer.
        If combined == True it will only generate a combined file in the output_path.

        :param output_path: string, the output path where the files need to be deposited.
        :param normal: boolean, create a file with glosses.
        :param time: boolean, create a file with glosses|time.
        :param vocal: boolean, create a file with glosses|vocal.
        :param combined: boolean, create a file with glosses|vocal|time.
        :param sentences: boolean, create a file with english sentences.
        :param standardisation: boolean, standardising the words. Greatly increases runtime.
        """
        sentence = ""
        sentences_list = []
        normal_list = []
        times_list = []
        vocal_list = []
        combined_list = []

        # Looping over the (combined) dataframe
        print("\nCreating specified files.\n")

        # Source (regarding the lines of code related to the tqdm-libary):
        # DDGG. (2018, Feb 22) tqdm not showing bar. Stackoverflow.com.
        # https://stackoverflow.com/questions/48935907/tqdm-not-showing-bar

        # Calculate the total length of the dataframe and create the progress bar
        total = len(self.dataframe.index)
        with tqdm(total=total) as pbar:

            # Loop over the combined dataframe
            for number, row in self.dataframe.iterrows():
                # If this sentence isn't the last sentence
                if row["Translation"] != sentence:

                    sentence = row["Translation"]
                    sentences_list.append(sentence)

                    # This only needs to be run when either the normal, time, vocal, or combined parameters are turned
                    # to True. The sentence_list has been created before this block.
                    if normal == True or time == True or vocal == True or combined == True:

                        # Create a temporary dataframe that holds the data from the original dataset that belongs to a
                        # single sentence.
                        temporary_dataframe = self.dataframe[self.dataframe['Translation'] == str(sentence)]

                        normal_string = ""
                        normal_time = ""
                        normal_vocal = ""
                        normal_combined = ""

                        # Loop over the temporary dataframe
                        for number, row in temporary_dataframe.iterrows():
                            if normal:
                                normal_string += self.normal_function(row, standardisation=standardisation)

                            if time:
                                normal_time += self.time_function(row, standardisation=standardisation)

                            if vocal:
                                normal_vocal += self.vocal_function(row, standardisation=standardisation)

                            if combined:
                                normal_combined += self.combined_function(row, standardisation=standardisation)

                        # Append all the words into a list once per sentence
                        vocal_list.append(normal_vocal)
                        normal_list.append(normal_string)
                        times_list.append(normal_time)
                        combined_list.append(normal_combined)
                # Update the progress-bar by 1
                pbar.update(1)

        # These if-statements correspond to the parameters specified in the initialisation of the function.
        if sentences:
            # Source of the line after this comment:
            # User764357. (2014, Jan 9). How can I remove Nan from list Python/NumPy. Stackoverflow.com.
            # https://stackoverflow.com/questions/21011777/how-can-i-remove-nan-from-list-python-numpy
            cleaned_list = [x for x in sentences_list if str(x) != "nan"]  # Clear the sentence list of all empty lines

            self.func(str(output_path) + "sentences.nl", cleaned_list)  # Create the file
        if normal:
            self.func(str(output_path) + "normal.en", normal_list)  # Create the file
        if time:
            self.func(str(output_path) + "times.en", times_list)  # Create the file
        if vocal:
            self.func(str(output_path) + "vocal.en", vocal_list)  # Create the file
        if combined:
            self.func(str(output_path) + "combined.en", combined_list)  # Create the file

    def normal_function(self, row, standardisation=False):
        """
        A function to generate the sentence in Sign-Glosses based on the row.

        :param row: pandas row, the row for which the text needs to be determined
        :param standardisation: boolean, True enables standardising the words. Greatly increases runtime.
        :return: string, a string that holds the entire sentence
        """
        normal_string = ""

        if standardisation:
            pre_standarised_left = row['Left']
            left = self.standardisation(pre_standarised_left)
            pre_standarised_right = row['Right']
            right = self.standardisation(pre_standarised_right)
        else:
            left = row['Left']
            right = row['Right']

        if str(right) == "nan" and str(left) == "nan":
            pass
        elif str(right) == "nan":
            normal_string += f"{left} "
        elif str(left) == "nan":
            normal_string += f"{right} "
        elif str(left) != "nan" and str(right) != "nan":
            normal_string += f"{left} {right} "
        else:
            pass

        return normal_string

    def time_function(self, row, standardisation=False):
        """
        A function to generate the sentence in Sign-Glosses|Time-token based on the row.

        :param row: pandas row, the row for which the text needs to be determined
        :param standardisation: boolean, True enables standardising the words. Greatly increases runtime.
        :return: string, a string that holds the entire sentence
        """
        normal_time = ""

        if standardisation:
            pre_standarised_left = row['Left']
            left = self.standardisation(pre_standarised_left)
            pre_standarised_right = row['Right']
            right = self.standardisation(pre_standarised_right)
            tijd = format(row["Time"], '04d')
        else:
            left = row['Left']
            # Tijd is the Dutch word for time this is done to distinguish between parameter
            # time and variable time (tijd)
            tijd = format(row["Time"], '04d')
            right = row['Right']

        if str(right) == "nan" and str(left) == "nan":
            pass
        elif str(right) == "nan":
            normal_time += f"{left}￨{tijd} "
        elif str(left) == "nan":
            normal_time += f"{right}￨{tijd} "
        elif str(left) != "nan" and str(right) != "nan":
            normal_time += f"{left}￨{tijd} {right}￨{tijd} "
        else:
            pass
        return normal_time

    def vocal_function(self, row, standardisation=False):
        """
        A function to generate the sentence in Sign-Glosses|Vocal-Token based on the row.

        :param row: pandas row, the row for which the text needs to be determined
        :param standardisation: boolean, True enables standardising the words. Greatly increases runtime.
        :return: string, a string that holds the entire sentence
        """
        normal_vocal = ""

        if standardisation:
            pre_standarised_left = row['Left']
            left = self.standardisation(pre_standarised_left)
            pre_standarised_right = row['Right']
            right = self.standardisation(pre_standarised_right)
            vocal_line = row["Mouth"]
        else:
            left = row['Left']
            vocal_line = row["Mouth"]
            right = row['Right']

            # OpenNMT has some restriction when it comes to having source factors in the dataset, as
            # opposed to MarianNMT all the words must have the same amount of source factors. Therefore
            # if a word doesn't have a vocal gloss, a "none" will be assigned to this word.

            if vocal_line == "nan":
                vocal_line = "none"

        if str(right) == "nan" and str(left) == "nan":
            pass
        elif str(right) == "nan":
            normal_vocal += f"{left}￨{vocal_line} "
        elif str(left) == "nan":
            normal_vocal += f"{right}￨{vocal_line} "
        elif str(left) != "nan" and str(right) != "nan":
            normal_vocal += f"{left}￨{vocal_line} {right}￨{vocal_line} "
        else:
            pass

        return normal_vocal

    def combined_function(self, row, standardisation=False):
        """
        A function to generate the sentence in Sign-Glosses|Vocal-Token|Time-token based on the row.

        :param row: pandas row, the row for which the text needs to be determined
        :param standardisation: boolean, True enables standardising the words. Greatly increases runtime.
        :return: string, a string that holds the entire sentence
        """
        normal_combined = ""

        if standardisation:
            pre_standarised_left = row['Left']
            left = self.standardisation(pre_standarised_left)
            pre_standarised_right = row['Right']
            right = self.standardisation(pre_standarised_right)
            tijd = format(row["Time"], '04d')
            vocal_line = row["Mouth"]
        else:
            left = row['Left']
            vocal_line = row["Mouth"]
            right = row['Right']
            tijd = format(row["Time"], '04d')

            # OpenNMT has some restriction when it comes to having source factors in the dataset, as
            # opposed to MarianNMT all the words must have the same amount of source factors. Therefore
            # if a word doesn't have a vocal gloss, a "none" will be assigned to this word.

            if vocal_line == "nan":
                vocal_line = "none"

        # If both the glosses are empty, skip the line. This will remove the empty lines in the eventual file.
        if str(right) == "nan" and str(left) == "nan":
            pass
        elif str(right) == "nan":
            normal_combined += f"{left}￨{vocal_line}￨{tijd} "
        elif str(left) == "nan":
            normal_combined += f"{right}￨{vocal_line}￨{tijd} "
        elif str(left) != "nan" and str(right) != "nan":
            normal_combined += f"{left}￨{vocal_line}￨{tijd} {right}￨{vocal_line}￨{tijd} "
        else:
            pass

        return normal_combined

    def standardisation(self, word):
        """
        Standardises the inputted word by removing characters such as: {1, ^, &, 234, |, ;}
        and by leaving only (latin) alphabetical characters in place, upper-case and lower-case
        letters will remain their respective case.

        Example:
        - word = BU1G4R|A
        - output = BUGRA

        :param word: string, word input that needs to be standardised
        :return: string, standardised word with all non-latin-alphabetical characters removed
        """
        # Source:
        # timgeb. (2015, Dec 11). Python: keep only letters in string [duplicate]. Stackoverflow.com.
        # https://stackoverflow.com/questions/34214139/python-keep-only-letters-in-string

        return ''.join(filter(str.isalpha, str(word)))

    def __repr__(self):
        return f"Input files: {self.inputs}"
