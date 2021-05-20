# Multiple feature Gloss to Text translation 
Gijs Thissen - 21-05-2021
Code for the Bachelor Thesis Cognitive Science and Artificial Intelligence
This code has been created for the purposes of my Bachelor Thesis CSAI.

The goal of the thesis was to figure out whether or not adding temporal data (and other tokens) to a baseline gloss system would aid in its ability to translate gloss to text.
The resultsshow that adding these extra tokens to the data results in a less accurate translation across allmodels. The neural machine translation system with an input of nothing but glosses [BLEU 3.69,TER 0.960] outperforms the more complex models [average BLEU 2.19, average TER 0.981].


Requirements:

OpenNMT-py==v1.2.0

How to install:
```
pip install OpenNMT-py==v1.2.0
```

# Documentation

Running main.py will create the basic 5 (fixed) files needed to run each of the 4 experiments.
f-normal.en, f-times.en, f-vocal.en, f-combined.en, f-sentences.nl

All of the commands shown below require the user to put them into the terminal, not a seperate python file.
These commands are considered for 1 single experiments, source.en can be any of the en files. However, f-sentences.nl must always be the sentence file.

It is recommended to put the files for the experiment you want to run into a seperate folder as to avoid removing the whitespaces twice and creating double files, however, this is not necessary and the programme will work nonetheless.

Example:
Create a experiment1/ folder.

1. Preprocessing
First the files need to be splitted using train_test_dev.py. The command needed to run:
```
python train_test_dev.py -s source.en -t f-sentences.nl
```

Since the train_test_dev.py script creates files with empty space in between them. This causes the machine translation system to interpret these lines as sentences
and starts assigning sentences to empty lines. Therefore running the following script is necessary

```
python remove_whitespace.py
```

Secondly, the BPE algorithm needs to be applied:
1. Preprocessing
The BPE algorithm needs to be applied:

1. Train the bpe models using the train.src and train.trg files:
```
python learn_bpe.py -i f-train.src -o src.code

python learn_bpe.py -i f-train.trg -o trg.code
```
2. Apply the bpe algorithm using the bpe models on all the files used in that experiment, except trg-test.bpe.trg:

!!!!IMPORTANT!!!! When experimenting with times.en use apply_bpe_temporal.py instead !!!!IMPORTANT!!!!
```
python apply_bpe.py -c src.code -i f-train.src -o src-train-bpe.src

python apply_bpe.py -c src.code -i f-dev.src -o src-dev-bpe.src

python apply_bpe.py -c src.code -i f-test.src -o src-test-bpe.src

python apply_bpe.py -c trg.code -i f-train.trg -o trg-train-bpe.trg

python apply_bpe.py -c trg.code -i f-dev.trg -o trg-dev-bpe.trg
```

Secondly, preprocess the data one final time to being able to be used by the OpenNMT transformer
```
onmt_preprocess -train_src src-train-bpe.src -train_tgt trg-train-bpe.trg -valid_src src-dev-bpe.src -valid_tgt trg-dev-bpe.trg -save_data result
```
2. Training
```
onmt_train -data result -save_model model -layers 6 -rnn_size 512 -word_vec_size 512 -transformer_ff 2048 -heads 8 -encoder_type transformer -decoder_type transformer -position_encoding -train_steps 202000 -max_generator_batches 2 -dropout 0.1 -batch_size 2048 -batch_type tokens -normalization tokens -optim adam -adam_beta2 0.998 -decay_method noam -warmup_steps 2000 -learning_rate 2 -max_grad_norm 0 -param_init 0 -param_init_glorot -label_smoothing 0.1 -valid_steps 5000 -save_checkpoint_steps 5000 -report_every 100 -accum_count 2 -early_stopping 5 -early_stopping_criteria ppl accuracy -world_size 1 -gpu_rank 0 -log_file train.log
```

Possible error: Not enough V-RAM.
Solution: Decrease the batch size or alternatively use a better GPU.

3. Translating

In the command the last model (20k steps) is selected. If the system stops earlier due to early stopping criteria use that model step instead.
```
onmt_translate -model model_step_20000.pt -src src-test-bpe.src -output pred.txt -gpu 0 -verbose -replace_unk
```
4. Detokenizing the tokenization done by the BPE-algorithm
```
sed -i "s/@@ //g"  pred.txt
```
# Sources:

learn_bpe.py [2]

apply_bpe.py [2]

apply_bpe_temporal.py [2]

train_test_dev.py [4]


Sources can be found when used in the code:

1. DDGG. (2018, Feb 22) tqdm not showing bar. Stackoverflow.com. https://stackoverflow.com/questions/48935907/tqdm-not-showing-bar
2. Klein, G., Kim, Y., Deng, Y., Senellart, J., & Rush, A. (2017). OpenNMT: Open-source toolkit forneural machine translation. InProceedings of ACL 2017, System Demonstrations, (pp. 67–72).,Vancouver, Canada. Association for Computational Linguistics
3. timgeb. (2015, Dec 11). Python: keep only letters in string [duplicate]. Stackoverflow.com. https://stackoverflow.com/questions/34214139/python-keep-only-letters-in-string
4. Shterionov, D. (2020). Python: train_test_dev.py. Tilburg University.
5. User764357. (2014, Jan 9). How can I remove Nan from list Python/NumPy. Stackoverflow.com. https://stackoverflow.com/questions/21011777/how-can-i-remove-nan-from-list-python-numpy
