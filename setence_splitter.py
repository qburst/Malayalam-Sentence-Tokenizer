import os
import sys
import codecs
import argparse


from tokenizer import RuleBasedSentenceTokenizer


def main(input_file):
    sentence_list = list()
    with codecs.open(input_file, 'r','utf8') as fin:
        data = fin.read()
        
    tokenizer = RuleBasedSentenceTokenizer()
    sentence_list = tokenizer.tokenize(data)
    for sentence in sentence_list:
        print(sentence)


def process_multiple_articles(base_path, result_dir):

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
    parser.add_argument('input', nargs='?', help="Enter data path")
    parser.add_argument('--src_dir', help="Enter data path")
    parser.add_argument('--result_dir', help="Enter data path")
    args = parser.parse_args()
    if not args.src_dir:
        try:
            main(sys.argv[1])
            sys.exit()
        except Exception as e:
            print(e)
    src_dir = args.src_dir
    result_dir = args.result_dir
    if not os.path.isdir(src_dir) or not os.path.isdir(result_dir):
        print("Invalid input/result directory")
        sys.exit()
    process_multiple_articles(src_dir, result_dir)


