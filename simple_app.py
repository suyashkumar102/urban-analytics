
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

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
    page = st.sidebar.selectbox("Choose View", [
        "📊 Statistical Analysis", 
        "🗺️ Geographic Visualization", 
        "💡 Data Insights",
        "🏙️ City Explorer"
    ])
    
    if page == "📊 Statistical Analysis":
        st.header("📊 Statistical Analysis from Excel Data")
        st.markdown("*Comprehensive statistical plots generated from our cities dataset*")
        
        # File upload option
        st.subheader("📁 Data Source")
        col1, col2 = st.columns([2, 1])
        with col1:
            st.info("📊 Currently using: cities_data.csv (50 Indian cities)")
            st.write(f"**Dataset Shape:** {df.shape[0]} cities × {df.shape[1]} metrics")
        with col2:
            uploaded_file = st.file_uploader("Upload your Excel file", type=['xlsx', 'csv'])
            if uploaded_file:
                if uploaded_file.name.endswith('.xlsx'):
                    df_new = pd.read_excel(uploaded_file)
                else:
                    df_new = pd.read_csv(uploaded_file)
                st.success(f"✅ Loaded: {df_new.shape}")
                df = df_new
        
        # Statistical Plots Section
        st.markdown("---")
        st.subheader("📈 Statistical Visualizations")
        
        # Row 1: Histogram and Pie Chart
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📊 Histogram: UGI Score Distribution**")
            fig_hist = px.histogram(df, x='UGI', nbins=15, 
                                  title="Distribution of Urban Growth Intelligence Scores",
                                  labels={'UGI': 'UGI Score', 'count': 'Number of Cities'},
                                  color_discrete_sequence=['#1f77b4'])
            fig_hist.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig_hist, use_container_width=True)
        
        with col2:
            st.markdown("**🥧 Pie Chart: Cities by Region**")
            region_counts = df['Region'].value_counts()
            fig_pie = px.pie(values=region_counts.values, names=region_counts.index,
                           title="Distribution of Cities by Region",
                           color_discrete_sequence=px.colors.qualitative.Set3)
            fig_pie.update_layout(height=400)
            st.plotly_chart(fig_pie, use_container_width=True)
        
        # Row 2: Bar Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📊 Bar Chart: Top 10 Cities by Population**")
            top_pop = df.nlargest(10, 'Population_2011')
            fig_bar1 = px.bar(top_pop, x='Population_2011', y='City', orientation='h',
                            title="Most Populous Cities (2011 Census)",
                            labels={'Population_2011': 'Population (Millions)'},
                            color='Population_2011', color_continuous_scale='Blues')
            fig_bar1.update_layout(height=400)
            st.plotly_chart(fig_bar1, use_container_width=True)
        
        with col2:
            st.markdown("**💰 Bar Chart: Top 10 Cities by GDP**")
            top_gdp = df.nlargest(10, 'GDP_Billions_USD')
            fig_bar2 = px.bar(top_gdp, x='GDP_Billions_USD', y='City', orientation='h',
                            title="Highest GDP Cities",
                            labels={'GDP_Billions_USD': 'GDP (Billions USD)'},
                            color='GDP_Billions_USD', color_continuous_scale='Greens')
            fig_bar2.update_layout(height=400)
            st.plotly_chart(fig_bar2, use_container_width=True)
        
        # Row 3: Advanced Statistical Plots
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📈 Scatter Plot: Population vs GDP**")
            fig_scatter = px.scatter(df, x='Population_2011', y='GDP_Billions_USD',
                                   size='UGI', color='Region', hover_name='City',
                                   title="Economic Performance vs Population Size",
                                   labels={'Population_2011': 'Population (Millions)',
                                          'GDP_Billions_USD': 'GDP (Billions USD)'})
            fig_scatter.update_layout(height=400)
            st.plotly_chart(fig_scatter, use_container_width=True)
        
        with col2:
            st.markdown("**📊 Box Plot: UGI Scores by Region**")
            fig_box = px.box(df, x='Region', y='UGI', 
                           title="UGI Score Distribution Across Regions",
                           color='Region')
            fig_box.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig_box, use_container_width=True)
        
        # Summary Statistics Table
        st.markdown("---")
        st.subheader("📋 Statistical Summary")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Key Metrics Summary**")
            summary_stats = df[['Population_2011', 'GDP_Billions_USD', 'UGI', 'DailyFlights']].describe().round(2)
            st.dataframe(summary_stats)
        
        with col2:
            st.markdown("**Regional Statistics**")
            regional_stats = df.groupby('Region').agg({
                'UGI': ['mean', 'std', 'count'],
                'Population_2011': 'sum',
                'GDP_Billions_USD': 'sum'
            }).round(2)
            regional_stats.columns = ['Avg_UGI', 'UGI_StdDev', 'City_Count', 'Total_Pop', 'Total_GDP']
            st.dataframe(regional_stats)
    
    elif page == "🗺️ Geographic Visualization":
        st.header("🗺️ Geographic Visualization on India Map")
        st.markdown("*Interactive maps showing urban development patterns across India*")
        
        # Map 1: Bubble Map of Cities
        st.subheader("🫧 Bubble Map: Cities by UGI Score")
        fig_map1 = px.scatter_geo(df, 
                                lat='Latitude', lon='Longitude',
                                size='UGI', color='UGI',
                                hover_name='City',
                                hover_data=['State', 'Population_2011', 'GDP_Billions_USD'],
                                title="Indian Cities Urban Growth Intelligence Map",
                                color_continuous_scale='RdYlGn',
                                size_max=30)
        
        fig_map1.update_geos(
            projection_type="natural earth",
            showland=True, landcolor="lightgray",
            showocean=True, oceancolor="lightblue",
            showcountries=True, countrycolor="white",
            center_lat=20, center_lon=78,
            projection_scale=3
        )
        fig_map1.update_layout(height=600)
        st.plotly_chart(fig_map1, use_container_width=True)
        
        # Map 2: Population Density Map
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("👥 Population Distribution Map")
            fig_map2 = px.scatter_geo(df,
                                    lat='Latitude', lon='Longitude',
                                    size='Population_2011', color='Population_2011',
                                    hover_name='City',
                                    title="Population Distribution Across India",
                                    color_continuous_scale='Blues',
                                    size_max=25)
            fig_map2.update_geos(
                projection_type="natural earth",
                showland=True, landcolor="lightgray",
                center_lat=20, center_lon=78,
                projection_scale=3
            )
            fig_map2.update_layout(height=400)
            st.plotly_chart(fig_map2, use_container_width=True)
        
        with col2:
            st.subheader("💰 Economic Activity Map")
            fig_map3 = px.scatter_geo(df,
                                    lat='Latitude', lon='Longitude',
                                    size='GDP_Billions_USD', color='GDP_Billions_USD',
                                    hover_name='City',
                                    title="Economic Centers of India",
                                    color_continuous_scale='Greens',
                                    size_max=25)
            fig_map3.update_geos(
                projection_type="natural earth",
                showland=True, landcolor="lightgray",
                center_lat=20, center_lon=78,
                projection_scale=3
            )
            fig_map3.update_layout(height=400)
            st.plotly_chart(fig_map3, use_container_width=True)
        
        # Map 3: Connectivity Map
        st.subheader("✈️ Air Connectivity Map")
        # Filter cities with airports
        airport_cities = df[df['DailyFlights'] > 0]
        
        fig_map4 = px.scatter_geo(airport_cities,
                                lat='Latitude', lon='Longitude',
                                size='DailyFlights', color='DailyFlights',
                                hover_name='City',
                                hover_data=['DailyFlights', 'ConnectedAirports'],
                                title="Air Connectivity Network Across India",
                                color_continuous_scale='Reds',
                                size_max=40)
        fig_map4.update_geos(
            projection_type="natural earth",
            showland=True, landcolor="lightgray",
            center_lat=20, center_lon=78,
            projection_scale=3
        )
        fig_map4.update_layout(height=500)
        st.plotly_chart(fig_map4, use_container_width=True)
        
        # Geographic Insights
        st.markdown("---")
        st.subheader("🎯 Geographic Insights")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info("**🏙️ Urban Clusters**\n\nMajor urban clusters visible in Western (Mumbai-Pune) and Northern (Delhi-NCR) regions")
        with col2:
            st.info("**🌊 Coastal Advantage**\n\nCoastal cities show higher economic activity due to port access and trade")
        with col3:
            st.info("**✈️ Connectivity Hubs**\n\nMumbai and Delhi dominate air connectivity with 950+ and 1200+ daily flights")
    
    elif page == "💡 Data Insights":
        st.header("💡 Key Insights from Dataset Analysis")
        st.markdown("*Data-driven insights and recommendations based on comprehensive urban analysis*")
        
        # Key Performance Indicators
        st.subheader("📊 Key Performance Indicators")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Cities Analyzed", len(df), "🏙️")
        with col2:
            avg_ugi = df['UGI'].mean()
            st.metric("Average UGI Score", f"{avg_ugi:.1f}", "📈")
        with col3:
            top_city = df.loc[df['UGI'].idxmax(), 'City']
            top_score = df['UGI'].max()
            st.metric("Leading City", f"{top_city}", f"UGI: {top_score:.1f}")
        with col4:
            total_pop = df['Population_2011'].sum()
            st.metric("Total Urban Population", f"{total_pop:.0f}M", "👥")
        
        # Major Insights
        st.markdown("---")
        st.subheader("🔍 Major Insights")
        
        # Insight 1: Top Performers
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("### 🏆 **Top Performing Cities**")
            top_5 = df.nlargest(5, 'UGI')[['City', 'State', 'UGI', 'Population_2011', 'GDP_Billions_USD']]
            
            insight_text = f"""
            **Key Findings:**
            1. **{top_5.iloc[0]['City']}** leads with UGI score of {top_5.iloc[0]['UGI']:.1f}
            2. **Top 5 cities** account for {(top_5['Population_2011'].sum()/df['Population_2011'].sum()*100):.1f}% of total urban population
            3. **Economic dominance**: Top 5 cities contribute {(top_5['GDP_Billions_USD'].sum()/df['GDP_Billions_USD'].sum()*100):.1f}% of total GDP
            4. **Regional pattern**: {top_5['State'].value_counts().index[0]} state has {top_5['State'].value_counts().iloc[0]} cities in top 5
            """
            st.markdown(insight_text)
        
        with col2:
            st.dataframe(top_5.round(2))
        
        # Insight 2: Regional Analysis
        st.markdown("### 🗺️ **Regional Development Patterns**")
        col1, col2 = st.columns(2)
        
        with col1:
            regional_analysis = df.groupby('Region').agg({
                'UGI': 'mean',
                'Population_2011': 'sum',
                'GDP_Billions_USD': 'sum',
                'City': 'count'
            }).round(2)
            regional_analysis.columns = ['Avg_UGI', 'Total_Population', 'Total_GDP', 'City_Count']
            regional_analysis = regional_analysis.sort_values('Avg_UGI', ascending=False)
            
            best_region = regional_analysis.index[0]
            best_ugi = regional_analysis.iloc[0]['Avg_UGI']
            
            st.markdown(f"""
            **Regional Insights:**
            - **{best_region}** region leads with average UGI of {best_ugi:.1f}
            - **Economic concentration**: Top 3 regions account for 70%+ of total GDP
            - **Population distribution**: Uneven development across regions
            - **Growth opportunity**: Emerging regions show potential for investment
            """)
        
        with col2:
            fig_regional = px.bar(regional_analysis.reset_index(), 
                                x='Region', y='Avg_UGI',
                                title="Average UGI Score by Region",
                                color='Avg_UGI', color_continuous_scale='Viridis')
            fig_regional.update_layout(height=300)
            st.plotly_chart(fig_regional, use_container_width=True)
        
        # Insight 3: Connectivity vs Development
        st.markdown("### ✈️ **Connectivity Impact Analysis**")
        
        # Correlation analysis
        connectivity_corr = df[['DailyFlights', 'UGI', 'GDP_Billions_USD', 'Population_2011']].corr()['UGI'].sort_values(ascending=False)
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown(f"""
            **Connectivity Insights:**
            - **Strong correlation** between flights and UGI ({connectivity_corr['DailyFlights']:.2f})
            - **Metro cities** have {df[df['Metro']==1]['UGI'].mean():.1f} avg UGI vs {df[df['Metro']==0]['UGI'].mean():.1f} for non-metro
            - **Airport cities** show {((df[df['DailyFlights']>0]['UGI'].mean() / df[df['DailyFlights']==0]['UGI'].mean() - 1) * 100):.0f}% higher UGI scores
            """)
        
        with col2:
            fig_connectivity = px.scatter(df, x='DailyFlights', y='UGI', 
                                        size='Population_2011', color='Metro',
                                        hover_name='City',
                                        title="Connectivity vs Urban Development",
                                        labels={'DailyFlights': 'Daily Flights', 'UGI': 'UGI Score'})
            fig_connectivity.update_layout(height=300)
            st.plotly_chart(fig_connectivity, use_container_width=True)
        
        # Recommendations
        st.markdown("---")
        st.subheader("🎯 Strategic Recommendations")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            #### 🚀 **Investment Priorities**
            1. **Tier-2 cities** with high growth potential
            2. **Infrastructure development** in emerging regions
            3. **Connectivity enhancement** for underserved areas
            4. **Digital infrastructure** expansion
            """)
        
        with col2:
            st.markdown("""
            #### 📈 **Growth Opportunities**
            1. **Regional balance** through targeted development
            2. **Airport connectivity** for economic growth
            3. **Metro expansion** in major cities
            4. **Industrial corridor** development
            """)
        
        with col3:
            st.markdown("""
            #### ⚠️ **Key Challenges**
            1. **Urban inequality** between regions
            2. **Infrastructure gaps** in smaller cities
            3. **Connectivity bottlenecks**
            4. **Sustainable development** needs
            """)
        
        # Data Quality Note
        st.markdown("---")
        st.info("📊 **Data Sources**: Census 2011, RBI Economic Data, Airport Authority of India, Ministry Statistics. Analysis based on 50 major Indian cities with comprehensive urban development metrics.")
    
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
