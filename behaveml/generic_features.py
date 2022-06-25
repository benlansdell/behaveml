""" Functions to take pose tracks and compute a set of features from them """

import pandas as pd
import numpy as np

# * More generic feature creation functions, for general models, not just MARS featureset
#   - [x] Intra-body part distances
#   - [x] Intra-body part velocities 
#   - [x] Center of mass location
#   - [x] Center of mass velocity
#   - [x] Inter-animal velocities (of all body parts)
#   - [x] Inter-animal velocities (center of mass)
#   - [x] Inter-animal distances (of all body parts)
#   - [x] Inter-animal distances (center of mass)
#   - [ ] Intra-animal angles (of all body parts)

############################

def compute_centerofmass_interanimal_distances(df : pd.DataFrame, raw_col_names : list, animal_setup : dict, **kwargs) -> pd.DataFrame:

    bodypart_ids = animal_setup['bodypart_ids']
    mouse_ids = animal_setup['mouse_ids']

    features_df = df.copy()

    for animal_id in mouse_ids:
        fxs = ['_'.join([animal_id, 'x', bp]) for bp in bodypart_ids]
        fys = ['_'.join([animal_id, 'y', bp]) for bp in bodypart_ids]
        fx_new = '_'.join([animal_id, 'COM_x'])
        fy_new = '_'.join([animal_id, 'COM_y'])
        features_df[fx_new] = features_df[fxs].sum(axis = 1) / len(bodypart_ids)
        features_df[fy_new] = features_df[fys].sum(axis = 1) / len(bodypart_ids)

    orig_cols = features_df.columns

    for i, animal_i in enumerate(mouse_ids):
        fx_i = '_'.join([animal_i, 'COM_x'])
        fy_i = '_'.join([animal_i, 'COM_y'])
        for j, animal_j in enumerate(mouse_ids[:i]):
            fx_j = '_'.join([animal_j, 'COM_x'])
            fy_j = '_'.join([animal_j, 'COM_y'])
            f_new = '_'.join([animal_i, animal_j, 'COM_distance'])
            features_df[f_new] = np.sqrt((features_df[fx_i] - features_df[fx_j])**2 \
                                         + (features_df[fy_i] - features_df[fy_j])**2)

    features_df = features_df.drop(columns = orig_cols)
    return features_df

def compute_centerofmass_interanimal_speed(df : pd.DataFrame, raw_col_names : list, animal_setup : dict, n_shifts = 5, **kwargs) -> pd.DataFrame:

    bodypart_ids = animal_setup['bodypart_ids']
    mouse_ids = animal_setup['mouse_ids']

    features_df = df.copy()

    dt = features_df['time'].diff(periods = n_shifts)

    for animal_id in mouse_ids:
        fxs = ['_'.join([animal_id, 'x', bp]) for bp in bodypart_ids]
        fys = ['_'.join([animal_id, 'y', bp]) for bp in bodypart_ids]
        fx_new = '_'.join([animal_id, 'COM_x'])
        fy_new = '_'.join([animal_id, 'COM_y'])
        features_df[fx_new] = features_df[fxs].sum(axis = 1) / len(bodypart_ids)
        features_df[fy_new] = features_df[fys].sum(axis = 1) / len(bodypart_ids)
        features_df[fx_new] = features_df[fx_new].diff(periods = n_shifts)/dt
        features_df[fy_new] = features_df[fx_new].diff(periods = n_shifts)/dt

    orig_cols = features_df.columns

    for i, animal_i in enumerate(mouse_ids):
        fx_i = '_'.join([animal_i, 'COM_x'])
        fy_i = '_'.join([animal_i, 'COM_y'])
        for j, animal_j in enumerate(mouse_ids[:i]):
            fx_j = '_'.join([animal_j, 'COM_x'])
            fy_j = '_'.join([animal_j, 'COM_y'])
            f_new = '_'.join([animal_i, animal_j, 'COM_speed'])
            features_df[f_new] = np.sqrt((features_df[fx_i] - features_df[fx_j])**2 \
                                         + (features_df[fy_i] - features_df[fy_j])**2)
            features_df[f_new] = features_df[f_new].diff(periods = n_shifts)/dt

    features_df = features_df.drop(columns = orig_cols)
    return features_df

def compute_centerofmass(df : pd.DataFrame, raw_col_names : list, animal_setup : dict, **kwargs) -> pd.DataFrame:

    bodypart_ids = animal_setup['bodypart_ids']
    mouse_ids = animal_setup['mouse_ids']

    features_df = df.copy()
    orig_cols = df.columns

    for animal_id in mouse_ids:
        fxs = ['_'.join([animal_id, 'x', bp]) for bp in bodypart_ids]
        fys = ['_'.join([animal_id, 'y', bp]) for bp in bodypart_ids]
        fx_new = '_'.join([animal_id, 'COM_x'])
        fy_new = '_'.join([animal_id, 'COM_y'])
        features_df[fx_new] = features_df[fxs].sum(axis = 1) / len(bodypart_ids)
        features_df[fy_new] = features_df[fys].sum(axis = 1) / len(bodypart_ids)

    features_df = features_df.drop(columns = orig_cols)
    return features_df

############################

def compute_centerofmass_velocity(df : pd.DataFrame, raw_col_names : list, animal_setup : dict, n_shifts = 5, **kwargs) -> pd.DataFrame:

    bodypart_ids = animal_setup['bodypart_ids']
    mouse_ids = animal_setup['mouse_ids']

    features_df = df.copy()
    orig_cols = df.columns

    dt = features_df['time'].diff(periods = n_shifts)

    for animal_id in mouse_ids:
        fxs = ['_'.join([animal_id, 'x', bp]) for bp in bodypart_ids]
        fys = ['_'.join([animal_id, 'y', bp]) for bp in bodypart_ids]
        fx_new = '_'.join([animal_id, 'COM_vel_x'])
        fy_new = '_'.join([animal_id, 'COM_vel_y'])
        features_df[fx_new] = features_df[fxs].sum(axis = 1) / len(bodypart_ids)
        features_df[fy_new] = features_df[fys].sum(axis = 1) / len(bodypart_ids)
        features_df[fx_new] = features_df[fx_new].diff(periods = n_shifts)/dt
        features_df[fy_new] = features_df[fx_new].diff(periods = n_shifts)/dt

    features_df = features_df.drop(columns = orig_cols)
    return features_df

def compute_centerofmass(df : pd.DataFrame, raw_col_names : list, animal_setup : dict, **kwargs) -> pd.DataFrame:

    bodypart_ids = animal_setup['bodypart_ids']
    mouse_ids = animal_setup['mouse_ids']

    features_df = df.copy()
    orig_cols = df.columns

    for animal_id in mouse_ids:
        fxs = ['_'.join([animal_id, 'x', bp]) for bp in bodypart_ids]
        fys = ['_'.join([animal_id, 'y', bp]) for bp in bodypart_ids]
        fx_new = '_'.join([animal_id, 'COM_x'])
        fy_new = '_'.join([animal_id, 'COM_y'])
        features_df[fx_new] = features_df[fxs].sum(axis = 1) / len(bodypart_ids)
        features_df[fy_new] = features_df[fys].sum(axis = 1) / len(bodypart_ids)

    features_df = features_df.drop(columns = orig_cols)
    return features_df

def compute_speed_features(df : pd.DataFrame, raw_col_names : list, animal_setup : dict, n_shifts = 5, **kwargs) -> pd.DataFrame:

    bodypart_ids = animal_setup['bodypart_ids']
    mouse_ids = animal_setup['mouse_ids']

    features_df = df.copy()
    orig_cols = df.columns

    dt = features_df['time'].diff(periods = n_shifts)

    ##Make the distance features
    for i, bp1 in enumerate(bodypart_ids):
        for j, bp2 in enumerate(bodypart_ids):
            if i < j:
                for mouse_id in mouse_ids:
                    #We can compute the intra-mouse difference
                    f1x = '_'.join([mouse_id, 'x', bp1])
                    f2x = '_'.join([mouse_id, 'x', bp2])
                    f1y = '_'.join([mouse_id, 'y', bp1])
                    f2y = '_'.join([mouse_id, 'y', bp2])
                    f_new = '_'.join([mouse_id, 'speed', bp1, bp2])
                    features_df[f_new] = \
                        np.sqrt((features_df[f1x].diff(periods = n_shifts) - features_df[f2x].diff(periods = n_shifts))**2 + 
                                (features_df[f1y].diff(periods = n_shifts) - features_df[f2y].diff(periods = n_shifts))**2)/dt

            #Inter-mouse difference
            for animal_i in range(len(mouse_ids)):
                for animal_j in range(animal_i):
                    f1x = '_'.join([mouse_ids[animal_i], 'x', bp1])
                    f2x = '_'.join([mouse_ids[animal_j], 'x', bp2])
                    f1y = '_'.join([mouse_ids[animal_i], 'y', bp1])
                    f2y = '_'.join([mouse_ids[animal_j], 'y', bp2])
                    f_new = '_'.join([f'M{animal_i}_M{animal_j}', 'speed', bp1, bp2])
                    features_df[f_new] = \
                                np.sqrt((features_df[f1x].diff(periods = n_shifts) - features_df[f2x].diff(periods = n_shifts))**2 + 
                                        (features_df[f1y].diff(periods = n_shifts) - features_df[f2y].diff(periods = n_shifts))**2)/dt

    #Remove base features
    features_df = features_df.drop(columns = orig_cols)

    return features_df

def compute_distance_features(df : pd.DataFrame, raw_col_names : list, animal_setup : dict, **kwargs) -> pd.DataFrame:

    bodypart_ids = animal_setup['bodypart_ids']
    mouse_ids = animal_setup['mouse_ids']

    features_df = df.copy()
    orig_cols = df.columns

    ##Make the distance features
    for i, bp1 in enumerate(bodypart_ids):
        for j, bp2 in enumerate(bodypart_ids):
            if i < j:
                for mouse_id in mouse_ids:
                    #We can compute the intra-mouse difference
                    f1x = '_'.join([mouse_id, 'x', bp1])
                    f2x = '_'.join([mouse_id, 'x', bp2])
                    f1y = '_'.join([mouse_id, 'y', bp1])
                    f2y = '_'.join([mouse_id, 'y', bp2])
                    f_new = '_'.join([mouse_id, 'distance', bp1, bp2])
                    features_df[f_new] = \
                        np.sqrt((features_df[f1x] - features_df[f2x])**2 + 
                                (features_df[f1y] - features_df[f2y])**2)

            #Inter-mouse difference
            for animal_i in range(len(mouse_ids)):
                for animal_j in range(animal_i):
                    f1x = '_'.join([mouse_ids[animal_i], 'x', bp1])
                    f2x = '_'.join([mouse_ids[animal_j], 'x', bp2])
                    f1y = '_'.join([mouse_ids[animal_i], 'y', bp1])
                    f2y = '_'.join([mouse_ids[animal_j], 'y', bp2])
                    f_new = '_'.join([f'M{animal_i}_M{animal_j}', 'distance', bp1, bp2])
                    features_df[f_new] = \
                                np.sqrt((features_df[f1x] - features_df[f2x])**2 + 
                                        (features_df[f1y] - features_df[f2y])**2)

    #Remove base features
    features_df = features_df.drop(columns = orig_cols)

    return features_df