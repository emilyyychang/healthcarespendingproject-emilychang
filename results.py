import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("cleaned_datasets/main_df.csv")

new = df.groupby('code').mean()
new = new.drop(columns = ['year'])

#ranks by a column
def rank_column(column,ascending):
    rank = new.sort_values(column,ascending = ascending)
    rank = rank.reset_index()
    rank['rank'] = rank.index+1
    mean_col_value = rank[column].mean()
    sd_col = rank[column].std()
    rank = rank[['rank','code',column]]
    return {'rank_df':rank, 'mean':mean_col_value, 'sd':sd_col}


quality_of_care_info = {
    # lowest stay should be ranked 1st --> ascending = True
    'hospital_stay_length':rank_column('hospital_stay_length', True),
    # lowest technology availability should be ranked lowest --> ascending = False
    'med_tech_availability_p_mil_ppl':rank_column('med_tech_availability_p_mil_ppl', False),
    # lowest life expectancy should be ranked lowest --> ascending = False
    'life_expectancy':rank_column('life_expectancy', False),
    # lowest avoidable deaths should be ranked 1st --> ascending = True
    'avoidable_deaths':rank_column("avoidable_deaths", True)
}
[hos_stay, med_ava, life_exp, avoidable_death] = [data['rank_df'] for data in quality_of_care_info.values()]

#weighted average 
def weight_averages(multipliers_dict):
    columns = ['code','rank']
    # get dataframes ready to be merged, only including the code and rank columns
    df_pair_1 = [hos_stay[columns], med_ava[columns]]
    df_pair_2 = [life_exp[columns],avoidable_death[columns]]
    # merge all 4 dataframes into one, with columns such as "rank_hospital_stay_length"
    rank_df_1 = pd.merge(df_pair_1[0],df_pair_1[1], on = "code", suffixes = ['_hospital_stay_length','_med_tech_availability_p_mil_ppl'])
    rank_df_2 = pd.merge(df_pair_2[0],df_pair_2[1], on = "code", suffixes = ['_life_expectancy','_avoidable_deaths'])
    rank_df = pd.merge(rank_df_1,rank_df_2, on = "code")
    # calculated the weighted average based on the passed in normalized multipliers dict
    rank_df['rank_weighted_avg'] = 0
    for column,multiplier in multipliers_dict.items():
        temp = rank_df[column] * multiplier
        rank_df["rank_weighted_avg"] = rank_df["rank_weighted_avg"] + temp

    return rank_df
        
# calculate the weights based on variability (sd as a percent of mean)
def weight_by_sd_as_perc_mean(quality_of_care_dict):
    """Determine the weights based on standard deviation as a percent of mean, all normalized"""
    # get unnormalized weights
    weights_dict = {}
    for title, stats in quality_of_care_dict.items():
        rank_title = 'rank_' + title
        sd_as_perc_mean = 100 * stats['sd']/stats['mean']
        weights_dict[rank_title] = sd_as_perc_mean
    # normalize weights so they can be used as multipliers in a weighted average
    total_weight = sum(weights_dict.values())
    weights_dict = {title: weight/total_weight for title, weight in weights_dict.items()}
    return weights_dict

# choose normalized multipliers to be summed for the weighted average
#life expentacy has a really low standard deviation meaning that it does not mattter much in calucluation of effectiveness of healthcare 
#where as med tech avaibility and avoidable deaths have a really large standard deviation 
#decided how to weight based on standard deviation as a percent of mean
rank_titles = ['rank_' + title for title in quality_of_care_info.keys()]
unweighted_multipliers = dict(zip(rank_titles, [0.25]*4))
weighted_multipliers = weight_by_sd_as_perc_mean(quality_of_care_info)

#results dataframe organization
def calculate_results(multipliers):
    """Given a dictionary of column names and multipliers, calculate the weighted average.
    Return a dataframe containing the final rank, code, and the weighted average of all ranked variables.
    """
    rank_df = weight_averages(multipliers)
    results_df = rank_df.sort_values("rank_weighted_avg",ascending = True)
    results_df = results_df.reset_index(drop = True)
    results_df["rank"] = results_df.index + 1
    results_df = results_df[["rank", "code", "rank_weighted_avg"]]
    return results_df

# calculate results based on the different multipliers
results_unweighted = calculate_results(weighted_multipliers)
results_weighted = calculate_results(weighted_multipliers)

#expenditure rankings 
#draw corellation between quality ranking and gdp ranking, and capita ranking seperately 
gdp_expenditure = rank_column("health_expenditure_as_percent_gdp", False)['rank_df']
capita_expenditure = rank_column('expenditure_per_capita', False)['rank_df']

#correlation of rankings visulizations 
def care_quality_vs_expenditure(results_df, expenditure_rank_df, metric_title, graph_suffix):
    merged_df = pd.merge(results_df, expenditure_rank_df, on = ['code'], suffixes = ["_final","_health_expenditure"])
    plt.figure(figsize=(10, 6))
    plt.title(f"Rank of {metric_title} vs HealthCare Quality Rank {graph_suffix}")
    sns.scatterplot(data= merged_df, y='rank_final', x='rank_health_expenditure')
    plt.show()

care_quality_vs_expenditure(results_unweighted, gdp_expenditure, 
                            "Expenditure as a Percentage of GDP", "for Unweighted Multipliers")
care_quality_vs_expenditure(results_unweighted, capita_expenditure, 
                            "Expenditure per Capita", "for Unweighted Multipliers")

care_quality_vs_expenditure(results_weighted, gdp_expenditure, 
                            "Expenditure as a Percentage of GDP", "for Weighted Multipliers")
care_quality_vs_expenditure(results_weighted, capita_expenditure, 
                            "Expenditure per Capita", "for Weighted Multipliers")