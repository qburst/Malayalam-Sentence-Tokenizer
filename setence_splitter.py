import sys
import codecs

from tokenizer import RuleBasedSentenceTokenizer


def main(input_file):
    sentence_list = list()
    with codecs.open(input_file, 'r','utf8') as fin:
        data = fin.read()
        
    tokenizer = RuleBasedSentenceTokenizer()
    sentence_list = tokenizer.tokenize(data)
    for sentence in sentence_list:
        print(sentence)

if __name__=="__main__":
    try:
        main(sys.argv[1])
    except Exception as e:
        print(e)
