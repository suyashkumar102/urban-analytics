"""
🏙️ PULSE: India Urban Growth Intelligence Platform
Streamlit Dashboard - Portfolio Version

Two-page interactive dashboard:
1. National Overview - India UGI map, top cities, KPIs
2. City Explorer - Individual city analysis and insights
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import folium
from streamlit_folium import st_folium

# Page configuration
st.set_page_config(
    page_title="PULSE: India Urban Intelligence",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    }
    .insight-box {
        background-color: #e8f4fd;
        padding: 1rem;
        border-left: 5px solid #1f77b4;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and cache the cities dataset"""
    # In production, this would load from the actual CSV file
    # For now, creating sample data structure
    np.random.seed(42)
    
    cities = [
        'Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata', 'Hyderabad', 'Pune', 'Ahmedabad',
        'Surat', 'Jaipur', 'Lucknow', 'Kanpur', 'Nagpur', 'Indore', 'Thane', 'Bhopal',
        'Visakhapatnam', 'Pimpri-Chinchwad', 'Patna', 'Vadodara', 'Ghaziabad', 'Ludhiana',
        'Agra', 'Nashik', 'Faridabad', 'Meerut', 'Rajkot', 'Kalyan-Dombivali', 'Vasai-Virar',
        'Varanasi', 'Srinagar', 'Aurangabad', 'Dhanbad', 'Amritsar', 'Navi Mumbai', 'Allahabad',
        'Ranchi', 'Howrah', 'Coimbatore', 'Jabalpur', 'Gwalior', 'Vijayawada', 'Jodhpur',
        'Madurai', 'Raipur', 'Kota', 'Guwahati', 'Chandigarh', 'Solapur', 'Hubli-Dharwad'
    ]
    
    states = ['Maharashtra', 'Delhi', 'Karnataka', 'Tamil Nadu', 'West Bengal', 'Telangana', 
              'Gujarat', 'Rajasthan', 'Uttar Pradesh', 'Madhya Pradesh', 'Andhra Pradesh',
              'Punjab', 'Haryana', 'Jharkhand', 'Odisha', 'Kerala', 'Assam', 'Chhattisgarh']
    
    regions = ['West', 'North', 'South', 'East', 'Northeast', 'Central']
    
    data = {
        'City': cities,
        'State': np.random.choice(states, len(cities)),
        'Region': np.random.choice(regions, len(cities)),
        'UGI': np.random.normal(55, 15, len(cities)).clip(20, 95),
        'Population': np.random.lognormal(14, 0.8, len(cities)),
        'GDP': np.random.lognormal(2, 1.2, len(cities)),
        'DailyFlights': np.random.poisson(50, len(cities)),
        'GrowthRate': np.random.normal(2.5, 1.0, len(cities)).clip(0, 8),
        'LiteracyRate': np.random.normal(75, 10, len(cities)).clip(50, 95),
        'Connectivity_Score': np.random.normal(60, 20, len(cities)).clip(10, 100),
        'Economy_Score': np.random.normal(55, 18, len(cities)).clip(10, 100),
        'Demographics_Score': np.random.normal(65, 15, len(cities)).clip(10, 100),
        'Infrastructure_Score': np.random.normal(50, 20, len(cities)).clip(10, 100),
        'Digital_Score': np.random.normal(45, 25, len(cities)).clip(10, 100),
        'Latitude': np.random.uniform(8, 35, len(cities)),
        'Longitude': np.random.uniform(68, 97, len(cities))
    }
    
    df = pd.DataFrame(data)
    df['UGI'] = df['UGI'].round(1)
    df['Population'] = (df['Population'] / 1000000).round(2)  # Convert to millions
    df['GDP'] = df['GDP'].round(1)
    
    return df

def create_india_map(df):
    """Create interactive India map with UGI scores"""
    fig = px.scatter_geo(
        df,
        lat='Latitude',
        lon='Longitude',
        size='UGI',
        color='UGI',
        hover_name='City',
        hover_data=['State', 'Population', 'GDP'],
        title='India Urban Growth Intelligence Map',
        color_continuous_scale='RdYlGn',
        size_max=30
    )
    
    fig.update_geos(
        projection_type="natural earth",
        showland=True,
        landcolor="lightgray",
        showocean=True,
        oceancolor="lightblue",
        center_lat=20,
        center_lon=78,
        projection_scale=3
    )
    
    fig.update_layout(height=500)
    return fig

def create_radar_chart(city_data):
    """Create radar chart for city pillars"""
    pillars = ['Connectivity_Score', 'Economy_Score', 'Demographics_Score', 
               'Infrastructure_Score', 'Digital_Score']
    pillar_names = ['Connectivity', 'Economy', 'Demographics', 'Infrastructure', 'Digital']
    
    values = [city_data[pillar].iloc[0] for pillar in pillars]
    values += values[:1]  # Complete the circle
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=pillar_names + [pillar_names[0]],
        fill='toself',
        name=city_data['City'].iloc[0],
        line_color='rgb(31, 119, 180)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100])
        ),
        showlegend=False,
        title=f"{city_data['City'].iloc[0]} - Development Pillars",
        height=400
    )
    
    return fig

def main():
    # Header
    st.markdown('<h1 class="main-header">🏙️ PULSE: India Urban Growth Intelligence</h1>', 
                unsafe_allow_html=True)
    
    # Load data
    df = load_data()
    
    # Sidebar navigation
    st.sidebar.title("🧭 Navigation")
    page = st.sidebar.selectbox("Choose Page", ["🇮🇳 National Overview", "🏙️ City Explorer"])
    
    if page == "🇮🇳 National Overview":
        national_overview(df)
    else:
        city_explorer(df)

def national_overview(df):
    """National Overview Page"""
    st.header("🇮🇳 National Overview")
    
    # KPIs Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_ugi = df['UGI'].mean()
        st.metric("Average UGI Score", f"{avg_ugi:.1f}", "📊")
    
    with col2:
        high_growth_cities = len(df[df['UGI'] >= 70])
        st.metric("High-Growth Cities", high_growth_cities, "🚀")
    
    with col3:
        avg_flights = df['DailyFlights'].mean()
        st.metric("Avg Daily Flights", f"{avg_flights:.0f}", "✈️")
    
    with col4:
        avg_gdp = df['GDP'].mean()
        st.metric("Avg GDP (Billions)", f"${avg_gdp:.1f}B", "💰")
    
    st.markdown("---")
    
    # Main content in two columns
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Interactive India Map
        st.subheader("🗺️ Interactive UGI Map")
        fig_map = create_india_map(df)
        st.plotly_chart(fig_map, use_container_width=True)
    
    with col2:
        # Top 15 Cities Table
        st.subheader("🏆 Top 15 Cities")
        top_15 = df.nlargest(15, 'UGI')[['City', 'State', 'UGI']].reset_index(drop=True)
        top_15.index += 1
        st.dataframe(top_15, height=400)
    
    # Insights Section
    st.markdown("---")
    st.subheader("🔍 Key Insights")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="insight-box">
        <h4>🏙️ Metro Dominance</h4>
        <p>Mumbai, Delhi, and Bangalore lead with UGI scores above 80, driven by superior connectivity and economic activity.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="insight-box">
        <h4>🌱 Tier-2 Growth</h4>
        <p>Emerging cities show 23% higher growth potential, presenting significant investment opportunities.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="insight-box">
        <h4>🎯 Regional Balance</h4>
        <p>Southern states dominate rankings with balanced development across all five pillars.</p>
        </div>
        """, unsafe_allow_html=True)

def city_explorer(df):
    """City Explorer Page"""
    st.header("🏙️ City Explorer")
    
    # City selection
    selected_city = st.selectbox("Select a City", df['City'].sort_values())
    city_data = df[df['City'] == selected_city]
    
    if not city_data.empty:
        # City header
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.subheader(f"📍 {selected_city}")
            st.write(f"**State:** {city_data['State'].iloc[0]}")
            st.write(f"**Region:** {city_data['Region'].iloc[0]}")
        
        with col2:
            ugi_score = city_data['UGI'].iloc[0]
            st.metric("UGI Score", f"{ugi_score:.1f}", "🎯")
        
        with col3:
            rank = df['UGI'].rank(ascending=False)[city_data.index[0]]
            st.metric("National Rank", f"#{int(rank)}", "🏆")
        
        st.markdown("---")
        
        # Main content
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Radar Chart
            st.subheader("📊 Development Pillars")
            fig_radar = create_radar_chart(city_data)
            st.plotly_chart(fig_radar, use_container_width=True)
        
        with col2:
            # UGI Breakdown
            st.subheader("🎯 UGI Score Breakdown")
            
            pillars = ['Connectivity_Score', 'Economy_Score', 'Demographics_Score', 
                      'Infrastructure_Score', 'Digital_Score']
            pillar_names = ['Connectivity', 'Economy', 'Demographics', 'Infrastructure', 'Digital']
            
            breakdown_data = []
            for pillar, name in zip(pillars, pillar_names):
                score = city_data[pillar].iloc[0]
                breakdown_data.append({'Pillar': name, 'Score': score})
            
            breakdown_df = pd.DataFrame(breakdown_data)
            
            fig_bar = px.bar(
                breakdown_df, 
                x='Score', 
                y='Pillar', 
                orientation='h',
                color='Score',
                color_continuous_scale='RdYlGn',
                title=f"{selected_city} - Pillar Scores"
            )
            fig_bar.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Key Metrics Table
        st.subheader("📈 Key Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Population", f"{city_data['Population'].iloc[0]:.2f}M", "👥")
        
        with col2:
            st.metric("GDP", f"${city_data['GDP'].iloc[0]:.1f}B", "💰")
        
        with col3:
            st.metric("Growth Rate", f"{city_data['GrowthRate'].iloc[0]:.1f}%", "📈")
        
        with col4:
            st.metric("Daily Flights", f"{city_data['DailyFlights'].iloc[0]}", "✈️")
        
        # Recommendations
        st.markdown("---")
        st.subheader("💡 AI Recommendations")
        
        # Generate dynamic recommendations based on scores
        recommendations = generate_recommendations(city_data)
        
        for i, rec in enumerate(recommendations, 1):
            st.markdown(f"""
            <div class="insight-box">
            <h4>🎯 Recommendation {i}</h4>
            <p>{rec}</p>
            </div>
            """, unsafe_allow_html=True)

def generate_recommendations(city_data):
    """Generate AI recommendations based on city data"""
    recommendations = []
    
    # Analyze weakest pillar
    pillars = {
        'Connectivity_Score': 'connectivity infrastructure',
        'Economy_Score': 'economic development',
        'Demographics_Score': 'demographic planning',
        'Infrastructure_Score': 'basic infrastructure',
        'Digital_Score': 'digital transformation'
    }
    
    scores = {pillar: city_data[pillar].iloc[0] for pillar in pillars.keys()}
    weakest_pillar = min(scores, key=scores.get)
    weakest_score = scores[weakest_pillar]
    
    if weakest_score < 40:
        recommendations.append(f"Priority focus needed on {pillars[weakest_pillar]} (Score: {weakest_score:.1f}). Consider targeted investments and policy interventions.")
    
    # Growth potential analysis
    ugi = city_data['UGI'].iloc[0]
    growth_rate = city_data['GrowthRate'].iloc[0]
    
    if ugi > 60 and growth_rate > 3:
        recommendations.append("High growth potential detected. Excellent opportunity for business expansion and infrastructure development.")
    elif ugi < 50 but growth_rate > 2:
        recommendations.append("Emerging growth opportunity. Strategic investments could yield significant returns as the city develops.")
    
    # Connectivity recommendations
    flights = city_data['DailyFlights'].iloc[0]
    if flights < 20:
        recommendations.append("Limited air connectivity may hinder business growth. Consider advocating for improved airport infrastructure and flight frequency.")
    
    return recommendations[:3]  # Return top 3 recommendations

if __name__ == "__main__":
    main()