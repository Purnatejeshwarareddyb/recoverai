"""ML model hyperparameters and decision thresholds, kept separate from
settings.py so they can be tuned without touching path/data config."""

LOGISTIC_REGRESSION_PARAMS = {
    "max_iter": 5000,
    "C": 1.0,
}

RANDOM_FOREST_PARAMS = {
    "n_estimators": 200,
    "max_depth": 8,
    "min_samples_leaf": 5,
}

# Classification threshold used when a hard yes/no recoverability label
# is needed (e.g. for the confusion matrix). The dashboard mostly uses
# the raw probability instead of this cutoff.
CLASSIFICATION_THRESHOLD = 0.5

TRAIN_TEST_SPLIT = 0.25
