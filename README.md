# CSAI Thesis
Gijs Thissen - 21-05-2021
Code for the Bachelor Thesis Cognitive Science and Artificial Intelligence
This code has been created for the purposes of my Bachelor Thesis CSAI.

The goal of the thesis was to figure out whether or not adding temporal data (and other tokens) to a baseline gloss system would aid in its ability to translate gloss to text.
The resultsshow that adding these extra tokens to the data results in a less accurate translation across allmodels. The neural machine translation system with an input of nothing but glosses [BLEU 3.69,TER 0.960] outperforms the more complex models [average BLEU 2.19, average TER 0.981].


Requirements:

OpenNMT-py==v1.2.0

How to install:

pip install OpenNMT-py==v1.2.0


# Documentation

Running main.py will create the basic 5 (fixed) files needed to run each of the 4 experiments.
f-normal.en, f-times.en, f-vocal.en, f-combined.en, f-sentences.nl

1. Preprocessing
First the files need to be splitted using train_test_dev.py. The command needed to run:

pythhon train_test_dev.py -s source.en -t f-sentences.nl

Next the BPE algorithm needs to be applied:
1. Train the bpe models using the train.src and train.trg files:

python learn_bpe.py -i f-train.src -o src.code
python learn_bpe.py -i f-train.trg -o trg.code

2. Apply the bpe algorithm using the bpe models on all the files used in that experiment, except trg-test.bpe.trg:

python apply_bpe.py -c src.code -i \f-train.src -o src-train-bpe.src
python apply_bpe.py -c src.code -i \f-dev.src -o src-dev-bpe.src
python apply_bpe.py -c src.code -i \f-test.src -o src-test-bpe.src
python apply_bpe.py -c trg.code -i \f-train.trg -o trg-train-bpe.trg
python apply_bpe.py -c trg.code -i \f-dev.trg -o trg-dev-bpe.trg

And last preprocess the data one final time to being able to be used by the OpenNMT transformer

onmt_preprocess -train_src src-train-bpe.src -train_tgt trg-train-bpe.trg -valid_src src-dev-bpe.src -valid_tgt trg-dev-bpe.trg -save_data result

# Sources:
Sources can be found when used in the code

1. DDGG. (2018, Feb 22) tqdm not showing bar. Stackoverflow.com. https://stackoverflow.com/questions/48935907/tqdm-not-showing-bar
2. Klein, G., Kim, Y., Deng, Y., Senellart, J., & Rush, A. (2017). OpenNMT: Open-source toolkit forneural machine translation. InProceedings of ACL 2017, System Demonstrations, (pp. 67–72).,Vancouver, Canada. Association for Computational Linguistics
3. timgeb. (2015, Dec 11). Python: keep only letters in string [duplicate]. Stackoverflow.com. https://stackoverflow.com/questions/34214139/python-keep-only-letters-in-string
4. User764357. (2014, Jan 9). How can I remove Nan from list Python/NumPy. Stackoverflow.com. https://stackoverflow.com/questions/21011777/how-can-i-remove-nan-from-list-python-numpy
5. 
