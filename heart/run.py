from heart.src.scripts.preparation import preprocessing
from heart.src.scripts.modelling import xgb_model

def run_model():
    preprocessing()
    xgb_model()
