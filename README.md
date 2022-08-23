# Eye Tracking in Virtual Reality: Vive Pro Eye Spatial Accuracy, Precision, and Calibration Reliability (JEMR, 2022)


This repository contains the experiment code, data, and analysis for our manuscript accepted in the *Journal of Eye Movement Research* (2022). 

## Experiment Code

The experiment was implemented in Python using WorldViz Vizard and [our *vexptoolbox* software toolbox](https://github.com/ischtz/vizard-experiment-toolbox) designed to aid in developing behavioral experiments on the Vizard platform. It can be run by opening *gaze_evaluation.py* within Vizard and pressing F5 or clicking the *Run* button. Currently, only the Vive Pro Eye built-in eye tracker is fully supported, but there is limited support for the Pupil Labs HTC Vive Add-On and the code can also be run without an eye tracker or VR headset connected. 

The experiment calibrates the chosen eye tracker, then presents 74 head-locked target positions across two distances (6 m and 0.5 m), spanning a range of +/- 15 degrees at 6 m and +/- 10 degrees at 0.5 m. After all targets have been displayed, a JSON file with raw gaze angle data and computed metrics is output (see below).


## Summary of Results

We found that participants (N=18) could be calibrated reliably, including those wearing contact lenses or glasses (*left figure*). On average, participants achieved a spatial accuracy of 1.1°, with higher accuracy (lower angular error) for more central compared to peripheral targets (*right figure*). 

![figure5_small](https://user-images.githubusercontent.com/7711674/186172277-9f3b5201-9fa4-4243-b995-f3e047429d14.png) ![figure4_small](https://user-images.githubusercontent.com/7711674/186172296-a814b13d-bac8-4bc1-9c6a-71e0e63c4e78.png)

Please refer to the paper for detailed results, where we also statistically evaluate the effect of vision correction (contact lenses, glasses, or no correction) and estimate participants' inter-pupillary distance using the pupil positions detected by the eye tracker. 


## Data Format




## Citation

If you use any data or code from this repository, please cite the corresponding manuscript (Link will be added here after publication): 

*Schuetz, I. & Fiehler, K. (2022). Eye Tracking in Virtual Reality: Vive Pro Eye Spatial Accuracy, Precision, and Calibration Reliability. Journal of Eye Movement Research, 15(3):3. https://doi.org/10.16910/jemr.15.3.3*

Citation in BibTeX format:
```
@Article{Schuetz2022JEMR,
  author       = {Schuetz, I. and Fiehler, K.},
  journal      = {Journal of Eye Movement Research},
  title        = {Eye Tracking in Virtual Reality: Vive Pro Eye Spatial Accuracy, Precision, and Calibration Reliability},
  year         = {2022},
  issn         = {1995-8692},
  number       = {3},
  pages        = {3},
  volume       = {15},
  doi          = {10.16910/jemr.15.3.3}
}
```


