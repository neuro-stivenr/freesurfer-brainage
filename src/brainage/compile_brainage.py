#!/usr/bin/env python

from pathlib import Path
from sys import argv
import argparse
import logging

from tqdm import tqdm
import pandas as pd

def _init_parser():
    parser = argparse.ArgumentParser(
        prog='compile_brainage',
        description='Compiles brainage.txt files from multiple FreeSurfer subject directories into a single .csv spreadsheet file.'
    )
    parser.add_argument('--fsdir', required=True, help='FreeSurfer subjects directory.')
    return parser

def main():
    logging.getLogger().setLevel(logging.INFO)
    args = vars(_init_parser().parse_args(argv[1:]))
    freesurfer = Path(args['fsdir'])
    output_path = freesurfer.joinpath('brainage_all.csv')
    if not freesurfer.exists():
        logging.error(f'Directory does not exist: \n{freesurfer}')
    brainage_files = list(freesurfer.glob('*/mri/brainage.txt'))
    logging.info(f'Computing brain age for {len(brainage_files)} subjects.')
    brainage_dict = {}
    for brainage_file in tqdm(brainage_files):
        subjid = brainage_file.parent.parent.name
        with open(str(brainage_file)) as handle:
            brain_age = float(handle.read())
        brainage_dict[subjid] = brain_age
    df_brainage = pd.DataFrame({'brain_age': pd.Series(brainage_dict)})
    logging.info(f'Output is written to: \n{output_path}')
    df_brainage.to_csv(output_path)
    logging.info('DONE!')

if __name__ == '__main__':
    # logging
    # running the program
    main()
