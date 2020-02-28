import os
import sys
import re
import codecs
import argparse


ABBREVIATION_PATH = './abbreviations.txt'


class RuleBasedSentenceTokenizer():
    def __init__(self):
        self.regex = r'([ഀ-ൿ\u200C\u200D"A-Za-z]+ *\.|[0-9]+ *\. )'
        self.abb_list = self.__read_abbreviations(ABBREVIATION_PATH)

    def __read_abbreviations(self, model):
        with codecs.open(
                model, 'r','utf8') as fin:
            abb_list = fin.read().lower().split("\n")
        return abb_list

    def tokenize(self, data):
        dataset = data.split("\n")
        sentences = list()
        for data in dataset:
            sentence_ends = re.findall(self.regex, data)
            for end in sentence_ends:
                if end.lower() not in self.abb_list:
                    end_idx = data.index(end)+len(end)
                    sentence = data[: end_idx]
                    sentences.append(sentence)
                    data = data[end_idx:]
            if data:
                sentences.append(data)
        return sentences


def main(base_path, result_dir):

    files = os.listdir(base_path)
    for filename in files:
        sentence_list = list()
        input_path = os.path.join(base_path, filename)
        with codecs.open(input_path, 'r','utf8') as fin:
            data = fin.read()
        
        tokenizer = RuleBasedSentenceTokenizer()
        sentence_list = tokenizer.tokenize(data)
        sentence_list = map(lambda x: x+"\n", sentence_list)
       
        output_path = os.path.join(result_dir, filename)
        with codecs.open(output_path, "w+", 'utf8') as fout:
            fout.writelines(sentence_list)


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--src_dir', help="Enter data path", required=True)
    parser.add_argument('--result_dir', help="Enter data path", required=True)
    args = parser.parse_args()
    src_dir = args.src_dir
    result_dir = args.result_dir
    if not os.path.isdir(src_dir) or not os.path.isdir(result_dir):
        print("Invalid input/result directory")
        sys.exit()
    main(src_dir, result_dir)
