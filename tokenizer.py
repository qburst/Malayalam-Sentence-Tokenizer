import re
import os 
import codecs
import argparse


class RuleBasedSentenceTokenizer():
    def __init__(self, model):
        self.regex = r'([ഀ-ൿ\u200C\u200D"A-Za-z]+ *\.|[0-9]+ *\. )'
        self.abb_list = self.__read_abbreviations(model)

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


def main(filepath, model, result_file):

    with codecs.open(filepath, 'r','utf8') as fin:
        data = fin.read()

    tokenizer = RuleBasedSentenceTokenizer(model)
    sentence_list = tokenizer.tokenize(data)
    with open(result_file, "w+") as f:
        f.writelines(sentence_list)


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--src_file', default=None, help="Enter data path")
    parser.add_argument('--model', default=None, help="Enter model file path")
    parser.add_argument('--result_file', default=None, help="Enter result file path")
    args = parser.parse_args()
    main(args.src_file, args.model, args.result_file)
