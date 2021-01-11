import numpy as np
import pandas as pd
import math

import argparse

from scipy.stats import entropy

from collections import Counter

def compute_stats(blocks):
    results = pd.DataFrame(columns=["block_num","trial_num", "target", "kl_prev", "kl_target", "ent_p"])

    for block_num, target, dists in blocks:
        dists.sort(key = lambda x: x[0])

        p_prev = None

        for trial, dist in dists:
            dict = [x[0] for x in dist]
            idx_targ = dict.index(target)

            q_targ = np.array([0.]*len(dist))
            q_targ[idx_targ] = 1
            q_targ += 0.000001
            q_targ /= sum(q_targ)


            p_counts = [x[1] for x in dist]
            # print(sum(p_counts))
            p = np.array(p_counts)
            p = p + 0.000001
            p /= sum(p)


            kl_target = entropy(p, q_targ)
            kl_prev = entropy(p_prev, p) if p_prev is not None else "NA"
            ent_p = entropy(p)
            p_prev  = p

            results = results.append({
                "block_num": block_num,
                "trial_num": trial,
                "target": target,
                "kl_prev": kl_prev,
                "kl_target": kl_target,
                "ent_p": ent_p
            }, ignore_index=True)

    return results

def main(args):
    df = pd.read_csv(args.data)

    stats = pd.DataFrame()

    for bs, block_set in df.groupby("block_set"):
        blocks = []
        for b, block in block_set.groupby("block_id"):
            dict = list(filter(lambda x: type(x) == str, block.guess.unique()))
            dists = []
            for t, trial in block.groupby("trial_id"):
                dist = {x: 0 for x in dict}
                counts = Counter(trial.guess)
                for word, count in counts.items():
                    dist[word] = count

                dist = list(filter(lambda x: type(x[0]) == str, list(dist.items())))
                dist.sort(key=lambda x: x[0])
                dists.append((t, dist))
            blocks.append((b, block.iloc[0].target, dists))
        result = compute_stats(blocks)
        result['block_set'] = bs

        stats = stats.append(result, ignore_index=True)

    return stats



if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--data")

    args = parser.parse_args()

    results = main(args)

    results.to_csv("dist_change_exp202.csv", index=False)
