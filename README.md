# Malayalam-Sentence-Tokenizer

A rule-based implementation of Malayalam sentence tokenizer. 

## Tokenization

The `setence_splitter.py` script gives you a list of sentences for your input article(s)

### Usage

The following usage accepts the input.txt and writes each sentence into the console.  
`python setence_splitter.py input.txt`


If you want to perform sentence split for a large number of files, then run the script as follows.  
`python setence_splitter.py --src_dir ./dataset/input/ --result_dir ./dataset/output/`


## Evaluation

The evaluation script reads the input articles, ground truth files and the tokenized output in order to calculate the precision and the recall.

### Usage 
`python eval.py --data_src ./dataset/`

