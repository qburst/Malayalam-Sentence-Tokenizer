# Malayalam-Sentence-Tokenizer

A rule-based implementation of Malayalam sentence tokenizer. 

## Tokenization

The tokenizer accepts a list of articles and split as a set of sentences.

### Usage

`python tokenizer.py --src_dir ./dataset/input/ --result_dir ./dataset/output/`


## Evaluation

The evaluation script reads the input articles, ground truth files and the tokenized output in order to calculate the precision and the recall.

### Usage 
`python eval.py --data_src ./dataset/`

