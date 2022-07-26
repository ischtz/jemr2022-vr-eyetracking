# Data import and analysis functions, to not clutter notebooks

import os
import glob
import json
import pickle
import hashlib 

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from palettable.colorbrewer.qualitative import Set1_9, Set3_12, Set2_8, Paired_12

from helpers import *

# Import a patched version of the Vizard experiment toolbox for analysis
# besides metrics computation, this one includes repeated samples etc.
import vexptoolbox as vx

HASH_SALT = 'khiwpa67SzHoSUE'
PPID_COLORS = np.vstack([Paired_12.mpl_colors, Set1_9.mpl_colors, Set3_12.mpl_colors])


def read_json_data(folder, show_progress=True, samples_range=(25, 115), exclude_acc=None):
    """ Reads a folder full of ValidationResult JSON files into DataFrames

    Args:
        folder (str): folder containing files to parse, or list of folders
        show_progress (bool): if True, print file names as they are read
        samples_range (tuple): start and end sample for metric computation
    """
    agg_data = []
    tar_data = []
    sam_data = []

    if type(folder) == str:
        jfiles = glob.glob(os.path.join(folder, '*.json'))
    elif type(folder) == list:
        jfiles = []
        for ff in folder:
            jfiles.extend(glob.glob(os.path.join(ff, '*.json')))
    uids = {}
    uid_idx = 1

    print('Importing JSON experiment data files...')
    for jf in jfiles:
        with open(jf, 'r') as f:
            json_data = json.load(f)

            meta = json_data['metadata']

            # Create a unique user hash from HASH_SALT + lab + partID
            uid_str = (HASH_SALT + str(meta['lab']) + str(meta['part_id'])).encode('utf-8')
            uid = hashlib.sha1(uid_str).hexdigest()
            if uid not in uids.keys():
                uids[uid] = uid_idx
                uid_idx += 1

            # Create a random instance ID for this dataset
            vid_str = (HASH_SALT + str(meta['lab']) + 
                       str(meta['part_id']) + str(meta['datetime'])).encode('utf-8')
            val_id = hashlib.sha1(vid_str).hexdigest()

            # Create new data frame dict
            d ={'uid': uid,
                'user': meta['part_id'],
                'session': meta['session'],
                'val_id': val_id}

            # Summary: Add metadata
            m_keys = ['engine', 'eye_tracker', 'prescriptionR', 'gender', 'age', 'engine_version', 'platform', 
                      'version', 'prescriptionL', 'datetime', 'vision']
            for k in m_keys:
                d[k] = meta[k]

            # Summary: Add validation summary data
            v_keys = ['rmsi', 'ipd', 'rmsiX_R', 'sd_R', 'accX_R', 'rmsi_R', 'sdY_R', 'accY', 'accX', 'sdY_L', 'rmsi_L', 'sdX_L', 
                      'sdX_R', 'rmsiX', 'rmsiY', 'acc', 'rmsiY_L', 'rmsiX_L', 'accY_L', 'acc_L', 'sdX', 'sdY', 'accX_L', 'sd_L', 
                      'acc_R', 'accY_R', 'rmsiY_R', 'sd', 'start_sample', 'end_sample', 
                      'repeated', 'repeated_C', 'repeated_L', 'repeated_R', 'repeated_any']
            for k in v_keys:
                if k in json_data.keys(): # Some values not always present, e.g. monocular data
                    d['{:s}_json'.format(k)] = json_data[k]

            vr = vx.ValidationResult(samples=json_data['samples'], targets=json_data['targets'], metadata=meta)

            # All targets as-is
            agg_all = vr.recomputeMetrics(agg_fun=np.mean, 
                                          start_sample=samples_range[0],
                                          end_sample=samples_range[1])
            
            # All targets with outlier correction at 5 deg
            agg_all_valid = vr.recomputeMetrics(agg_fun=np.mean,
                                          start_sample=samples_range[0],
                                          end_sample=samples_range[1],
                                          exclude_acc=5.0)

            # These weren't used in the manuscript but are kept commented out here
            # for verification that removing sampling errors did not change results.
            
            # # All targets with outlier correction at 5 deg, skipping one eye missing
            # agg_valid_samp = vr.recomputeMetrics(agg_fun=np.mean,
            #                                          start_sample=samples_range[0],
            #                                          end_sample=samples_range[1],
            #                                          exclude_acc=5.0,
            #                                          skip_missing_eye=True)

            # # All targets with outlier correction at 5 deg, skipping one eye missing and sampling errors
            # agg_skip_nosamp = vr.recomputeMetrics(agg_fun=np.mean,
            #                                          start_sample=samples_range[0],
            #                                          end_sample=samples_range[1],
            #                                          exclude_acc=5.0,
            #                                          skip_missing_eye=True,
            #                                          skip_sample_repeats=True)

            # Inner 20 deg targets only (Vive Pro specs)
            agg_inner = vr.recomputeMetrics(agg_fun=np.mean,
                                            start_sample=samples_range[0],
                                            end_sample=samples_range[1],
                                            tar_x_range=10,
                                            tar_y_range=10)

            for k in v_keys:
                if k in agg_all.results.keys():
                    d['{:s}'.format(k)] = agg_all.results[k]
                if k in agg_all_valid.results.keys():
                    d['{:s}_valid'.format(k)] = agg_all_valid.results[k]
                if k in agg_inner.results.keys():
                    d['{:s}_i10'.format(k)] = agg_inner.results[k]
                #if k in agg_valid_samp.results.keys():
                #    d['{:s}_nomonoc'.format(k)] = agg_valid_samp.results[k]
                #if k in agg_skip_nosamp.results.keys():
                #    d['{:s}_nosamp'.format(k)] = agg_skip_weird.results[k]

            # Summary: Add target information
            d['num_targets'] = len(json_data['targets'])
            agg_data.append(d)

            # Samples: add database keys, convert to DF
            for sd in agg_all.samples:
                s_df = pd.DataFrame(sd)
                s_df.loc[:, 'val_id'] = val_id
                s_df.loc[:, 'uid'] = uid
                s_df.loc[:, 'user'] = meta['part_id']
                sam_data.append(s_df)

            # Targets: Add by-target results
            for tar in agg_all.targets:
                t ={'uid': uid,
                    'user': meta['part_id'],
                    'session': meta['session'],
                    'val_id': val_id}
                t.update(tar)
                tar_data.append(t)

        if show_progress:
            print(jf)
    print('Done importing.')

    return(pd.DataFrame(agg_data), 
           pd.DataFrame(tar_data),
           sam_data)


def load_pickle_data(folder):
    """ Load pickled preprocessed data """
    with open(os.path.join(folder, 'gaze_targets.pkl'), 'rb') as f:
        tar = pickle.load(f)
    with open(os.path.join(folder, 'gaze_targets_i10.pkl'), 'rb') as f:
        tar_i10 = pickle.load(f)
    with open(os.path.join(folder, 'gaze_validations.pkl'), 'rb') as f:
        val = pickle.load(f)
    with open(os.path.join(folder, 'participants.pkl'), 'rb') as f:
        pp = pickle.load(f)
    with open(os.path.join(folder, 'gaze_samples.pkl'), 'rb') as f:
        sam = pickle.load(f)
    #with open(os.path.join(folder, 'gaze_targets_nosamperr.pkl'), 'rb') as f:
    #    tar_samp = pickle.load(f)

    print('Data loaded from pickles.')
    #return (tar, tar_i10, val, pp, sam, tar_samp)
    return (tar, tar_i10, val, pp, sam)
