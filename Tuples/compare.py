""" compare output/PR with PR (input) & output/PS with PS (input)
    does one have files the other is missing?
"""
import pathlib

import numpy as np


def main():

    for in_dir, out_dir in [("PS", "output/PS"), ("PR", "output/PR")]:


        in_fps = pathlib.Path(in_dir).glob('*txt')
        out_fps = pathlib.Path(out_dir).glob('*json')

        # get dicts of filename:filepath
        in_name2fp = {fp.stem:fp for fp in in_fps}
        out_name2fp = {fp.stem:fp for fp in out_fps}

        # get names of files
        in_names = set(in_name2fp.keys())
        out_names = set(out_name2fp.keys())

        # get list of filenames present in output, but absent in input
        redundant = out_names - in_names
        print('redundant', len(redundant))   

        # # remove files present in output, but absent in input
        # for r in redundant:
        #     out_name2fp[r].unlink()

        # get list of filename present in input, but absent in output
        missing = in_names - out_names
        print(f'missing', missing)





if __name__ == "__main__":
    main()
