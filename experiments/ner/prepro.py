import os
import argparse
from sys import path
path.append(os.getcwd())
from data_utils.task_def import DataFormat
from data_utils.log_wrapper import create_logger
from experiments.ner.ner_utils import load_conll_chunk, load_conll_ner, load_conll_pos, read_tsv, read_iob2, load_sent_classd
from experiments.common_utils import dump_rows
logger = create_logger(__name__, to_disk=True, log_file='bert_ner_data_proc_512_cased.log')

def parse_args():
    parser = argparse.ArgumentParser(description='Preprocessing English NER dataset.')
    parser.add_argument('--data_dir', type=str, required=True)
    parser.add_argument('--seed', type=int, default=13)
    parser.add_argument('--output_dir', type=str, required=True)
    args = parser.parse_args()
    return args

def main(args):
    data_dir = args.data_dir
    data_dir = os.path.abspath(data_dir)
    if not os.path.isdir(data_dir):
        os.mkdir(data_dir)

    bc2_train_path = os.path.join(data_dir, 'bc2_train.tsv')
    bc2_dev_path = os.path.join(data_dir, 'bc2_devel.tsv')
    bc2_test_path = os.path.join(data_dir, 'bc2_test.tsv')
    bc2_train_data = read_tsv(bc2_train_path)
    bc2_dev_data = read_tsv(bc2_dev_path)
    bc2_test_data = read_tsv(bc2_test_path)

    bc5_chem_train_path = os.path.join(data_dir, 'bc5_chem_train.tsv')
    bc5_chem_dev_path = os.path.join(data_dir, 'bc5_chem_devel.tsv')
    bc5_chem_test_path = os.path.join(data_dir, 'bc5_chem_test.tsv')
    bc5_chem_train_data = read_tsv(bc5_chem_train_path, num_cols=4, entity_label='CHEM')
    bc5_chem_dev_data = read_tsv(bc5_chem_dev_path, num_cols=4, entity_label='CHEM')
    bc5_chem_test_data = read_tsv(bc5_chem_test_path, num_cols=4, entity_label='CHEM')

    bc5_disease_train_path = os.path.join(data_dir, 'bc5_disease_train.tsv')
    bc5_disease_dev_path = os.path.join(data_dir, 'bc5_disease_devel.tsv')
    bc5_disease_test_path = os.path.join(data_dir, 'bc5_disease_test.tsv')
    bc5_disease_train_data = read_tsv(bc5_disease_train_path, num_cols=4, entity_label='DISEASE')
    bc5_disease_dev_data = read_tsv(bc5_disease_dev_path, num_cols=4, entity_label='DISEASE')
    bc5_disease_test_data = read_tsv(bc5_disease_test_path, num_cols=4, entity_label='DISEASE')

    ncbi_train_data = read_iob2(os.path.join(data_dir, 'ncbi_disease_train.iob2'))
    ncbi_dev_data = read_iob2(os.path.join(data_dir, 'ncbi_disease_dev.iob2'))
    ncbi_test_data = read_iob2(os.path.join(data_dir, 'ncbi_disease_test.iob2'))

    chemprot_train_data = load_sent_class(os.path.join(data_dir, 'chemprot_train.tsv'))
    chemprot_dev_data = load_sent_class(os.path.join(data_dir, 'chemprot_dev.tsv'))
    chemprot_test_data = load_sent_class(os.path.join(data_dir, 'chemprot_test.tsv'))

    ddi_train_data = load_sent_class(os.path.join(data_dir, 'ddi_train.tsv'))
    ddi_dev_data = load_sent_class(os.path.join(data_dir, 'ddi_dev.tsv'))
    ddi_test_data = load_sent_class(os.path.join(data_dir, 'ddi_test.tsv'))

    bert_root = args.output_dir
    if not os.path.isdir(bert_root):
        os.mkdir(bert_root)
    train_fout = os.path.join(bert_root, 'ner_train.tsv')
    dev_fout = os.path.join(bert_root, 'ner_dev.tsv')
    test_fout = os.path.join(bert_root, 'ner_test.tsv')

    bc2_train_fout = os.path.join(bert_root, 'bc2_train.tsv')
    bc2_dev_fout = os.path.join(bert_root, 'bc2_dev.tsv')
    bc2_test_fout = os.path.join(bert_root, 'bc2_test.tsv')
    dump_rows(bc2_train_data, bc2_train_fout, DataFormat.Seqence)
    dump_rows(bc2_dev_data, bc2_dev_fout, DataFormat.Seqence)
    dump_rows(bc2_test_data, bc2_test_fout, DataFormat.Seqence)

    bc5_chem_train_fout = os.path.join(bert_root, 'bc5chem_train.tsv')
    bc5_chem_dev_fout = os.path.join(bert_root, 'bc5chem_dev.tsv')
    bc5_chem_test_fout = os.path.join(bert_root, 'bc5chem_test.tsv')
    dump_rows(bc5_chem_train_data, bc5_chem_train_fout, DataFormat.Seqence)
    dump_rows(bc5_chem_dev_data, bc5_chem_dev_fout, DataFormat.Seqence)
    dump_rows(bc5_chem_test_data, bc5_chem_test_fout, DataFormat.Seqence)

    dump_rows(bc5_disease_train_data, os.path.join(bert_root, 'bc5disease_train.tsv'), DataFormat.Seqence)
    dump_rows(bc5_disease_dev_data, os.path.join(bert_root, 'bc5disease_dev.tsv'), DataFormat.Seqence)
    dump_rows(bc5_disease_test_data, os.path.join(bert_root, 'bc5disease_test.tsv'), DataFormat.Seqence)

    dump_rows(ncbi_train_data, os.path.join(bert_root, 'ncbidisease_train.tsv'), DataFormat.Seqence)
    dump_rows(ncbi_dev_data, os.path.join(bert_root, 'ncbidisease_dev.tsv'), DataFormat.Seqence)
    dump_rows(ncbi_test_data, os.path.join(bert_root, 'ncbidisease_test.tsv'), DataFormat.Seqence)

    dump_rows(chemprot_train_data, os.path.join(bert_root, 'chemprot_train.tsv'), DataFormat.PremiseAndOneHypothesis)
    dump_rows(chemprot_dev_data, os.path.join(bert_root, 'chemprot_dev.tsv'), DataFormat.PremiseAndOneHypothesis)
    dump_rows(chemprot_test_data, os.path.join(bert_root, 'chemprot_test.tsv'), DataFormat.PremiseAndOneHypothesis)

    dump_rows(ddi_train_data, os.path.join(bert_root, 'ddi_train.tsv'), DataFormat.PremiseAndOneHypothesis)
    dump_rows(ddi_dev_data, os.path.join(bert_root, 'ddi_dev.tsv'), DataFormat.PremiseAndOneHypothesis)
    dump_rows(ddi_test_data, os.path.join(bert_root, 'ddi_test.tsv'), DataFormat.PremiseAndOneHypothesis)

if __name__ == '__main__':
    args = parse_args()
    main(args)