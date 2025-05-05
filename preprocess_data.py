"""
This file is for cleaning, tidying, and analyzing the data. Here is where datasets
will be imported from original_datasets, then fixed up and saved into cleaned_datasets.
Here is where everyone will be writing code for their individual datasets.
"""

import pandas as pd
from analysis import analyze
from tidy import tidy


# ==================================================================================
# CALLING FUNCTIONS - comment out functions inside run() that you don't want to run
# ==================================================================================

def run():
    medical_tech_availability()
    healthcare_expenditure_worldbank()
    life_expectancy_worldbank()
    ICU_beds()
    health_expenditure_as_percent_of_gdp()
    set_healthcare_capita_outcomes()
    avoidable_mortality()
    hospital_stay_length()
    oecd_population()
    gdp_worldbank()

# =============================================
# FUNCTION DEFINITIONS - no need to comment out
# =============================================

def medical_tech_availability():
    read_file = "original_datasets/medical_tech_availability.csv"
    df = pd.read_csv(read_file)
    # most of these are duplicate short-version columns
    unnecessary_cols = [
        'STRUCTURE', 'STRUCTURE_ID', 'STRUCTURE_NAME', 'ACTION', 'MEASURE', 'UNIT_MEASURE',
        'STATISTICAL_OPERATION', 'OWNERSHIP_TYPE', 'HEALTH_FUNCTION', 'CARE_TYPE',
        'HEALTH_CARE_PROVIDER', 'Time period', 'Observation value', 'DECIMALS', 'Decimals',
        'OBS_STATUS', 'OBS_STATUS2', 'OBS_STATUS3', 'UNIT_MULT', 'REF_YEAR_PRICE'
    ]
    data_cols_rename_dict = {
        'OBS_VALUE': 'med_tech_availability_p_mil_ppl'
    }
    df_title = "medical_tech_availability"
    df = tidy(df, df_title,
              data_cols_rename_dict, drop_columns=unnecessary_cols)
    analyze(df, df_title)
    print("Dataframe:", df, sep="\n")


def healthcare_expenditure_worldbank():
    df = pd.read_csv("original_datasets/healthcare_expenditure_worldbank.csv")
    df = df.rename(columns=df.iloc[3]).iloc[4:]
    #drop columns not needed and only years from 2000 to 2019
    columns_to_keep = ['Country Name', 'Country Code'] + \
                  [col for col in df.columns if isinstance(col, float) and col >= 2000.0 and col<=2019]
    df_filtered = df[columns_to_keep]
    
    #change the orientation of the dataframe and add years as observations instead of variables
    df_long = pd.melt(df_filtered, 
                  id_vars=['Country Name', 'Country Code'], 
                  var_name='Year', 
                  value_name='Value')
    
    # convert 'year' column from float to integer
    df_long['Year'] = df_long['Year'].astype(int)
    # change column names
    df_long.columns = ['country', 'code', 'year', 'expenditure_per_capita']
    # sort df
    df_long = df_long.sort_values(['code', 'year'], ascending=[True, True])
    df_long = df_long.reset_index(drop=True)
    # save df
    df_long.to_csv("cleaned_datasets/healthcare_expenditure_worldbank.csv", index=False)


def life_expectancy_worldbank():
    df = pd.read_csv("original_datasets/life_expectancy.csv")
    df = df.rename(columns=df.iloc[3]).iloc[4:]
    #drop columns not needed and only years from 2000 to 2019
    columns_to_keep = ['Country Name', 'Country Code'] + \
                   [col for col in df.columns if isinstance(col, float) and col >= 2000.0 and col<=2019]
    df_filtered = df[columns_to_keep]
    
    #change the orientation of the dataframe and add years as observations instead of variables
    df_long = pd.melt(df_filtered,
                  id_vars=['Country Name', 'Country Code'],
                  var_name='Year',
                  value_name='Value')
    
    # convert 'year' column from float to integer
    df_long['Year'] = df_long['Year'].astype(int)
    # change column names
    df_long.columns = ['country', 'code', 'year', 'life_expectancy']
    # sort dataframe
    df_long = df_long.sort_values(['code', 'year'], ascending=[True, True])
    df_long = df_long.reset_index(drop=True)
    df = df_long
    df.to_csv('cleaned_datasets/life_expectancy.csv', index=False)
    df_title = 'life_expectancy'
    analyze(df, df_title)
    print("Dataframe:", df, sep="\n")
    

def ICU_beds():
    read_file = "original_datasets/ICU_beds.csv"
    df = pd.read_csv(read_file)
    # most of these are duplicate short-version columns
    unnecessary_cols = [
        'STRUCTURE', 'STRUCTURE_ID', 'STRUCTURE_NAME', 'ACTION', 'MEASURE', 'UNIT_MEASURE',
        'STATISTICAL_OPERATION', 'OWNERSHIP_TYPE', 'HEALTH_FUNCTION', 'CARE_TYPE', 'MEDICAL_TECH',
        'HEALTH_CARE_PROVIDER', 'Observation value', 'DECIMALS', 'Decimals',
        'OBS_STATUS', 'OBS_STATUS2', 'OBS_STATUS3', 'UNIT_MULT', 'REF_YEAR_PRICE'
    ]
    data_cols_rename_dict = {
        'OBS_VALUE': 'available_adult_ICU_beds'
    }
    df_title = "ICU_Beds_and_Use"
    df = tidy(df, df_title,
              data_cols_rename_dict, drop_columns=unnecessary_cols)
    analyze(df, df_title)
    print("Dataframe:", df, sep="\n")


def health_expenditure_as_percent_of_gdp():
    read_file = "original_datasets/filtered_health_expenditure_as_percent_gdp.csv"
    # cols 38 - 41 are NA for the first large chunk --> pandas must be told their type to not mix up types while reading in df in chunks to save memory
    df = pd.read_csv(read_file, dtype={i: object for i in range(38,42)})
    # most of these are duplicate short-version columns
    unnecessary_cols = [
        'STRUCTURE', 'STRUCTURE_ID', 'STRUCTURE_NAME', 'ACTION', 'MEASURE', 'UNIT_MEASURE', 'FREQ',
        'FINANCING_SCHEME', 'PRICE_BASE', 'CURRENCY', 'BASE_PER', 'FUNCTION', 'MODE_PROVISION',
        'FACTOR_PROVISION', 'ASSET_TYPE', 'Time period', 'Observation value', 'DECIMALS',
        'Decimals', 'OBS_STATUS', 'OBS_STATUS2', 'OBS_STATUS3', 'Unit multiplier', 'UNIT_MULT',
        'MODE_PROVISION'
    ]
    data_cols_rename_dict = {
        'OBS_VALUE': 'health_expenditure_as_percent_gdp'
    }
    df_title = "filtered_health_expenditure_as_percent_gdp"
    country_col = "Reference area"
    
    # tidy and analyze dataframe
    df = tidy(df, df_title, data_cols_rename_dict, og_country_column=country_col,
              og_year_column="TIME_PERIOD", drop_columns=unnecessary_cols)
    analyze(df, df_title)
    print("Dataframe:", df, sep="\n")


def set_healthcare_capita_outcomes():
    read_file = "original_datasets/unfiltered_set_healthcare_capita_outcomes.csv"
    # cols 34,35 are NA for the first large chunk --> pandas must be told their type to not mix up types while reading in df in chunks to save memory
    df = pd.read_csv(read_file, dtype={34:object, 35:object})
    data_cols_rename_dict = {'OBS_VALUE': 'set_healtchare_capita_outcomes',
                              'BASE_PER': 'base_period'}
    df_title = "unfiltered_set_healthcare_capita_outcomes"
    # all nonspecified tidy parameters are the same as the defualts
    df = tidy(df, df_title=df_title, new_data_cols_map=data_cols_rename_dict)
    # drop all rows where base_period isn't NA, then drop base period column
    # this is fine to do because base_period rows have corresponding duplicates without base_period
    df = df[df['base_period'].isna()].reset_index(drop=True).drop(columns=['base_period'])
    df.to_csv('cleaned_datasets/unfiltered_set_healthcare_capita_outcomes.csv', index=False)
    analyze(df, df_title)
    print(df)


def avoidable_mortality():
    read_file = "original_datasets/avoidable_mortality.csv"
    df = pd.read_csv(read_file)
    df_title = "avoidable_mortality"
    unnecessary_cols = ["STRUCTURE", "STRUCTURE_ID", "STRUCTURE_NAME", "ACTION", "FREQ", "MEASURE",
                        "UNIT_MEASURE", "Time period", "Observation value", "UNIT_MULT",
                        "DECIMALS", "Decimals", "AGE", "SOCIO_ECON_STATUS", "DEATH_CAUSE",
                        "CALC_METHODOLOGY", "GESTATION_THRESHOLD", "HEALTH_STATUS", "DISEASE",
                        "CANCER_SITE", "Observation value", "OBS_STATUS2", "SEX",
                        "OBS_STATUS3"]
    new_data_cols_rename_dict = {
        "OBS_VALUE": "avoidable_deaths"
    }
    df = tidy(df, df_title=df_title, new_data_cols_map=new_data_cols_rename_dict,
              drop_columns=unnecessary_cols)
    analyze(df, df_title)
    print(df)


def hospital_stay_length():
    df = pd.read_csv("original_datasets/hospital_stay_length.csv")
    df_title = "hospital_stay_length"
    unnecessary_cols = ["STRUCTURE", "STRUCTURE_ID", "STRUCTURE_NAME", "ACTION", "MEASURE",
                        "UNIT_MEASURE", "Time period", "Observation value", "UNIT_MULT",
                        "DECIMALS", "Decimals", "AGE", "DISEASE", "DIAGNOSTIC_TYPE", "PROVIDER",
                        "CANCER_SITE", "Observation value", "OBS_STATUS2", "SEX", "FUNCTION", 
                        "MODE_PROVISION", "CARE_TYPE", "HEALTH_FACILITY", "WAITING_TIME",
                        "CONSULTATION_TYPE", "OBS_STATUS", "OBS_STATUS2", "OBS_STATUS3", 
                        "MEDICAL_PROCEDURE", "OCCUPATION"]
    new_data_cols_rename_dict = {
        "OBS_VALUE": "hospital_stay_length"
    }
    df = tidy(df, df_title=df_title, new_data_cols_map=new_data_cols_rename_dict,
              drop_columns=unnecessary_cols)
    analyze(df, df_title)
    print(df)


def gdp_worldbank():
    """
    gdp_by_country csv file retrieved from https://databank.worldbank.org/reports.aspx?source=2&series=NY.GDP.MKTP.CD&country#, setting the year to 2000-2019
    """
    main_df = pd.read_csv('cleaned_datasets/main_df.csv')
    df = pd.read_csv('original_datasets/gdp_by_country.csv')
    code_col = 'Country Code'
    # drop down to only have countries and columns that are in the final merged df
    df = df[df[code_col].isin(main_df['code'].unique())]
    df = df.reset_index(drop=True)
    drop_cols = ['Series Name','Series Code']
    df = df.drop(columns=drop_cols)
    # get the year_col named like '2000' instead of '2000 [YR2000]'
    old_year_columns = [col for col in df.columns if 'YR' in col]
    new_year_columns = [year_col[:4] for year_col in old_year_columns]
    rename_dict = dict(zip(old_year_columns, new_year_columns))
    # rename cols in dict - combine year rename dict with other column rename dict
    rename_dict.update({'Country Name': 'country', code_col:'code'})
    df = df.rename(columns=rename_dict)
    df = pd.melt(df, id_vars=['country', 'code'], var_name='year',
                  value_vars=new_year_columns, value_name='gdp_in_usd')
    df.to_csv('cleaned_datasets/country_gdps.csv', index=False)

def oecd_population():
    df = pd.read_csv("original_datasets/oecd_population_data.csv")
    rename_cols = {"Code":"code","Population - Sex: all - Age: all - Variant: estimates":"population","Entity":"country","Year":"year"}
    df = df.rename(columns= rename_cols)
    print(df)
    unique_countires =len(df["code"].unique())
    print(unique_countires)
    df.to_csv("cleaned_datasets/population.csv",index = False)



# RUNNING MAIN PROGRAM
if __name__ == "__main__":
    # make sure to comment out the functions that you don't want to run inside the run() function
    run()
   
