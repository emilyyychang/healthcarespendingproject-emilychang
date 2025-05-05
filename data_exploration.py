import pandas as pd 
filtered_df = pd.read_csv("original_datasets/filtered_expenditure.csv")
unfiltered_df = pd.read_csv("original_datasets/unfiltered_expenditure.csv")

def explore_data (df):
   print("country value counts\n",df['Reference area'].value_counts())
   print("\nyear value counts\n",df['TIME_PERIOD'].value_counts())
   print("\nlength of dataframe\n",len(df))

explore_data(filtered_df)
explore_data(unfiltered_df)



