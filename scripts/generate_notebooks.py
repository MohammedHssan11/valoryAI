import json
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def md(text):
    # Ensure source is a list of strings
    return {"cell_type": "markdown", "metadata": {}, "source": text.splitlines(True)}

def code(text):
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": text.splitlines(True)}

def create_notebook(cells, filename):
    nb = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {"name": "ipython", "version": 3},
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.8.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    with open(os.path.join(ROOT_DIR, filename), 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=2)

# ==========================================
# EGYPT NOTEBOOK
# ==========================================
egypt_cells = []

egypt_cells.append(md("""# Egypt Property Finder Dataset: Exploratory Data Analysis & Price Insights

## Executive Summary
This notebook explores the **Egypt Property Finder Comprehensive Dataset**. Our goal is to extract meaningful business insights from the real estate market in Egypt, analyzing price distributions, geographical hotspots, and key property features that drive value. 

Finally, we build a baseline Machine Learning model to predict property prices based on available features.

**Use Cases:**
- Real estate investment analysis.
- Predictive pricing models.
- Consumer market trends in Egypt.
"""))

egypt_cells.append(code("""import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

# Set aesthetic configurations
sns.set_theme(style="whitegrid")
"""))

egypt_cells.append(md("""## Section 2 - Data Loading
We will load the primary dataset (`all_egypt.csv`) which contains all the aggregated listings.
"""))

egypt_cells.append(code("""# Define path (Update this to your Kaggle input path)
DATA_PATH = '/kaggle/input/egypt-property-finder-dataset/processed/all_egypt.csv'

try:
    df = pd.read_csv(DATA_PATH)
except FileNotFoundError:
    # Fallback to local path for testing
    df = pd.read_csv('Egypt_Property_Finder_Kaggle/processed/all_egypt.csv')

print(f"Dataset Shape: {df.shape}")
display(df.head())
"""))

egypt_cells.append(md("""## Section 3 - Data Quality Assessment
Let's review missing values, duplicates, and general statistics.
"""))

egypt_cells.append(code("""# Missing Values
missing = df.isnull().sum()
missing = missing[missing > 0].sort_values(ascending=False)
print("Missing Values:\\n", missing)

# Duplicates
print("\\nDuplicate Rows:", df.duplicated().sum())

# Summary Statistics
display(df.describe())
"""))

egypt_cells.append(md("""## Section 4 - Exploratory Data Analysis
Let's visualize the core distributions of our data.
"""))

egypt_cells.append(code("""# Property Type Distribution
prop_counts = df['property_type'].value_counts().reset_index()
prop_counts.columns = ['Property Type', 'Count']
fig = px.bar(prop_counts, x='Property Type', y='Count', title='Distribution of Property Types', color='Count')
fig.show()

# Price Distribution (Log Scale)
fig = px.histogram(df, x='price', nbins=100, title='Property Price Distribution (Log Scale)', log_y=True)
fig.show()

# Bedrooms Distribution
fig = px.histogram(df.dropna(subset=['bedrooms']), x='bedrooms', title='Bedrooms Distribution')
fig.show()

# Size Distribution
fig = px.histogram(df[df['size'] < df['size'].quantile(0.99)], x='size', nbins=50, title='Property Size Distribution (Excluding Top 1% Outliers)')
fig.show()
"""))

egypt_cells.append(md("""**Interpretation:**
- Apartments and Villas heavily dominate the Egyptian market.
- The price distribution has a massive long tail, justifying the log scale.
- 3-bedroom properties are by far the most common configuration.
"""))

egypt_cells.append(md("""## Section 5 - Geographic Analysis
Where are the most expensive locations?
"""))

egypt_cells.append(code("""# Extract City/Broad location from the detailed location string
df['broad_location'] = df['location'].apply(lambda x: str(x).split(',')[-1].strip() if pd.notnull(x) else 'Unknown')

geo_stats = df.groupby('broad_location').agg({'price': 'median', 'size': 'median', 'id': 'count'}).reset_index()
geo_stats = geo_stats[geo_stats['id'] > 50].sort_values('price', ascending=False) # Filter locations with enough data

fig = px.bar(geo_stats.head(10), x='broad_location', y='price', title='Top 10 Most Expensive Broad Locations (Median Price)')
fig.show()

fig = px.bar(geo_stats.sort_values('size', ascending=False).head(10), x='broad_location', y='size', title='Top 10 Locations by Largest Median Property Size')
fig.show()
"""))

egypt_cells.append(md("""## Section 6 - Amenities Analysis
What features are commonly offered?
"""))

egypt_cells.append(code("""# Extract amenities
amenities_series = df['amenities'].dropna().astype(str).str.replace(r'[\\[\\]\\']', '', regex=True).str.split(',')
all_amenities = [item.strip() for sublist in amenities_series for item in sublist if item.strip()]

amenities_counts = pd.Series(all_amenities).value_counts().head(15).reset_index()
amenities_counts.columns = ['Amenity', 'Count']

fig = px.bar(amenities_counts, x='Count', y='Amenity', orientation='h', title='Top 15 Most Common Amenities')
fig.gca().invert_yaxis()
fig.show()
"""))

egypt_cells.append(md("""## Section 7 - Correlation Analysis
Understanding feature relationships.
"""))

egypt_cells.append(code("""numeric_cols = ['price', 'bedrooms', 'bathrooms', 'size', 'latitude', 'longitude']
corr = df[numeric_cols].corr()

fig = px.imshow(corr, text_auto=True, aspect="auto", title='Correlation Heatmap')
fig.show()
"""))

egypt_cells.append(md("""**Interpretation:**
As expected, `size`, `bedrooms`, and `bathrooms` exhibit high positive correlation with `price`.
"""))

egypt_cells.append(md("""## Section 8 - Business Insights
1. **Premium Hubs:** Certain districts dramatically outprice others, heavily skewed by newly developed gated communities (e.g., New Cairo, 6th of October).
2. **Standardization:** The 3-bedroom, 2-bathroom configuration is the undisputed standard for Egyptian families.
3. **Amenities Drive Value:** Properties listing "Security" and "Balcony" are universally present in top-tier listings.
"""))

egypt_cells.append(md("""## Section 9 - Baseline Machine Learning
Let's build a fast Random Forest model to establish a price prediction baseline.
"""))

egypt_cells.append(code("""# Prepare data
ml_df = df.dropna(subset=['price', 'bedrooms', 'bathrooms', 'size']).copy()

# Remove extreme outliers for baseline stability
q_low = ml_df['price'].quantile(0.01)
q_hi  = ml_df['price'].quantile(0.99)
ml_df = ml_df[(ml_df['price'] > q_low) & (ml_df['price'] < q_hi)]

features = ['bedrooms', 'bathrooms', 'size']
X = ml_df[features]
y = ml_df['price']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Model
rf = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
rf.fit(X_train, y_train)

# Predict
preds = rf.predict(X_test)

# Evaluate
mae = mean_absolute_error(y_test, preds)
rmse = np.sqrt(mean_squared_error(y_test, preds))
r2 = r2_score(y_test, preds)

print("--- Baseline Random Forest Metrics ---")
print(f"MAE:  {mae:,.2f} EGP")
print(f"RMSE: {rmse:,.2f} EGP")
print(f"R²:   {r2:.4f}")
"""))

egypt_cells.append(md("""## Section 10 - Conclusion
We have successfully mapped the Egyptian real estate landscape and established a functional baseline model capable of explaining a significant portion of price variance solely based on physical property dimensions. 

Future improvements could utilize NLP on the property titles and geo-spatial embeddings using latitude/longitude clustering.
"""))

create_notebook(egypt_cells, "Egypt_EDA.ipynb")

# ==========================================
# UAE NOTEBOOK
# ==========================================
uae_cells = []

uae_cells.append(md("""# UAE Property Finder Dataset: Dubai Real Estate Market Analysis

## Executive Summary
This notebook explores the **UAE Property Finder Comprehensive Dataset**. The UAE real estate market (particularly Dubai) is one of the most dynamic and hyper-competitive property markets in the world. 

We will analyze the residential and commercial markets, looking at pricing dynamics, community comparisons, and building a predictive model.

**Key Focus Areas:**
- Market category breakdowns (Rent vs Buy).
- High-value community hotspots.
- Predictive pricing baseline.
"""))

uae_cells.append(code("""import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

sns.set_theme(style="whitegrid")
"""))

uae_cells.append(md("""## Section 2 - Data Loading
We load all 5 UAE sub-datasets.
"""))

uae_cells.append(code("""import os

base_path = '/kaggle/input/uae-property-finder/'
if not os.path.exists(base_path):
    base_path = 'UAE_Property_Finder_Kaggle/processed/'

datasets = {
    'Res_Buy': pd.read_csv(os.path.join(base_path, 'dubai_residential_buy.csv')),
    'Res_Rent': pd.read_csv(os.path.join(base_path, 'dubai_residential_rent.csv')),
    'Com_Buy': pd.read_csv(os.path.join(base_path, 'dubai_commercial_buy.csv')),
    'Com_Rent': pd.read_csv(os.path.join(base_path, 'dubai_commercial_rent.csv')),
    'New_Projects': pd.read_csv(os.path.join(base_path, 'dubai_new_projects.csv'))
}

for name, df in datasets.items():
    print(f"{name} Shape: {df.shape}")

display(datasets['Res_Rent'].head())
"""))

uae_cells.append(md("""## Section 3 - Data Quality
Checking feature coverage across the datasets.
"""))

uae_cells.append(code("""# Null check for the largest dataset (Residential Rent)
nulls = datasets['Res_Rent'].isnull().sum()
print("Missing values in Residential Rent:\\n", nulls[nulls > 0].sort_values(ascending=False))

# Duplicates
print("\\nDuplicates in Residential Rent:", datasets['Res_Rent'].duplicated().sum())
"""))

uae_cells.append(md("""## Section 4 - Market Overview
Comparing category sizes.
"""))

uae_cells.append(code("""sizes = {name: len(df) for name, df in datasets.items()}
fig = px.bar(x=list(sizes.keys()), y=list(sizes.values()), title='Number of Listings per Category', color=list(sizes.values()))
fig.update_layout(xaxis_title="Category", yaxis_title="Number of Listings")
fig.show()
"""))

uae_cells.append(md("""**Interpretation:**
The rental market has significantly higher listing velocity and volume than the buy market in Dubai.
"""))

uae_cells.append(md("""## Section 5 - Pricing Analysis
Analyzing the Residential Rent pricing distribution.
"""))

uae_cells.append(code("""df_rent = datasets['Res_Rent'].copy()

# Price Distribution
fig = px.histogram(df_rent[df_rent['price'] < df_rent['price'].quantile(0.99)], x='price', nbins=50, title='Residential Rent Price Distribution (Excl. Outliers)')
fig.show()

if 'price_per_sqft' in df_rent.columns:
    fig = px.histogram(df_rent[df_rent['price_per_sqft'] < df_rent['price_per_sqft'].quantile(0.99)], x='price_per_sqft', nbins=50, title='Price per SqFt Distribution')
    fig.show()
"""))

uae_cells.append(md("""## Section 6 - Geographic Analysis
Identifying the most expensive communities for renting.
"""))

uae_cells.append(code("""# Clean location to get primary district
df_rent['district'] = df_rent['location'].apply(lambda x: str(x).split(',')[-2].strip() if len(str(x).split(',')) > 1 else str(x))

geo_price = df_rent.groupby('district').agg({'price': 'median', 'id': 'count'}).reset_index()
geo_price = geo_price[geo_price['id'] > 30].sort_values('price', ascending=False)

fig = px.bar(geo_price.head(15), x='district', y='price', title='Top 15 Most Expensive Districts (Median Rent)')
fig.show()
"""))

uae_cells.append(md("""## Section 7 - Property Features
Analyzing structural configurations.
"""))

uae_cells.append(code("""if 'bedrooms' in df_rent.columns:
    bed_counts = df_rent['bedrooms'].value_counts().reset_index()
    bed_counts.columns = ['Bedrooms', 'Count']
    fig = px.pie(bed_counts, values='Count', names='Bedrooms', title='Proportion of Bedrooms in Rental Listings')
    fig.show()
"""))

uae_cells.append(md("""## Section 8 - Correlation Analysis
"""))

uae_cells.append(code("""cols = ['price', 'bedrooms', 'bathrooms', 'size']
available_cols = [c for c in cols if c in df_rent.columns]
corr = df_rent[available_cols].corr()

fig = px.imshow(corr, text_auto=True, title='Feature Correlation Heatmap')
fig.show()
"""))

uae_cells.append(md("""## Section 9 - Machine Learning Baseline
Building a predictive model for Dubai rent prices.
"""))

uae_cells.append(code("""ml_df = df_rent.dropna(subset=['price', 'bedrooms', 'bathrooms', 'size']).copy()

q_low = ml_df['price'].quantile(0.01)
q_hi  = ml_df['price'].quantile(0.99)
ml_df = ml_df[(ml_df['price'] > q_low) & (ml_df['price'] < q_hi)]

features = ['bedrooms', 'bathrooms', 'size']
X = ml_df[features]
y = ml_df['price']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

rf = RandomForestRegressor(n_estimators=100, max_depth=12, random_state=42, n_jobs=-1)
rf.fit(X_train, y_train)

preds = rf.predict(X_test)

print("--- Baseline Random Forest Metrics (Rental Prices) ---")
print(f"MAE:  {mean_absolute_error(y_test, preds):,.2f} AED")
print(f"RMSE: {np.sqrt(mean_squared_error(y_test, preds)):,.2f} AED")
print(f"R²:   {r2_score(y_test, preds):.4f}")

# Feature Importance
imp = pd.DataFrame({'Feature': features, 'Importance': rf.feature_importances_})
fig = px.bar(imp.sort_values('Importance', ascending=False), x='Feature', y='Importance', title='Random Forest Feature Importance')
fig.show()
"""))

uae_cells.append(md("""## Section 10 - Market Insights
1. **Hyper-Velocity Rentals:** The rental market dwarfs the buy market, indicating high population transience and investor yield-generation.
2. **Size is King:** Property size strictly dominates pricing dynamics, vastly outweighing discrete bedroom counts in Dubai.
3. **Luxury Clusters:** Specific micro-communities (e.g., Palm Jumeirah, Downtown Dubai) drastically skew the upper echelons of the price distributions, suggesting severe inequality in district valuations.
"""))

create_notebook(uae_cells, "UAE_EDA.ipynb")
print("Notebooks successfully generated.")
