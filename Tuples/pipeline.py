import itertools
import json
import pathlib
import re
import sys
import typing
from functools import partial
from itertools import cycle, product
from pprint import pprint as pp
import numpy as np
from multiprocessing import Pool

from tqdm import tqdm
# from tqdm.contrib.concurrent import process_map

# import .py files in ./loaders
for p in pathlib.Path("Loaders").glob("*.py"):
    exec(f"import Loaders.{p.stem}")

# import .py files in ./parsers
for p in pathlib.Path("parsers").glob("*.py"):
    exec(f"import parsers.{p.stem}")

# load the classes containing patterns
for p in pathlib.Path("patterns").glob("*.py"):
    exec(f"import patterns.{p.stem}")

from tuple_fetcher import get_tuples

def main(args):

    # load configs
    with open("configs.json", "r") as f:
        configs: list[dict] = json.loads(f.read())

    # iterate over the configs
    for config_i, config in enumerate(configs, start=1):
        print(f"runnng {config_i} of {len(configs)}")

        # run config if switched on
        if config["switch"] == True:

            ### 1. create a list of outstanding books to be processed

            # create iterable of input files
            input_dir = pathlib.Path(config["input"][0]).expanduser().resolve()
            input_pattern = re.compile(config["input"][1])
            fps: list[pathlib.Path] = list(gen_dir(input_dir, pattern=input_pattern))

            # ignore input files with results
            output_dir = pathlib.Path(config["output_dir"]).expanduser().resolve()
            output_dir.mkdir(exist_ok=True, parents=True)
            fps:list[str] = [str(fp) for fp in fps if (output_dir / f"{fp.stem}.json").exists() == False]

            print(f'number of outstanding files to retrieve={len(fps)}')

            # ensure 'fps_lists' exist
            fps_lists_dir = pathlib.Path("fps_lists").expanduser().resolve()
            fps_lists_dir.mkdir(parents=True, exist_ok=True)

            ### 2. Make sub-lists of outstanding books fps, one for each of n_processes

            ## Check if we have all the lists we need already saved
            n_processes = int(config['n_processes'])
            name = config['set']
            fps_lists_fps = [fps_lists_dir / f'{name}_{config_i}_{i}.json' for i in range(1, n_processes+1)]

            if all([fp.exists() for fp in fps_lists_fps]):
                pass
            else:

                ## otherwise re-build the lists and save them
                chunks = [list(chunk) for chunk in np.array_split(fps, n_processes)]
                for chunk, fp in zip(chunks, fps_lists_fps):
                    with open(fp, 'w') as f:
                        json.dump(chunk, f)

            ### 3. Run the pipeline wrt., the current process

            if n_processes == 1:
                pipeline(config, fps_lists_dir / f'{name}_{config_i}_1.json')
            else:
                num = int(args[0])
                pipeline(config, fps_lists_dir / f'{name}_{config_i}_{num}.json')

def pipeline(config: dict, fps_list_fp:pathlib.Path):

    parser: typing.Callable = eval(config["parser"])

    patterns = eval(config["patterns"])()

    # the loader does the work, it returns
    loader = eval(config["loader"])

    output_dir = pathlib.Path(config["output_dir"]).expanduser().resolve()

    # get dict used by loader for handling cut words
    with open(
        pathlib.Path(config["dictionary_fp"]).expanduser().resolve(),
        "r",
        encoding="utf-8",
    ) as f:
        dictionary: set[str] = set([w.strip("\n") for w in f.readlines()])

    # load the list of book filepaths to consider in this process
    with open(fps_list_fp, 'r') as f:
        fps:list[pathlib.Path] = [pathlib.Path(fp) for fp in json.load(f)]
    
    for fp in tqdm(fps):

        print(fp.stem)

        # get sentence parts for fp
        df = loader(fp, dictionary)

        # get parses wrt., df
        parses: list[tuple] = parser(df)

        # ------
        # get the tuples from the parses
        # ------
        adj_tiers = patterns.adj_tiers
        verb_tiers = patterns.verb_tiers
        # where pattern_tiers[i] is a list of patterns
        # where pattern_tiers[i][j] is a tuple, corresponding to a pattern,
        #   of (pattern_s::dict, pattern_p, pattern_t::list[tuple])

        # get tuples for df
        tuples = []
        for text, (parse_s, parse_p) in tqdm(zip(df['text'], parses)):
            found_tuples = list(set(get_tuples(parse_s, parse_p, adj_tiers)))  # adj
            # Note: list(set ... ensures unique tuple instances by text
            if len(found_tuples) > 0:
                tuples += (text, found_tuples)
        for text, (parse_s, parse_p) in tqdm(zip(df['text'], parses)):
            found_tuples = list(set(get_tuples(parse_s, parse_p, verb_tiers)))  # verbs
            # Note: list(set ... ensures unique tuple instances by text
            if len(found_tuples) > 0:
                tuples += (text, found_tuples)

        # # save tuples for doc
        with open(output_dir / f"{fp.stem}.json", "w", encoding="utf-8") as f:
            json.dump(tuples, f)


def gen_dir(
    dir_path: pathlib.Path,
    *,
    pattern: re.Pattern = re.compile(".+"),
    ignore_pattern: typing.Union[re.Pattern, None] = None,
) -> typing.Generator:
    """Return a generator yielding pathlib.Path objects in a directory,
    optionally matching a pattern.

    Args:
        dir (str): directory from which to retrieve file names [default: script dir]
        pattern (re.Pattern): re.search pattern to match wanted files [default: all files]
        ignore (re.Pattern): re.search pattern to ignore wrt., previously matched files
    """

    for fp in filter(lambda fp: re.search(pattern, str(fp)), dir_path.glob("*")):

        # no ignore pattern specified
        if ignore_pattern is None:
            yield fp
        else:
            # ignore pattern specified, but not met
            if re.search(ignore_pattern, str(fp)):
                pass
            else:
                yield fp


def gen_chunks(iterable: typing.Iterable, chunk_size: int) -> typing.Generator:
    """Return a generator yielding chunks (as iterators) of passed iterable."""
    it = iter(iterable)
    while True:
        chunk = itertools.islice(it, chunk_size)
        try:
            first_el = next(chunk)
        except StopIteration:
            return
        yield itertools.chain((first_el,), chunk)


if __name__ == "__main__":
    main(sys.argv[1:])
