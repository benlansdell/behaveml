[![codecov](https://codecov.io/gh/benlansdell/behaveml/branch/master/graph/badge.svg?token=PN52Q3UH3G)](https://codecov.io/gh/benlansdell/behaveml)

# BehaveML

Supervised learning for animal behavior.

Interprets pose-tracking files (currently only from DLC), behavior annotations (currently only from BORIS) to train a behavior classifier. 

## Installation

```
pip install behaveml
```

### Advantages

* Can import data from a range of sources
* Comes with some general data processing methods, e.g. can filter DLC tracks and interpolate at low-confidence points
* More general than SimBA and MABE
* Lightweight, no GUI... just use in jupyter notebook. Or can be put into a fully automated pipeline this way
 and be given to experimentalists. Train them to use DLC, BORIS and then run the script/notebook to do behavior classification
* For some problems (mouse tracking), good baseline performance 
* Extensible, add your own features;
* And try your own ML models or use good baselines
* Active learning... train classifier on one video, inference on the rest, and suggest chunks of 
