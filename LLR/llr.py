""" Build a {token:count, ...} dict, aggregating all .txt files in "input_dir"
"""

import json
import operator
import pathlib
import re
import typing
from collections import Counter, defaultdict
from itertools import cycle, tee

import numpy as np
from scipy.sparse import csr_matrix, lil_matrix, save_npz
from tqdm import tqdm
from tqdm.contrib.concurrent import process_map

def main():

    # load configs
    with open("configs.json", "r", encoding="utf-8") as f:
        configs = json.load(f)

    # iterate over configs
    for config in configs:

        # user-defined variables
        switch = config["switch"]
        input_dir = pathlib.Path(config["input_dir"]).expanduser().resolve()
        output_dir = pathlib.Path(config["output_dir"]).expanduser().resolve()

        # ...
        if switch:

            fps = list(input_dir.glob('*.json'))

            tuples = gen_tuples(fps)
            tuples_1, tuples_2, tuples_3, tuples_4, tuples_5, tuples_6 = tee(tuples, 6)
            # yields (noun, feature, role, pattern, filename) tuples

            # build frequency matrices and llr matrices
            for tuples_x, tuples_y, role in [
                (tuples_1, tuples_2, "adj"),
                (tuples_3, tuples_4, "agent"),
                (tuples_5, tuples_6, "patient"),
            ]:
                # i.e., tuples_x generator is exhausted building noun2i & feature2i wrt., specified role
                # i.e., tuples_y generator is exhausted building noun--feature co-occurrence frequency matrix, indexed by aforementioned noun2i and feature2i indices

                print(f"\tbuild indices wrt., role")
                nouns = set([])
                features = set([])
                for tup in tuples_x:
                    # only collect nouns where feature present
                    if tup[2] == role:
                        nouns.add(tup[0])
                        features.add(tup[1])
                noun2i = {x: i for i, x in enumerate(nouns)}
                feature2j = {x: j for j, x in enumerate(features)}
                print(f"role:{role}, {len(nouns)} nouns, {len(features)} features")

                print(f"\tbuild frequency matrix wrt., role")
                F = lil_matrix((len(nouns), len(features)), dtype=int)
                for tup in tuples_y:
                    if tup[2] == role:
                        i = noun2i[tup[0]]
                        j = feature2j[tup[1]]
                        F[i, j] += 1
                F = csr_matrix(F)
                # thus all features have at least one coincident noun, and all nouns have at least one coincident features
                # that is, all rows and column have at least one entry

                print(f"\tbuild a LLR scores, for a total of {len(nouns)} nouns")
                L = lil_matrix(F.shape, dtype=float)
                llr_profiles = process_map(
                    get_llr_profile_star, zip(range(F.shape[0]), cycle([F])), chunksize=1000
                )  # a list of rows of L
                print(f"\t\tassemble L by calculated rows")
                for row_i, llr_profile in tqdm(enumerate(llr_profiles)):
                    L[row_i, :] = llr_profile
                print(f"\t\t convert lil_matrix to csr_matrix")
                L = csr_matrix(L)

                # save 
                print("save noun2i, feature2i, F, L")
                save_dir = output_dir / role
                save_dir.mkdir(parents=True, exist_ok=True)

                with open(save_dir / "noun2i.json", "w", encoding="utf-8") as f:
                    json.dump(noun2i, f)

                with open(save_dir / "feature2i.json", "w", encoding="utf-8") as f:
                    json.dump(feature2j, f)

                save_npz(save_dir / "freq_profiles.npz", F)
                save_npz(save_dir / "llr_profiles.npz", L)


def log_binom(k: np.ndarray, n: float, p: np.ndarray) -> np.ndarray:

    result = np.zeros(len(k))
    # Note: @p==1, log(p) = 0: hence handled implicity

    # where p > 0 and p < 1
    mask = (p > 0) & (p < 1)
    result[mask] = k[mask] * np.log(p[mask]) + (n - k[mask]) * np.log(1 - p[mask])

    return result


def get_llr_profile_star(t):
    return get_llr_profile(*t)


def get_llr_profile(row_i, F) -> np.ndarray:
    """Build a llr profile for row_i
    where row_i is the study corpus and row_i' is the ref corpus.
    """

    # get the study corpus and ref_corpus
    study = F[row_i, :].toarray().squeeze()  # i.e., feature freqs wrt., noun
    global_profile = np.array(F.sum(axis=0)).squeeze()
    ref = (
        global_profile - study
    )  # feature freqs aggregated over all nouns except (excl. study results)

    # build llr profile
    llr_profile = np.zeros(len(study))

    n1 = study.sum()
    n2 = ref.sum()
    n = n1 + n2

    study_mle = study / n1  # i.e., list of P(feature_i | study)
    ref_mle = ref / n2  # i.e, list of P(feature_i | ref)
    p = (study + ref) / n  # combined mle, i.e., P(feature_i | study & ref) 

    # LLR = -2*log(lambda) ; lambda = L(null) / L(alt)
    #   lambda is the relative likelihood of 2 generative assumptions: 
    #       * the null assumpion: that both the study and reference are generative distributions are generated according to the combined MLE probabilties
    #       * the alternative assumption: that the study and reference are generated according to the their own MLE feature probabilities
    #       * thus, a more positive LLR means L(alt) > L(null). The net affect that the ( noun, feature ) of the study are disproportionately associated

    # i.e., where study = 0, make the result 0, as the entry is irrelevant to study
    mask = study > 0
    llr_profile[mask] = 2 * (
        # alt
        log_binom(study[mask], n1, study_mle[mask])
        + log_binom(ref[mask], n2, ref_mle[mask])
        # null
        - log_binom(study[mask], n1, p[mask])
        - log_binom(ref[mask], n2, p[mask])
    )

    return lil_matrix(llr_profile)


def gen_tuples(fps) -> typing.Generator:
    """Return a generator of e.g., ['man', 'medium-sized', 'adj', 'A_h', filename] objects"""

    for fp in fps:

        with open(fp, "r", encoding="utf-8") as f:
            doc = json.load(f)

        for i, tuples in enumerate(doc, start=1):
            if i % 2 == 0:
                for tup in tuples:
                    yield list(tup) + [fp.name]


if __name__ == "__main__":
    main()
