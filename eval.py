import os
import sys
import argparse
import codecs

class CustomTokenizerEvaluator:

    def _read_data(self, base_path, filename):
        result_data_path = os.path.join(base_path, "output", filename)
        with codecs.open(result_data_path, 'r','utf8') as fres:
            self._predicted_tokens = fres.readlines()
        
        gt_data_path = os.path.join(base_path, "gt", filename)
        if not os.path.exists(gt_data_path):
            raise Exception("Ground truth file is missing - %s" % filename)

        with codecs.open(gt_data_path, 'r','utf8') as gtf:
            self._gt_tokens = gtf.readlines()
        
        input_data_path = os.path.join(base_path, "input", filename)
        if not os.path.exists(input_data_path):
            raise Exception("Input data file is missing - %s" % filename)
        with codecs.open(gt_data_path, 'r','utf8') as gtf:
            self._data = gtf.read()

    def _get_tp_fp(self):
        correct_split_indices = list()
        for token in self._gt_tokens:
            correct_split_indices.append(
                    self._data.find(token.replace("\n", "")))
        correct_split_indices = correct_split_indices[1:]

        tp = 0
        fp = 0
        for token in self._predicted_tokens:
            token = token.strip()
            predicted_split_index  = self._data.find(token)
            if self._data.find(token) in correct_split_indices:
                tp += 1
            elif predicted_split_index != 0:
                fp += 1
        return tp, fp

    def evaluate(self, base_path, filename):
        self._read_data(base_path, filename)
        tp, fp = self._get_tp_fp()
        return tp, fp, len(self._gt_tokens)-1


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--data_src', help="Tokenized sentence dir", required=True)
    args = parser.parse_args()

    base_path = args.data_src

    output_dir = os.path.join(base_path, "output")
    if not os.path.isdir(output_dir):
        print("Output directory does not exist")
        sys.exit()
    files = os.listdir(output_dir)
    evaluator = CustomTokenizerEvaluator()

    total_tp = total_fp = total_gt = 0
    for filename in files:
        try:
            tp, fp, total_gt_in_file = evaluator.evaluate(base_path, filename)
        except Exception as e:
            print(e)
            continue
        total_tp += tp
        total_fp += fp
        total_gt += total_gt_in_file
    
        print("|", filename, "|", tp, "|", fp, "|", total_gt_in_file, "|")

    precision = total_tp/(total_tp+total_fp)
    recall = total_tp/total_gt 
    print("Precesion: ", precision, "Recall: ", recall)
