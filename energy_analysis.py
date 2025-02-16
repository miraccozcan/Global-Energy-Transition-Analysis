import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 1. Load Data
# OWID data
owid_df = pd.read_csv('owid-energy-data.csv')

# World Energy Balances
wb_df = pd.read_excel('WorldEnergyBalancesHighlights2024.xlsx', 
                      sheet_name='TimeSeries_1971-2023',
                      skiprows=2)

# 2. Global Analysis
def plot_global_trends():
    # Filter
    global_data = owid_df[owid_df['country'] == 'World'].copy()
    
    # Create figure with secondary y-axis
    fig = make_subplots(rows=2, cols=2,
                       subplot_titles=('Renewable Share in Electricity',
                                     'Energy Mix Evolution',
                                     'Technology Adoption',
                                     'Carbon Intensity'))
    
    # Add renewable share trend
    fig.add_trace(
        go.Scatter(x=global_data['year'], 
                  y=global_data['renewables_share_elec'],
                  name='Renewables'),
        row=1, col=1
    )
    
    # Add energy mix evolution
    energy_sources = ['coal_share_energy', 'gas_share_energy', 
                     'oil_share_energy', 'renewables_share_energy']
    
    for source in energy_sources:
        fig.add_trace(
            go.Scatter(x=global_data['year'],
                      y=global_data[source],
                      name=source.split('_')[0].title(),
                      stackgroup='one'),
            row=1, col=2
        )
    
    # Add technology adoption
    techs = ['solar_share_elec', 'wind_share_elec', 'hydro_share_elec']
    for tech in techs:
        fig.add_trace(
            go.Scatter(x=global_data['year'],
                      y=global_data[tech],
                      name=tech.split('_')[0].title()),
            row=2, col=1
        )
    
    # Add carbon intensity
    fig.add_trace(
        go.Scatter(x=global_data['year'],
                  y=global_data['carbon_intensity_elec'],
                  name='Carbon Intensity'),
        row=2, col=2
    )
    
    fig.update_layout(height=800, 
                     title_text="Global Energy Transition Analysis",
                     showlegend=True)
    
    fig.show()

# 3. Regional Analysis
def plot_regional_comparison(year=2022):
    # Define regions
    regions = {
        'North America': ['United States', 'Canada', 'Mexico'],
        'Europe': ['Germany', 'France', 'United Kingdom', 'Italy', 'Spain'],
        'Asia': ['China', 'India', 'Japan', 'South Korea'],
        'Oceania': ['Australia', 'New Zealand']
    }
    
    # Get data for specified year
    year_data = owid_df[owid_df['year'] == year].copy()
    
    # Calculate regional averages
    regional_data = []
    for region, countries in regions.items():
        region_df = year_data[year_data['country'].isin(countries)]
        regional_data.append({
            'Region': region,
            'Renewable_Share': region_df['renewables_share_elec'].mean(),
            'Solar_Share': region_df['solar_share_elec'].mean(),
            'Wind_Share': region_df['wind_share_elec'].mean(),
            'Hydro_Share': region_df['hydro_share_elec'].mean()
        })
    
    regional_df = pd.DataFrame(regional_data)
    
    # Create radar chart
    fig = go.Figure()
    
    for idx, row in regional_df.iterrows():
        fig.add_trace(go.Scatterpolar(
            r=[row['Solar_Share'], row['Wind_Share'], 
               row['Hydro_Share'], row['Renewable_Share']],
            theta=['Solar', 'Wind', 'Hydro', 'Total Renewables'],
            name=row['Region']
        ))
    
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=True,
        title=f'Regional Renewable Energy Profile ({year})'
    )
    
    fig.show()

# 4. Top Countries Analysis
def plot_top_countries(year=2022):
    # Get data for specified year
    year_data = owid_df[owid_df['year'] == year].copy()
    
    # Get top 10 countries by renewable share
    top_countries = year_data.nlargest(10, 'renewables_share_elec')
    
    # Create bar plot
    fig = px.bar(top_countries, 
                 x='country', 
                 y=['solar_share_elec', 'wind_share_elec', 'hydro_share_elec'],
                 title=f'Top 10 Countries by Renewable Energy Share ({year})')
    
    fig.update_layout(
        xaxis_title="Country",
        yaxis_title="Share of Electricity (%)",
        barmode='stack'
    )
    
    fig.show()

# 5. Execute all analyses
print("Generating visualizations...")

# Plot global trends
plot_global_trends()

# Plot regional comparison
plot_regional_comparison()

# Plot top countries
plot_top_countries()

# 6. Calculate and display key metrics
def display_key_metrics(year=2022):
    year_data = owid_df[owid_df['year'] == year].copy()
    world_data = year_data[year_data['country'] == 'World'].iloc[0]
    
    print(f"\nKey Global Metrics for {year}:")
    print(f"Global Renewable Share: {world_data['renewables_share_elec']:.1f}%")
    print(f"Solar Share: {world_data['solar_share_elec']:.1f}%")
    print(f"Wind Share: {world_data['wind_share_elec']:.1f}%")
    print(f"Hydro Share: {world_data['hydro_share_elec']:.1f}%")
    print(f"Carbon Intensity: {world_data['carbon_intensity_elec']:.1f} gCO2/kWh")

display_key_metrics()
