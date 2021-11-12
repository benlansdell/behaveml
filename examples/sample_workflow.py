#######################
## General todo list ##
#######################

#TODO
# * Write a bunch of tests... make sure it's behaving as it should
# * Clean up the MARS code...
# * Rewrite stacking code in our new formalism... shouldn't need to use the MARS stacking code I wrote, 
#   idea is that things are cleaner for that sort of thing now
# * Make a cleaner feature creation interface? One that can support any animal config
# * Check row order is preserved by DL model. Otherwise it's useless
# * Better way of getting parameters to feature creation step...like frame width?
# * Add a way to enforce, for each feature creation function, that it has the columns it needs
#   Add a 'req columns' field somewhere. The names should matter
# * Add a column renamer -- say you labeled your columns differently in DLC, this will 
#   name them as expected by the 'req_columns' field for the features you want.
# * Get rid of warning messages when load CNN pre-trained parameters
# * Move read BORIS function to io.py
# * Make it so that raw tracking columns are not added as features by default
# * Add HMM on top of all this jazz
# * Add F1 optimizer on top of all this jazz
# * Add our DLC filtering code

# Also want to do some EDA and QC. So let's check:
# * Plots of the DLC tracks
# * Filtering options for the DLC tracks
# * Video of BORIS labels

#DONE


###########################
## Example analysis code ##
###########################

from glob import glob 
from behaveml import VideosetDataFrame, clone_metadata
from behaveml import compute_dl_probability_features, compute_mars_features

#A list of DLC tracking files
tracking_files = sorted(glob('./tests/data/dlc/*.csv'))

#A list of BORIS labeled files, ordered to correspond with DLC tracking file list
boris_files = sorted(glob('./tests/data/boris/*.csv'))

frame_length = None              # (float) length of entire horizontal shot
units = None                     # (str) units frame_length is given in
fps = 30                         # (int) frames per second
resolution = (1200, 1600)        # (tuple) HxW in pixels

#Metadata is a dictionary
metadata = clone_metadata(tracking_files, 
                          label_files = boris_files, 
                          frame_length = frame_length, 
                          fps = fps, 
                          units = units, 
                          resolution = resolution)

dataset = VideosetDataFrame(metadata)

#Now create features on this dataset
#By default this keras code will use CUDA. 
print("Calculating 1D CNN pretrained network features")
dataset.add_features(compute_dl_probability_features, 
                     featureset_name = '1dcnn', 
                     add_to_features = True)

print("Calculating MARS features")
dataset.add_features(compute_mars_features, 
                     featureset_name = 'MARS', 
                     add_to_features = True)

#Remove the raw DLC track features from our featureset for ML
dataset.remove_feature_cols(dataset.raw_track_columns)



####################
# Works up to here # 
####################

# dataset.add_features(compute_stacked_features, 
#                      featureset_name = 'stacked', 
#                      add_to_features = True)

#You can also make your own 'feature maker':
#The feature creation functions take:
# * Pandas data frame (dataset.data)
# * A list of column names that indicate which columns in the data frame 
#   the features will be computed from. For basic feature, this will be the 'raw' pose-tracking column names
#   For 'model stacking' models, this can be derivative column sets
# * A dictionary, animal_setup, that contains details about the animals in the experiment
# They return 
# * Pandas data frame with the new features, in the same order as input data

#dataset.add_features(create_custom_features, 
#                     featureset_name = 'custom', 
#                     add_to_feature_col = True)

#Now all the work of the package is done, more or less, and 
# we can do ML on this object in e.g. sklearn by using the following attributes:
# dataset.features #The feature matrix setup for learning w
# dataset.label    #The labels for supervision
# dataset.group    #Used for group-level cross validation 
#                   (by default, groups are set to filename, so this implements video-level CV)

splitter = GroupKFold(n_splits = dataset.n_videos)

######################
## Machine learning ##
######################

## Sample ML model
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from xgboost import XGBClassifier
from sklearn.model_selection import cross_val_predict, GroupKFold
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

model = RandomForestClassifier()
#model = XGBClassifier()
#model = LogisticRegression(solver = 'liblinear')
#model = KNeighborsClassifier(metric = 'manhattan')

print("Fitting ML model with LOO CV")
predictions = cross_val_predict(model, 
                                dataset.features, 
                                dataset.labels, 
                                groups = dataset.group, 
                                cv = splitter)
acc = accuracy_score(dataset.labels, predictions)
f1 = f1_score(dataset.labels, predictions)
pr = precision_score(dataset.labels, predictions)
re = recall_score(dataset.labels, predictions)
print("Acc", acc, "F1", f1, 'precision', pr, 'recall', re)

#Now we have our model we can make a video of its predictions

#It may be that the stacked models I haven't implemented yet are actually doing
#a lot of the work. This makes sense, because there really aren't many interaction
#frames for this thing to learn from in this dataset............
#XGB on top of the stacked model may be beneficial. On the other hand... the CNN should be doing that already. 
#Not sure why it isn't getting better performance. Perhaps it's just totally overfit... with the rest of the features
#could just try using the 1dCNN features

