import os
from sys import path
path.append(os.getcwd())
from data_utils.task_def import DataFormat

import csv
import sys
csv.field_size_limit(sys.maxsize)

def read_tsv(
    tsv_file: str,
    num_cols=2,
    entity_label='GENE'
):
    rows = []
    with open(tsv_file) as tsvfile:
        tsvreader = csv.reader(tsvfile, delimiter="\t", quotechar=None)
        cnt = 0
        sentence = []
        label = []
        for line in tsvreader:
            if not line:
                sample = {'uid': cnt, 'premise': sentence, 'label': label}
                rows.append(sample)
                sentence = []
                label = []
                cnt += 1
                continue
            sentence.append(line[0])
            iob_label = line[num_cols - 1]
            if iob_label == 'B' or iob_label == 'I':
                iob_label += '-' + entity_label
            label.append(iob_label)
    return rows

def read_iob2(
    iob_file: str
):
    rows = []
    cnt = 0
    sentence = []
    label = []
    with open(iob_file, encoding="utf8") as f:
        for line in f:
            line = line.strip()
            if len(line)==0 or line.startswith('###MEDLINE') or line[0]=="\n":
                if len(sentence) > 0:
                    sample = {'uid': cnt, 'premise': sentence, 'label': label}
                    rows.append(sample)
                    sentence = []
                    label = []
                    cnt += 1
                continue
            splits = line.split('\t')
            sentence.append(splits[0])
            label.append(splits[-1])
        if len(sentence) > 0:
            sample = {'uid': cnt, 'premise': sentence, 'label': label}
    return rows

def load_sent_class(file, header=True):
    rows = []
    cnt = 0
    with open(file, encoding="utf8") as f:
        for line in f:
            if header:
                header = False
                continue
            blocks = line.strip().split('\t')
            if blocks[-1] == '-': continue
            lab = blocks[-1]
            if lab == 'false':
                lab = 'f-label'
            sample = {'uid': cnt, 'premise': blocks[1], 'hypothesis': blocks[2], 'label': lab}
            rows.append(sample)
            cnt += 1
    return rows

def load_conll_ner(file, is_train=True):
    rows = []
    cnt = 0
    sentence = []
    label= []
    with open(file, encoding="utf8") as f:
        for line in f:
            line = line.strip()
            if len(line)==0 or line.startswith('-DOCSTART') or line[0]=="\n":
                if len(sentence) > 0:
                    sample = {'uid': cnt, 'premise': sentence, 'label': label}
                    rows.append(sample)
                    sentence = []
                    label = []
                    cnt += 1
                continue
            splits = line.split(' ')
            sentence.append(splits[0])
            label.append(splits[-1])
        if len(sentence) > 0:
            sample = {'uid': cnt, 'premise': sentence, 'label': label}
    return rows

def load_conll_pos(file, is_train=True):
    rows = []
    cnt = 0
    sentence = []
    label= []
    with open(file, encoding="utf8") as f:
        for line in f:
            line = line.strip()
            if len(line)==0 or line.startswith('-DOCSTART') or line[0]=="\n":
                if len(sentence) > 0:
                    sample = {'uid': cnt, 'premise': sentence, 'label': label}
                    rows.append(sample)
                    sentence = []
                    label = []
                    cnt += 1
                continue
            splits = line.split(' ')
            sentence.append(splits[0])
            label.append(splits[1])
        if len(sentence) > 0:
            sample = {'uid': cnt, 'premise': sentence, 'label': label}
    return rows

def load_conll_chunk(file, is_train=True):
    rows = []
    cnt = 0
    sentence = []
    label= []
    with open(file, encoding="utf8") as f:
        for line in f:
            line = line.strip()
            if len(line)==0 or line.startswith('-DOCSTART') or line[0]=="\n":
                if len(sentence) > 0:
                    sample = {'uid': cnt, 'premise': sentence, 'label': label}
                    rows.append(sample)
                    sentence = []
                    label = []
                    cnt += 1
                continue
            splits = line.split(' ')
            sentence.append(splits[0])
            label.append(splits[2])
        if len(sentence) > 0:
            sample = {'uid': cnt, 'premise': sentence, 'label': label}
    return rows
