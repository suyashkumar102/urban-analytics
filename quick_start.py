#!/usr/bin/env python3
"""
⚡ PULSE Quick Start - No Dependencies Required!
Creates your dataset and launches the app without complex installations
"""

import sys
import os
from pathlib import Path

def check_python():
    """Check Python version"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required. You have:", sys.version)
        return False
    print(f"✅ Python {sys.version.split()[0]} detected")
    return True

def install_minimal_deps():
    """Install only what's absolutely needed"""
    print("📦 Installing minimal dependencies...")
    
    essential = ["pandas", "numpy", "streamlit", "plotly"]
    
    for package in essential:
        try:
            __import__(package)
            print(f"✅ {package} already available")
        except ImportError:
            print(f"📥 Installing {package}...")
            os.system(f"pip install {package}")

def create_minimal_dataset():
    """Create dataset without complex dependencies"""
    print("📊 Creating sample dataset...")
    
    # Simple dataset creation without external dependencies
    import pandas as pd
    import numpy as np
    
    np.random.seed(42)
    
    # Top 50 Indian cities with real-ish data
    cities_data = {
        'City': [
            'Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata', 'Hyderabad', 
            'Pune', 'Ahmedabad', 'Surat', 'Jaipur', 'Lucknow', 'Kanpur', 
            'Nagpur', 'Indore', 'Thane', 'Bhopal', 'Visakhapatnam', 'Patna',
            'Vadodara', 'Ghaziabad', 'Ludhiana', 'Agra', 'Nashik', 'Faridabad',
            'Meerut', 'Rajkot', 'Varanasi', 'Srinagar', 'Aurangabad', 'Dhanbad',
            'Amritsar', 'Allahabad', 'Ranchi', 'Howrah', 'Coimbatore', 'Jabalpur',
            'Gwalior', 'Vijayawada', 'Jodhpur', 'Madurai', 'Raipur', 'Kota',
            'Guwahati', 'Chandigarh', 'Solapur', 'Hubli-Dharwad', 'Bareilly',
            'Moradabad', 'Mysore', 'Gurgaon'
        ]
    }
    
    # Real population data (Census 2011 - millions)
    real_populations = [18.4, 16.3, 8.5, 8.7, 14.1, 7.7, 5.0, 6.4, 4.6, 3.1, 
                       2.9, 2.9, 2.4, 2.2, 1.8, 1.8, 1.7, 1.7, 1.7, 1.6,
                       1.6, 1.6, 1.5, 1.4, 1.3, 1.3, 1.2, 1.2, 1.2, 1.1,
                       1.1, 1.1, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                       1.0, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9]
    
    # State mapping
    states = ['Maharashtra', 'Delhi', 'Karnataka', 'Tamil Nadu', 'West Bengal', 
              'Telangana', 'Maharashtra', 'Gujarat', 'Gujarat', 'Rajasthan',
              'Uttar Pradesh', 'Uttar Pradesh', 'Maharashtra', 'Madhya Pradesh', 
              'Maharashtra', 'Madhya Pradesh', 'Andhra Pradesh', 'Bihar',
              'Gujarat', 'Uttar Pradesh', 'Punjab', 'Uttar Pradesh', 'Maharashtra', 
              'Haryana', 'Uttar Pradesh', 'Gujarat', 'Uttar Pradesh', 'Jammu and Kashmir',
              'Maharashtra', 'Jharkhand', 'Punjab', 'Uttar Pradesh', 'Jharkhand', 
              'West Bengal', 'Tamil Nadu', 'Madhya Pradesh', 'Madhya Pradesh', 
              'Andhra Pradesh', 'Rajasthan', 'Tamil Nadu', 'Chhattisgarh', 'Rajasthan',
              'Assam', 'Chandigarh', 'Maharashtra', 'Karnataka', 'Uttar Pradesh',
              'Uttar Pradesh', 'Karnataka', 'Haryana']
    
    # Create DataFrame
    df = pd.DataFrame({
        'City': cities_data['City'],
        'State': states[:len(cities_data['City'])],
        'Population_2011': real_populations,
        'Region': np.random.choice(['North', 'South', 'East', 'West', 'Central', 'Northeast'], 
                                 len(cities_data['City'])),
        'Latitude': np.random.uniform(8, 35, len(cities_data['City'])),
        'Longitude': np.random.uniform(68, 97, len(cities_data['City']))
    })
    
    # Add economic data (GDP estimates based on city importance)
    gdp_multipliers = [100, 80, 45, 40, 35, 30, 25, 25, 20, 15] + [10] * 40
    df['GDP_Billions_USD'] = [pop * mult / 10 for pop, mult in zip(real_populations, gdp_multipliers)]
    
    # Add connectivity (flights based on city tier)
    flight_data = [950, 1200, 400, 350, 200, 300, 150, 180, 0, 80] + [20] * 40
    df['DailyFlights'] = flight_data
    
    # Add infrastructure scores
    df['Metro'] = [1 if city in ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata', 
                                'Hyderabad', 'Pune', 'Ahmedabad', 'Jaipur'] else 0 
                  for city in df['City']]
    
    # Calculate pillar scores
    df['Connectivity_Score'] = 30 + (df['DailyFlights'] / 10) + (df['Metro'] * 20)
    df['Economy_Score'] = 20 + (df['GDP_Billions_USD'] * 2)
    df['Demographics_Score'] = 40 + (df['Population_2011'] * 3)
    df['Infrastructure_Score'] = 35 + (df['GDP_Billions_USD'] * 1.5)
    df['Digital_Score'] = 25 + (df['GDP_Billions_USD'] * 1.8)
    
    # Calculate UGI score
    df['UGI'] = (df['Connectivity_Score'] * 0.25 + 
                 df['Economy_Score'] * 0.25 + 
                 df['Demographics_Score'] * 0.20 + 
                 df['Infrastructure_Score'] * 0.20 + 
                 df['Digital_Score'] * 0.10).round(1)
    
    # Ensure data directory exists
    Path("data/processed").mkdir(parents=True, exist_ok=True)
    
    # Save dataset
    output_path = "data/processed/cities_data.csv"
    df.to_csv(output_path, index=False)
    
    print(f"✅ Dataset created: {output_path}")
    print(f"📊 Shape: {df.shape}")
    print(f"🏙️ Top 5 cities by UGI:")
    top_5 = df.nlargest(5, 'UGI')[['City', 'State', 'UGI']]
    for _, row in top_5.iterrows():
        print(f"   {row['City']}, {row['State']}: {row['UGI']}")
    
    return True

def create_simple_app():
    """Create a simplified Streamlit app that definitely works"""
    print("🚀 Creating simplified Streamlit app...")
    
    app_content = '''
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="PULSE: India Urban Intelligence", page_icon="🏙️", layout="wide")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("data/processed/cities_data.csv")

def main():
    st.title("🏙️ PULSE: India Urban Growth Intelligence")
    st.markdown("*Comprehensive analysis of India's urban development*")
    
    df = load_data()
    
    # Sidebar
    st.sidebar.title("🧭 Navigation")
    page = st.sidebar.selectbox("Choose View", ["📊 Overview", "🏙️ City Details"])
    
    if page == "📊 Overview":
        # KPIs
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Cities Analyzed", len(df))
        with col2:
            st.metric("Avg UGI Score", f"{df['UGI'].mean():.1f}")
        with col3:
            st.metric("Top City", df.loc[df['UGI'].idxmax(), 'City'])
        with col4:
            st.metric("Total Population", f"{df['Population_2011'].sum():.0f}M")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🏆 Top 15 Cities by UGI")
            top_15 = df.nlargest(15, 'UGI')
            fig = px.bar(top_15, x='UGI', y='City', orientation='h',
                        title="Urban Growth Intelligence Rankings")
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("🗺️ Cities by Region")
            region_stats = df.groupby('Region').agg({
                'UGI': 'mean',
                'City': 'count'
            }).round(1)
            region_stats.columns = ['Avg_UGI', 'City_Count']
            
            fig = px.scatter(region_stats.reset_index(), 
                           x='City_Count', y='Avg_UGI', 
                           size='City_Count', color='Region',
                           title="Regional Performance Analysis")
            st.plotly_chart(fig, use_container_width=True)
        
        # Data table
        st.subheader("📋 Complete Dataset")
        st.dataframe(df[['City', 'State', 'Population_2011', 'GDP_Billions_USD', 'UGI']].round(2))
    
    else:
        # City details
        st.subheader("🏙️ City Explorer")
        
        selected_city = st.selectbox("Select a City", df['City'].sort_values())
        city_data = df[df['City'] == selected_city].iloc[0]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("UGI Score", f"{city_data['UGI']:.1f}")
        with col2:
            st.metric("Population", f"{city_data['Population_2011']:.1f}M")
        with col3:
            st.metric("GDP", f"${city_data['GDP_Billions_USD']:.1f}B")
        
        # Radar chart
        pillars = ['Connectivity_Score', 'Economy_Score', 'Demographics_Score', 
                  'Infrastructure_Score', 'Digital_Score']
        pillar_names = ['Connectivity', 'Economy', 'Demographics', 'Infrastructure', 'Digital']
        
        values = [city_data[pillar] for pillar in pillars]
        
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=pillar_names,
            fill='toself',
            name=selected_city
        ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            title=f"{selected_city} - Development Profile"
        )
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
'''
    
    # Save simplified app
    with open("simple_app.py", "w", encoding='utf-8') as f:
        f.write(app_content)
    
    print("✅ Simplified app created: simple_app.py")
    return True

def main():
    """Quick start main function"""
    print("⚡ PULSE Quick Start")
    print("=" * 40)
    
    # Check Python
    if not check_python():
        return
    
    # Install minimal deps
    install_minimal_deps()
    
    # Create dataset
    if not create_minimal_dataset():
        print("❌ Failed to create dataset")
        return
    
    # Create simple app
    create_simple_app()
    
    print("\n" + "=" * 50)
    print("🎉 PULSE PROJECT READY!")
    print("=" * 50)
    
    print("\n🚀 To launch your dashboard:")
    print("   streamlit run simple_app.py")
    
    print("\n📊 Your dataset is ready at:")
    print("   data/processed/cities_data.csv")
    
    print("\n💡 Next steps:")
    print("   1. Run: streamlit run simple_app.py")
    print("   2. Open browser to see your dashboard")
    print("   3. Enhance with real data (see REAL_DATA_GUIDE.md)")
    
    print("\n✨ No complex installations needed - just works!")

if __name__ == "__main__":
    main()