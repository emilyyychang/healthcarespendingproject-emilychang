"""
Tidying: import the tidy function from this file. Do not put dataset code in here.

Steps:
 - drop any years that aren't in the range 2000 to 2019
 - make sure all column names are lowercase and words are separated by underscores rather than spaces
 - Make dataframe have 1 index column (0-n), 1 countries column, 1 years column, 1+ variable column(s)
 - Each country in the country column will appear several times, same with each year in the year column. This is because for each country, we need one row per year.
    - therefore if there are c countries and y years, there will be c*y rows, where each country will be repeated y times and each year will be repeated c times
    
 - Ex:  (although year would be from 2000-2019 instead of 2008-2019)
    Country | Year | some_variable
    ------------------------------
    Albania | 2008 | 23.4
    Albania | 2009 | 26.2
    Andorra | 2008 | 11.1
    Andorra | 2009 | 10.3
"""
import pandas as pd


def drop_cols_with_proportion_na(df: pd.DataFrame, proportion: float = 0.9) -> pd.DataFrame:
    """
    Drop any columns in the dataframe that are some proportion or more of NA values
    Parameters:
        df - dataframe to drop columns from
        proportion - minimum proportion (between 0 and 1) of NA values in a column for that column to be dropped
    Returns:
        updated DataFrame
    """
    drop_cols = []
    # collect all columns that have >= proportion NA values
    for col in df.columns:
        proportion_na = df[col].isna().mean()
        if not isinstance(proportion_na, float):
            raise ValueError(f"after renaming columns, col '{col}' appears more than once in the dataframe. Please add one of them to the drop_columns when calling tidy().")
        if proportion_na >= proportion:
            drop_cols.append(col)
    # drop columns
    df = df.drop(columns=drop_cols)
    return df


def tidy_informational(df: pd.DataFrame, og_country_column: str = "Reference area", 
                       og_country_code_column: str = "REF_AREA", 
                       og_year_column: str = "TIME_PERIOD",
                       drop_columns:list[str]=None) -> pd.DataFrame:

    # drop unneeded columns
    if drop_columns is None:
        drop_columns = ["STRUCTURE", "STRUCTURE_ID", "STRUCTURE_NAME", "ACTION", "FREQ", "MEASURE",
                        "UNIT_MEASURE", "FINANCING_SCHEME", "FINANCING_SCHEME_REV", "FUNCTION",
                        "MODE_PROVISION", "PROVIDER", "FACTOR_PROVISION", "ASSET_TYPE",
                        "PRICE_BASE", "Time period", "Observation value", "Base period",
                        "CURRENCY", "UNIT_MULT", "DECIMALS", "Decimals"]
    df = df.drop(columns=drop_columns)
    # rename unclear columns
    rename_dict = {og_year_column: "year",
                   og_country_column: "country",
                   og_country_code_column: "code"}
    df = df.rename(columns=rename_dict)

    # drop all rows not in desried time frame
    max_year = 2019
    min_year = 2000
    df = df[(df["year"] <= max_year) & (df["year"] >= min_year)]

    # rename columns to be lowercase and replace spaces with underscores
    all_columns = list(df.columns)
    lower_columns = []
    for column in all_columns:
        lower_columns.append(column.lower().replace(" ", "_"))
    rename_dict = dict(zip(all_columns, lower_columns))
    df = df.rename(columns=rename_dict)

    # drop columns with at least 90% NA values
    df = drop_cols_with_proportion_na(df, 0.9)

    # drop columns that have the not applicable in them
    not_app_columns = df.columns[(df == "Not applicable").all()]
    df = df.drop(columns=not_app_columns)

    # drop columns that have the not application in them
    not_application_columns = df.columns[(df == "Not application").all()]
    df = df.drop(columns=not_application_columns)

    # checking that function successfully changed column names
    assert "country" in df.columns, "no country column found, orginal dataframe columns named differently than expected"
    assert "year" in df.columns, "no year column found, orginal dataframe columns named differently than expected"

    return df


def tidy_numerical(df):
    keep_columns = ["country", "year", "code"]
    numerical_columns = df.select_dtypes(include=["int64", "float64"]).columns
    for column in numerical_columns:
        if column not in keep_columns:
            keep_columns.append(column)
    drop_columns = [col for col in df.columns if col not in keep_columns]
    df = df.drop(columns=drop_columns)
    return df

def sort_by_country_and_year(df:pd.DataFrame) -> pd.DataFrame:
    return df.sort_values(['code', 'year'], ascending=[True, True])

def tidy(
        df: pd.DataFrame, df_title: str, new_data_cols_map: dict[str],
        og_country_column: str = "Reference area", og_year_column: str = "TIME_PERIOD",
        drop_columns: list[str] = None, og_country_code_column:str ="REF_AREA",) -> pd.DataFrame:
    """
    Tidy a dataframe in 2 steps, saving along the way:
        1. get it to an informational state and save in informational_datasets: 
            - drop useless columns
            - rename remaining columns
        2. get it to a tidy state and save in cleaned_datasets:
            - just containing an index, country, year, and data column(s)

    Parameters:
        - df: original dataframe
        - df_title: name of the dataframe - what the df represents (for saving in different files)
            - ex: "healthcare_expenditure_per_capita"
        - new_data_cols_map: dict mapping old name to new for the data column(s) in the df 
            - ex: {"OBSERVED VALUE":"healthcare_expenditure_per_capita"}
        - og_country_column: name of the column in the dataframe that contains the countries
        - og_year_name: name of the column in the dataframe that contains the years
        - drop_columns: a list of unneccessary columns that should be dropped
            - should not contain columns that would be put in the informational_dataset

    Returns:
        An updated, tidied dataframe

    Side Effects:
        Saves dfs to informational_datasets and cleaned_datasets
    """
    df_title = df_title.replace(" ", '_').lower()
    new_data_cols_map = {key: value.replace(" ", "_").lower()
                         for key, value in new_data_cols_map.items()}
    # rename important columns
    df = df.rename(columns=new_data_cols_map)
    df = tidy_informational(df,
                            og_country_column=og_country_column, 
                            og_year_column=og_year_column,
                            og_country_code_column=og_country_code_column, 
                            drop_columns=drop_columns)
    df.to_csv(f'informational_datasets/{df_title}.csv', index=False)
    df = tidy_numerical(df)
    df = sort_by_country_and_year(df)
    df.to_csv(f'cleaned_datasets/{df_title}.csv', index=False)
    df = df.reset_index(drop=True)
    return df
