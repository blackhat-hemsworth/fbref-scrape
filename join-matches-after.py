import pandas as pd
import re
import numpy as np

matches_df = pd.read_csv("output/matches.csv").set_index("Date")
col_cleaner = np.vectorize(lambda x: re.sub(".3$","_long",
                                            re.sub(".2$","_medium",
                                                   re.sub(".1$","_short",x))
                                            )
                          )
matches_df.columns = col_cleaner(matches_df.columns.values)

home = matches_df[matches_df.Venue=="Home"]
away = matches_df[matches_df.Venue=="Away"]
print(home.shape, away.shape)
matches_wide_df = home.join(away,how="left",lsuffix="_home",rsuffix="_away")
matches_wide_df.to_csv("output/matches_wide.csv")