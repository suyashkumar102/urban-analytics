# 🎯 Real Data Collection Guide for PULSE

## 🚀 Quick Start (30 minutes)

### Step 1: Run the Data Collector
```bash
cd pulse-india-urban-intelligence
python src/utils/data_collector.py
```

This creates a baseline dataset with real population/economic data mixed with estimates.

### Step 2: Download Key Government Files

#### A. Census 2011 Urban Agglomerations
1. Go to: https://censusindia.gov.in/2011-prov-results/paper2/data_files/India2/Table_3_PR_UA_Citiees_1Lakh_and_Above.xlsx
2. Download Excel file
3. Save as `data/raw/census_urban_2011.xlsx`

#### B. State GDP Data (MOSPI)
1. Go to: http://mospi.nic.in/sites/default/files/publication_reports/State_wise_SDP_2011-12_to_2020-21.xlsx
2. Download latest state GDP file
3. Save as `data/raw/state_gdp_2022.xlsx`

#### C. Airport Traffic Data
1. Go to: https://www.aai.aero/sites/default/files/traffic-news/monthwise/Dec2022/annex4.pdf
2. Download annual traffic statistics
3. Extract data manually or use PDF parsing

## 📊 Detailed Data Collection Process

### Phase 1: Demographics (High Priority)

#### 1.1 Census Data Collection
```python
# After downloading Census file
import pandas as pd

# Load Census urban agglomeration data
census_df = pd.read_excel('data/raw/census_urban_2011.xlsx', 
                         sheet_name='UA_Population')

# Extract key columns
cities_census = census_df[['Name of UA', 'Total Population', 
                          'Literacy Rate', 'State']].copy()

# Clean city names
cities_census['City'] = cities_census['Name of UA'].str.replace(' UA', '')
cities_census['Population_2011'] = cities_census['Total Population'] / 1000000  # Convert to millions

print(f"Census data loaded: {len(cities_census)} cities")
```

#### 1.2 Population Growth Estimates
```python
# Use World Bank/UN data for growth projections
# 2011 -> 2023 projection using average urban growth rate (2.3% annually)

cities_census['Population_2023'] = cities_census['Population_2011'] * (1.023 ** 12)
cities_census['Growth_Rate'] = ((cities_census['Population_2023'] / cities_census['Population_2011']) ** (1/12) - 1) * 100
```

### Phase 2: Economic Data (Medium Priority)

#### 2.1 State GDP Allocation
```python
# Load state GDP data
state_gdp = pd.read_excel('data/raw/state_gdp_2022.xlsx')

# Major city GDP allocation (research-based estimates)
city_gdp_allocation = {
    'Mumbai': 0.35,      # 35% of Maharashtra GDP
    'Delhi': 0.80,       # 80% of Delhi GDP  
    'Bangalore': 0.40,   # 40% of Karnataka GDP
    'Chennai': 0.35,     # 35% of Tamil Nadu GDP
    'Kolkata': 0.45,     # 45% of West Bengal GDP
    'Hyderabad': 0.50,   # 50% of Telangana GDP
    'Pune': 0.15,        # 15% of Maharashtra GDP
    'Ahmedabad': 0.25,   # 25% of Gujarat GDP
    # Add more based on research
}

# Calculate city GDP
for city, allocation in city_gdp_allocation.items():
    state = city_state_mapping[city]
    state_total = state_gdp[state_gdp['State'] == state]['GDP_2022'].iloc[0]
    city_gdp = state_total * allocation
    # Store in dataset
```

#### 2.2 FDI Data (RBI Source)
```python
# Download from: https://rbi.org.in/Scripts/PublicationsView.aspx?id=20432
# State-wise FDI data, allocate to major cities

fdi_data = {
    'Maharashtra': 15.8,  # Billions USD (2022-23)
    'Karnataka': 8.2,
    'Delhi': 6.5,
    'Tamil Nadu': 4.1,
    'Gujarat': 3.8
}

# Allocate FDI to cities based on economic importance
```

### Phase 3: Infrastructure Data (Medium Priority)

#### 3.1 Airport Connectivity
```python
# Manual extraction from AAI reports or use this API approach:

import requests

def get_airport_data():
    # Use flight tracking APIs (some are free with limits)
    airports = {
        'Mumbai': 'BOM',
        'Delhi': 'DEL', 
        'Bangalore': 'BLR',
        'Chennai': 'MAA',
        'Kolkata': 'CCU',
        'Hyderabad': 'HYD'
    }
    
    flight_data = {}
    for city, code in airports.items():
        # API call to get daily flights (example)
        # flight_data[city] = get_daily_flights(code)
        pass
    
    return flight_data
```

#### 3.2 Railway Connectivity
```python
# Use Indian Railways API or manual data collection
railway_stations = {
    'Mumbai': ['CSTM', 'LTT', 'BCT'],  # Major stations
    'Delhi': ['NDLS', 'DLI', 'NZM'],
    'Bangalore': ['SBC', 'YPR'],
    # Add more
}

# Count daily trains per city (manual research required)
```

#### 3.3 Healthcare Infrastructure
```python
# From Ministry of Health data
# https://mohfw.gov.in/sites/default/files/HealthInfrastructureStatistics2022.pdf

hospitals_per_city = {
    'Mumbai': 150,      # Research-based estimates
    'Delhi': 120,
    'Bangalore': 80,
    'Chennai': 90,
    # Add more based on health ministry data
}
```

### Phase 4: Digital Infrastructure (Lower Priority)

#### 4.1 Internet Penetration (TRAI Data)
```python
# Download from: https://trai.gov.in/sites/default/files/PIR_07032023_0.pdf
# State-wise broadband data, allocate to cities

internet_penetration = {
    'Delhi': 85.2,       # % of population
    'Mumbai': 82.1,
    'Bangalore': 78.5,
    'Chennai': 76.8,
    # Extract from TRAI reports
}
```

#### 4.2 Startup Ecosystem
```python
# Use Startup India portal data
# https://www.startupindia.gov.in/content/sih/en/search.html

startup_counts = {
    'Bangalore': 4500,   # Approximate registered startups
    'Mumbai': 3200,
    'Delhi': 2800,
    'Hyderabad': 1500,
    # Research from startup databases
}
```

## 🔧 Data Integration Script

### Complete Integration Example
```python
def integrate_all_data():
    # Load all collected data
    census_df = load_census_data()
    economic_df = load_economic_data() 
    infrastructure_df = load_infrastructure_data()
    digital_df = load_digital_data()
    
    # Merge on city name
    final_df = census_df.merge(economic_df, on='City', how='outer')
    final_df = final_df.merge(infrastructure_df, on='City', how='outer')
    final_df = final_df.merge(digital_df, on='City', how='outer')
    
    # Fill missing values with estimates
    final_df = fill_missing_estimates(final_df)
    
    # Calculate UGI score
    final_df = calculate_ugi_score(final_df)
    
    return final_df

# Run integration
complete_dataset = integrate_all_data()
complete_dataset.to_csv('data/processed/cities_data_real.csv', index=False)
```

## ⏰ Time Investment by Data Quality

### Option 1: Quick & Good (2-3 days)
- Use data collector script (baseline)
- Add Census 2011 data (1 day)
- Add basic economic estimates (1 day)
- Result: 70% real data, 30% estimates

### Option 2: Comprehensive & Excellent (1 week)
- All government sources
- Manual data extraction
- Cross-validation
- Result: 90% real data, 10% estimates

### Option 3: Research-Grade (2 weeks)
- Primary source verification
- Multiple data source triangulation
- Custom APIs and web scraping
- Result: 95%+ real data

## 🎯 Recommendation for Portfolio

**Start with Option 1** - it gives you credible, mostly real data quickly. You can always upgrade to Option 2 later.

The key is having **defensible data sources** you can cite in interviews:
- "Population data from Census 2011"
- "Economic estimates based on RBI state GDP data"
- "Infrastructure data from sectoral ministries"

This approach impresses recruiters while being achievable in your timeline.

## 📋 Next Steps

1. **Run the data collector**: `python src/utils/data_collector.py`
2. **Download Census file**: Get urban agglomeration data
3. **Enhance with real data**: Replace estimates with downloaded data
4. **Document sources**: Update README with data citations
5. **Validate results**: Cross-check with known city rankings

Your PULSE project will have real, credible data that stands up to scrutiny! 🚀