import re
import codecs


ABBREVIATION_PATH = './abbreviations.txt'


class RuleBasedSentenceTokenizer():
    def __init__(self):
        self.regex = r'([ഀ-ൿ\u200C\u200D"”?A-Za-z]+ *\.+|[0-9]+ *\. |[ഀ-ൿ\u200C\u200D"”A-Za-z]+ *\?)'
        self.url_regex = r'(?:https|http)://[a-z0-9\.\-\/]+'
        self.quote_regex = r'["”“]+'

        self.abb_list = self.__read_abbreviations(ABBREVIATION_PATH)

    def __read_abbreviations(self, model):
        with codecs.open(model, 'r', 'utf8') as fin:
            abb_list = fin.read().lower().split("\n")
        return abb_list

    def __get_url_indices(self, data):
        urls = re.findall(self.url_regex, data)
        url_indices = list()
        for url in urls:
            url_index = data.index(url)
            url_indices += list(range(
                url_index, url_index+len(url)-1))
        return url_indices

    def tokenize(self, data):
        dataset = data.split("\n")
        sentences = list()
        for data in dataset:
            sentence_ends = re.findall(self.regex, data)
            for end in sentence_ends:
                end_idx = data.index(end)+len(end)
                url_indices = self.__get_url_indices(data)
                if end_idx in url_indices:
                    continue
                sentence = data[: end_idx]
                quotes_list = re.findall(self.quote_regex, sentence)
                if (quotes_list and ((sentence.count('"') % 2 > 0)
                    or (sentence.count('“') == sentence.count('”')))) \
                        or (not quotes_list and end.lower() not in self.abb_list):
                    sentences.append(sentence)
                    data = data[end_idx:]
            if data:
                sentences.append(data)
        return sentences
