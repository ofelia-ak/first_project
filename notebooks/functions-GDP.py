#================================================================
# Data Cleaning
#================================================================

years = [str(year) for year in range(1990, 2025)] # to drop off the extra columns
df = df.rename(columns={"Country Name": "country", "Country Code": "code"}) # to adjust column names
df = df[['country', 'code'] + years] # keep only the country name, country code, and the yearly data columns
df['country'] = df['country'].str.strip() # remove spaces from the country names
df_clean = df_new.fillna(0) # fill null values with 0
df_clean['year'] = df_clean['year'].astype(int) # convert year rows into integer

# List of countries that we want to keep in the dataset
required_countries = [
    "Afghanistan","Albania","Algeria","Andorra","Angola","Anguilla","Antigua and Barbuda",
    "Argentina","Armenia","Australia","Austria","Azerbaijan","Bahamas","Bahrain","Bangladesh", ...
]

# Dictionary used to standardize country names
name_map = {
    "Democratic People's Republic of Korea": "Korea, Dem. People's Rep.",
    "The former Yugoslav Republic of Macedonia": "North Macedonia", ...
}

# Replace country names in the DataFrame using the mapping dictionary
df['country'] = df['country'].replace(name_map)

# Filter the DataFrame to keep only rows where the country is in required_countries
df_new = df[df['country'].isin(required_countries)].reset_index(drop=True)

# Convert year columns into long form
df_clean = df_clean.melt(id_vars=['country', 'code'], var_name='year', value_name='gdp')



#================================================================
# Data Visualization
#================================================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.pyplot as plt


# First view into the data
#================================================================

# List of religion columns in the dataset
religion = ["christianity", "judaism", "islam", "buddhism", "hindu", "shinto", "confus_tao"]

# Find the religion with the highest value for each country (row)
# idxmax(axis=1) returns the column name with the maximum value across the row
df["dominant_religion"] = df[religion].idxmax(axis=1)

# Group the data by year and sum the values of each religion column
# This gives the total number of followers of each religion per year
religion_yearly = df.groupby("year")[religion].sum()

avg_gdp_by_religion = df.groupby("dominant_religion")["gdp"].mean() # avg GDP by religion

df["religiosity"] = df["religious_population"] / df["population"] # find religiosity share


# Religiosity by GDP level
#================================================================
df["religiosity"] = df["religious_population"] / df["population"] # find religiosity share
df["gdp_per_capita"] = df["gdp"] / df["population"]
df["gdp_group"] = pd.qcut(df["gdp_per_capita"], 3,                    # create GDP categories 
                          labels=["Low GDP","Medium GDP","High GDP"])

table = df.groupby("gdp_group").agg(
    avg_gdp_per_capita=("gdp_per_capita","mean"),
    avg_religiosity=("religiosity","mean"),
    countries=("country","nunique")
)


# Share of religion & GDP for countries in conflict and without conflict
#================================================================
# Filter the dataset to keep only rows where a conflict is present (conflict_present = 1)
conflict_df = df[df["conflict_present"] == 1]

# Group the conflict data by year and sum the values of each religion column
# This gives the total number of followers of each religion in countries with conflict for each year
conflict_yearly = conflict_df.groupby("year")[religion].sum()

# Convert the totals into percentage shares for each year
conflict_pct = conflict_yearly.div(conflict_yearly.sum(axis=1), axis=0) * 100

# **Same applies for non-conflict countries

# Then group the data by year and dominant religion
# Calculate the average GDP for each religion group in conflict/non-conflict countries
conflict_gdp = df[df["conflict_present"] == 1] \
    .groupby(["year","dominant_religion"])["gdp"] \
    .mean() \
    .reset_index()


# Religion and GDP composition around conflict
#================================================================

# Function to classify the war phase for each row
def war_phase(row):
    if row["conflict_present"] == 1:
        return "During War"       # conflict is happening in this year
    elif row["conflict_prev"] == 1:
        return "Post War"         # year immediately after a conflict
    elif row["conflict_next"] == 1:
        return "Pre War"          # year immediately before a conflict
    else:
        return "No Conflict"      # No conflict before, during, or after


# Apply the function to create a new column identifying the war phase
df["war_phase"] = df.apply(war_phase, axis=1)

# Group data by war phase and sum religion values
# This gives total followers of each religion within each war phase
religion_phase = df.groupby("war_phase")[religion].sum()

# Average GDP by war phase and dominant religion
gdp_phase_religion = (
    war_df.groupby(["war_phase","dominant_religion"])["gdp"]
    .mean()
    .reset_index()
)






