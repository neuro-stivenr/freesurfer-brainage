# freesurfer-brainage

Wrapper script for running brain age extraction implemented via ANTsPyNet python module:
[ANTsPyNet](https://github.com/ANTsX/ANTsPyNet)

Right now, it's centered around running the script on FreeSurfer output directories.
Might add functionality later to run on individual T1w nifti images.

## Installation & Usage

```sh
# installing the python package
pip install git+https://github.com/neuro-stivenr/freesurfer-brainage

# computing brain age from freesurfer directory
compute_brainage --fsdir $SUBJECTS_DIR

# computing brain age for one subject in freesurfer directory
# might be useful when running in parallel on cluster
compute_brainage --fsdir $SUBJECTS_DIR --subj sub-TEST01

# compiling brain age from freesurfer directory into single .csv
compile_brainage --fsdir $SUBJECTS_DIR
```
