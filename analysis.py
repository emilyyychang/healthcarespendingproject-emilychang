import pandas as pd


def _print_title(title):
    """ Print the given title with a border around it
    """
    num_chars = 50
    print("\n", "="*num_chars, title, "="*num_chars, "", sep="\n")


def analyze(df: pd.DataFrame, df_title: str, cols_to_skip: list[str] = ["country", "code", "year"]):
    """
    Parameters:
        df - cleaned, tidy dataframe to analyze (columns should be variables, not individual years)
        df_title - what the dataframe represents (e.g. "Healthcare Expenditure Per Capita By Country")
        cols_to_skip (optional) - list of columns you don't want to analyze (e.g. ["country", "year"])
            - default is ["country", "year"]
            - If you want to analyze all columns (not recommended), set cols_to_skip=[]
    Returns:
        None, but prints information about the dataframe
    """
    _print_title(df_title)

    print("Dataframe description:")
    print(df.describe(), "\n")

    print("\nColumn Values Breakdown:")
    # Create a list of columns to analyze
    cols_to_analyze = [col for col in df.columns if col not in cols_to_skip]
    # Give value counts for each column
    for col in cols_to_analyze:
        print(f"Column {col}:")
        print(df[col].value_counts(), "\n")

    # analyze correlation between variable columns if more than one variable to analyze
    if len(cols_to_analyze) > 1:
        print("\nCorrelation Between Columns:")
        print(df[cols_to_analyze].corr(), "\n")
