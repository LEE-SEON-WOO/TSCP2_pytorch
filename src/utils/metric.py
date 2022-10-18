
import numpy as np
from sklearn.metrics import confusion_matrix,f1_score
from matplotlib import pyplot as plt
import torch
from torch import cosine_similarity
import math

def estimate_CPs(sim:np.array, gt:np.array, path,
                metric='cosine', threshold=0.5):
    
    # if metric == "cosine":
    #     sim = cosine_similarity(sim, gt, dim=1)

    est_cp = np.zeros(sim.shape)
    est_cp = np.where(sim<threshold, 1, 0)
    
    gt = gt.astype(np.uint8)
    sim = sim.astype(np.uint8)
    tn, fp, fn, tp = confusion_matrix(gt, est_cp).ravel()
    f1 = f1_score(gt, est_cp)

    ## gt==1
    gt_id = np.where(gt == 1)[0]
    
    plt.figure(figsize=(15, 7))
    plt.subplot(2, 1, 1)
    for i in gt_id:
        plt.axvline(x=i, ymin=0, ymax=1, color='k')
    plt.subplot(2, 1, 2)
    for i in np.where(est_cp == 1)[0]:
        plt.axvline(x=i, ymin=0, ymax=1, color='r')
    plt.savefig(path)
    
    print("tn {}, fp {}, fn {}, tp {} ----- f1-score {}".format(tn, fp, fn, tp, f1))
    ## continuous series
    i = 1
    pos, seq_tp, seq_fn, seq_fp = 0, 0, 0, 0

    while i < gt.shape[0]:
        if gt[i] == 1:
            pos += 1
            j = i
            while gt[i] == 1:
                i += 1

            if np.sum(est_cp[j:i]) > 0:
                seq_tp += 1
                est_cp[j:i] = 0
            else:
                seq_fn += 1

        i += 1
    
    seq_fp = np.where(np.diff(est_cp) == 1)[0].shape[0] #1-th discrete difference
    seq_f1 = (2 * seq_tp) / ((2 * seq_tp + seq_fn + seq_fp))

    print("SEQ : Pos {}, fp {}, fn {}, tp {} ----- f1-score {}".format(pos, seq_fp, seq_fn, seq_tp, seq_f1))
    result = "tn, {}, fp, {}, fn, {}, tp, {}, f1-score, {}, Pos, {}, seqfp, {}, seqfn, {}, seqtp, {}, seqf1, {}\n".format(tn, fp, fn, tp, f1, pos, seq_fp, seq_fn, seq_tp, seq_f1)
    return result