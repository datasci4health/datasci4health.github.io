# UCI Heart Disease Data Set
*lab 15/04/2021*

Original [Heart Disease Data Set](https://archive.ics.uci.edu/ml/datasets/heart+Disease) at UCI Machine Learning Repository.

## Kaggle Adapted Version

This task takes the [Kaggle Version of  Heart Disease UCI](https://www.kaggle.com/ronitf/heart-disease-uci) as the basis to produce artificial missing values.

The original data is in folder `raw` and artificially generated missing data are in folder `processed`. There are three files, each one misses data in one field: age, serum cholestoral, and sex.

## Task

You must try to classify the type of missing data among:
* MCAR - Missing Completely at Random
* MNAR - Missing not at Random
* MAR - Missing at Random

You must model a solution to inpute data, which you consider the best, for each dataset. The solution must be implemented in Orange or a Notebook.
