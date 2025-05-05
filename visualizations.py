#for generating visualilzations
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt


# ==================================================================================
# CALLING FUNCTIONS - comment out functions inside run() that you don't want to run
# ==================================================================================

def run():
    med_tech_availability_corr_with_expenditure()
    health_expenditure_p_capita_vs_health_expenditure_as_perc_gdp()
    death_by_country_over_time()
    hospital_stay_length_by_med_tech_avalibility_over_time()
    analyze_neg_expenditure_correlations()
    population()
    population_neg_expenditure_corr()
    gdp()    
    population_by_expenditure_per_capita()
    population_by_percent_gdp()
    per_capita_med_tech_availability()


# =============================================
# FUNCTION DEFINITIONS - no need to comment out
# =============================================

_NEG_EXPENDITURE_CORR_CODES = None
def get_neg_expenditure_corr_codes(correlation_data=None):
    if correlation_data is None:
        df = pd.read_csv('cleaned_datasets/main_df.csv')
        correlation_data = df.groupby('code').apply(
            lambda x: x['health_expenditure_as_percent_gdp'].corr(x['expenditure_per_capita'])
            ).reset_index(name='correlation')
    global _NEG_EXPENDITURE_CORR_CODES
    outlier_countries = correlation_data[correlation_data['correlation'] < 0]['code'].to_list()
    _NEG_EXPENDITURE_CORR_CODES = outlier_countries
    return _NEG_EXPENDITURE_CORR_CODES
    
def med_tech_availability_corr_with_expenditure():
    df = pd.read_csv('cleaned_datasets/main_df.csv')
    # get average over all years by country
    correlation_data = df.groupby('code').apply(
        lambda x: x['med_tech_availability_p_mil_ppl'].corr(x['expenditure_per_capita'])
    ).reset_index(name='correlation')

    plt.figure(figsize=(10, 6))
    plt.title("Correlation between Med Tech Availability and Expenditure per Capita by Country")
    sns.barplot(data=correlation_data, y='code', x='correlation', palette='viridis')
    plt.show()

def health_expenditure_p_capita_vs_health_expenditure_as_perc_gdp():
    df = pd.read_csv('cleaned_datasets/main_df.csv')
    correlation_data = df.groupby('code').apply(
        lambda x: x['health_expenditure_as_percent_gdp'].corr(x['expenditure_per_capita'])
    ).reset_index(name='correlation')

    plt.figure(figsize=(10, 6))
    plt.title("Correlation between Expenditure as percent of gdp and Expenditure per Capita by Country")
    sns.barplot(data=correlation_data, y='code', x='correlation', palette='viridis')
    plt.show()

def analyze_neg_expenditure_correlations():
    df = pd.read_csv('cleaned_datasets/main_df.csv')
    correlation_data = df.groupby('code').apply(
        lambda x: x['health_expenditure_as_percent_gdp'].corr(x['expenditure_per_capita'])
    ).reset_index(name='correlation')
    outlier_countries = get_neg_expenditure_corr_codes(correlation_data)
    df_outliers = df[df['code'].isin(outlier_countries)]
    
    plt.rc('figure', figsize=(15, 8))
    fig, (ax1, ax2) = plt.subplots(ncols=2, sharey=False)
    sns.lineplot(data=df_outliers, x='year', y='health_expenditure_as_percent_gdp', hue='code',palette='viridis', ax=ax1)
    ax1.set_title('Health Expenditure as Percentage of GDP Over Time')
    sns.lineplot(data=df_outliers, x='year', y='expenditure_per_capita', hue='code', palette='viridis', ax=ax2)
    ax2.set_title('Health Expenditure per Capita Over Time')
    plt.show()

def gdp(only_outlier_countries=True):
    df = pd.read_csv('cleaned_datasets/country_gdps.csv')
    data_df = None
    # only look at the gdp of outlier countries
    if only_outlier_countries:
        outlier_countries = get_neg_expenditure_corr_codes()
        df_weird_countries = df[df['code'].isin(outlier_countries)]
        plt.title("GDP of outlier countries in USD")
        data_df = df_weird_countries
    else:
        # look at gdp for all countries
        max_gdp = df['gdp_in_usd'].max()
        country_w_highest_gdp = df[df['gdp_in_usd'] == max_gdp]['code'].iloc[0]
        print("Country with highest GDP:", country_w_highest_gdp)
        df_except_highest = df[df['code'] != country_w_highest_gdp]
        data_df = df_except_highest

    sns.lineplot(x='year', y='gdp_in_usd', hue='country', data=data_df, palette='viridis')
    plt.show()

#avoidable deaths by country per year
def death_by_country_over_time():
    df = pd.read_csv("cleaned_datasets/main_df.csv")
    fig = sns.lineplot(hue = "code",y = "avoidable_deaths",x = "year", palette = "viridis", data = df)
    sns.move_legend(fig, "upper left", bbox_to_anchor=(1, 1))
    plt.show()

#hospital stay length by med tech avalibity
def hospital_stay_length_by_med_tech_avalibility_over_time():
    df = pd.read_csv("cleaned_datasets/main_df.csv")
    correlation_data = df.groupby('code').apply(
        lambda x: x['hospital_stay_length'].corr(x['med_tech_availability_p_mil_ppl'])
    ).reset_index(name='correlation')
    print(correlation_data)
    fig = sns.scatterplot(y = "code", x = "correlation", palette = "viridis", data =df)
    plt.xticks(range(0,7000,500))
    plt.title("Correlation between hostpial stay length and med tech avalability")
    sns.move_legend(fig, "upper left", bbox_to_anchor=(1, 1))
    plt.show()


# expenditure per capita by country (mean over the years)
def expenditure_per_capita_by_country():
    df = pd.read_csv("cleaned_datasets/main_df.csv")
    sns.barplot(data = df, x = 'code', y = 'expenditure_per_capita');
    plt.xticks(rotation=75)
    plt.tight_layout()
    plt.show()
    
# correlation heat map for all variables
def heat_map_all_var():
    df = pd.read_csv("cleaned_datasets/main_df.csv")
    plt.figure(figsize=(10, 8))
    correlation_matrix = df[['hospital_stay_length', 'med_tech_availability_p_mil_ppl',
                                    'expenditure_per_capita', 'life_expectancy',
                                    'avoidable_deaths', 'health_expenditure_as_percent_gdp']].corr()

    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Correlation Heatmap', fontsize=16)
    plt.show()
    
# key variables correlation plots
def key_variables_plot():
    df = pd.read_csv("cleaned_datasets/main_df.csv")
    sns.pairplot(df, vars=['expenditure_per_capita', 'life_expectancy', 
                                    'avoidable_deaths', 'health_expenditure_as_percent_gdp'],
                hue='code', palette='tab10', diag_kind='kde', height=2.5)
    plt.suptitle('Pair Plot for Key Variables', y=1.02, fontsize=16)
    plt.show()
    
# correlation between life expectancy and health expenditure by capita
def per_capita_life_exp():
    df = pd.read_csv("cleaned_datasets/main_df.csv")
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='expenditure_per_capita', y='life_expectancy', hue='code', palette='tab10')
    sns.regplot(data=df, x='expenditure_per_capita', y='life_expectancy', scatter=False, color='black')
    plt.title('Healthcare Expenditure vs. Life Expectancy', fontsize=16)
    plt.xlabel('Expenditure Per Capita', fontsize=14)
    plt.ylabel('Life Expectancy', fontsize=14)
    plt.legend(title='Country', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.show()

def per_capita_med_tech_availability():
    df = pd.read_csv("cleaned_datasets/main_df.csv")
    sns.scatterplot(data=df, x='expenditure_per_capita', y='med_tech_availability_p_mil_ppl', hue='code', palette='tab10')
    sns.regplot(data=df, x='expenditure_per_capita', y='life_expectancy', scatter=False, color='black')
    plt.title('Healthcare Expenditure vs. Medical Technology Availability', fontsize=16)
    plt.xlabel('Expenditure Per Capita', fontsize=14)
    plt.ylabel('Medical Technology Availability per Million people', fontsize=14)
    plt.legend(title='Country', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.show()

#population of all countries for each year
def population():
    df = pd.read_csv("cleaned_datasets/population.csv")
    sns.lineplot(hue = "country", x ="year",y = "population",data = df, palette = "tab10")
    plt.title("Population by country from 2000 - 2019")
    plt.legend(title='Country', bbox_to_anchor=(1, 1), loc='upper left')
    plt.show()
#closer look at populations with negative expenditure correlation for another analysis
def population_neg_expenditure_corr():
    df = pd.read_csv("cleaned_datasets/population.csv")
    outlier_countries = get_neg_expenditure_corr_codes()
    df_outlier_countries = df[df['code'].isin(outlier_countries)]
    sns.lineplot(hue = "country", x ="year",y = "population",data = df_outlier_countries, palette = "tab10")
    plt.title("Population for Outlier Countries from 2000 - 2019")
    plt.legend(title='Country', bbox_to_anchor=(1, 1), loc='upper left')
    plt.show()

#population by exepnditure correlation
def population_by_expenditure_per_capita():
    df_pop = pd.read_csv("cleaned_datasets/population.csv")
    df_main = pd.read_csv("cleaned_datasets/main_df.csv")
    merged_df = df_main.merge(df_pop, on = ['code','year'],how = 'inner')

    correlation_data = merged_df.groupby('code').apply(
        lambda x: x['population'].corr(x['expenditure_per_capita'])
    ).reset_index(name='correlation')

    plt.figure(figsize=(10, 6))
    plt.title("Correlation between Expenditure Per Capita and Population")
    sns.barplot(data=correlation_data, y='code', x='correlation', palette='viridis')
    plt.show()


#population by gdp correlation
def population_by_percent_gdp():
    df_pop = pd.read_csv("cleaned_datasets/population.csv")
    df_main = pd.read_csv("cleaned_datasets/main_df.csv")
    merged_df = df_main.merge(df_pop, on = ['code','year'],how = 'inner')

    correlation_data = merged_df.groupby('code').apply(
        lambda x: x['population'].corr(x['health_expenditure_as_percent_gdp'])
    ).reset_index(name='correlation')

    plt.figure(figsize=(10, 6))
    plt.title("Correlation between Expenditure as a Percentage of GDP and Population")
    sns.barplot(data=correlation_data, y='code', x='correlation', palette='viridis')
    plt.show()



# RUNNING MAIN PROGRAM
if __name__ == "__main__":
    run()