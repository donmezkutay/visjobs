import pandas as pd
import numpy as np
from visjobs.datas import get_GHCN as ghc

#Show available station IDs for TURKEY
ghc.get_turkey_ID()

#Get the GHCN data for Station ID indicated below
#Returns pandas Dataframe
dt = ghc.get_data_with_station('TUM00017064')