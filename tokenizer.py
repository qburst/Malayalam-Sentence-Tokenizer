import re
import codecs


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

