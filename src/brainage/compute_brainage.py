#!/usr/bin/env python

from pathlib import Path
from sys import argv
import argparse
import logging

from tqdm import tqdm
import antspynet as asnet
import ants

def _init_parser():
    parser = argparse.ArgumentParser(
        prog='brainage',
        description='Calculates brain age for either one participant or the entire FreeSurfer subjects directory.'
    )
    parser.add_argument('--fsdir', required=True, help='FreeSurfer subjects directory.')
    parser.add_argument('--subj', required=False, default=None, help='Specific subject ID to process.')
    return parser

def extract_brain_age(t1w_path: str):
    t1w_path = str(t1w_path)
    t1w = ants.image_read(t1w_path)
    brain_age = asnet.brain_age(t1w)['predicted_age']
    return brain_age

def main():
    logging.getLogger().setLevel(logging.INFO)
    args = vars(_init_parser().parse_args(argv[1:]))
    freesurfer = Path(args['fsdir'])
    if not freesurfer.exists():
        logging.error(f'Directory does not exist: \n{freesurfer}')
    if args['subj'] is not None:
        logging.info(f'Computing brain age for {args["subj"]}.')
        mridir = freesurfer.joinpath(args['subj'], 'mri')
        origdir = mridir.joinpath('orig')
        t1w_path = origdir.joinpath('001.mgz')
        if not t1w_path.exists():
            logging.error(f'File does not exist: \n{t1w_path}')
        brain_age = extract_brain_age(t1w_path)
        output_path = mridir.joinpath('brainage.txt')
        with open(output_path, 'w') as handle:
            handle.write(str(brain_age))
    else:
        logging.info(f'Computing brain age for all subjects.')
        origdirs = list(freesurfer.glob('*/mri/orig'))
        for origdir in tqdm(origdirs):
            mridir = origdir.parent
            t1w_path = origdir.joinpath('001.mgz')
            if not t1w_path.exists():
                logging.warn(f'File does not exist: \n{t1w_path}')
            brain_age = extract_brain_age(t1w_path)
            output_path = mridir.joinpath('brainage.txt')
            with open(output_path, 'w') as handle:
                handle.write(brain_age)
    logging.info('DONE!')

if __name__ == '__main__':
    main()
