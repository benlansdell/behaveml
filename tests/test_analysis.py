#####################
## Setup test code ##
#####################

import pytest

from behaveml import VideosetDataFrame, clone_metadata

#Metadata is a dictionary
def test_clone_metadata(tracking_files, label_files, metadata_params):
    """ Test creation of metadata object """

    metadata = clone_metadata(tracking_files, 
                                label_files = label_files, 
                                frame_length = metadata_params['frame_length'], 
                                fps = metadata_params['fps'], 
                                units = metadata_params['units'], 
                                resolution = metadata_params['resolution'])

    assert len(metadata) == 5
    assert metadata[list(metadata.keys())[0]]['fps'] == metadata_params['fps']



def test_VideoDataFrame(tracking_files, label_files, metadata, metadata_params):
    """ Test creation of VideoDataFrame object """
    # metadata = clone_metadata(tracking_files, 
    #                             label_files = label_files, 
    #                             frame_length = metadata_params['frame_length'], 
    #                             fps = metadata_params['fps'], 
    #                             units = metadata_params['units'], 
    #                             resolution = metadata_params['resolution'])

    #Eventually, check we can make it without error
    try: df = VideosetDataFrame(metadata)
    except: assert False, "Failed to make VideosetDataFrame object"

    try: df = VideosetDataFrame({})
    except: assert False, "Failed to make empty VideosetDataFrame object"

    metadata_no_labels = clone_metadata(tracking_files, 
                                frame_length = metadata_params['frame_length'], 
                                fps = metadata_params['fps'], 
                                units = metadata_params['units'], 
                                resolution = metadata_params['resolution'])
                                
    try: df = VideosetDataFrame(metadata_no_labels)
    except: assert False, "Failed to make VideosetDataFrame object without labels"

    #Also check that improper formatted metadata raises the right exception

    #Check that 

def test_VideoDataFrame_object(videodataset):
    assert videodataset.feature_cols is None

def test_df_renaming(metadata, default_track_cols):
    none_renamer = {}
    df = VideosetDataFrame(metadata, part_renamer = none_renamer)
    df.feature_cols = df.raw_track_columns
    assert df.feature_cols == default_track_cols

    new_parts = ['nose', 'left_ear', 'right_ear', 'neck', 'lefthip', 'righthip', 'tail']
    part_renamer = {'leftear': 'left_ear', 'rightear': 'right_ear'}
    df = VideosetDataFrame(metadata, part_renamer = part_renamer)
    assert set(new_parts) == set(df.body_parts)

    new_animals = ['resident', 'intruder']
    animal_renamer = {'adult': 'resident', 'juvenile': 'intruder'}
    df = VideosetDataFrame(metadata, animal_renamer = animal_renamer)
    print(df.animals)
    assert set(new_animals) == set(df.animals)
