"""
Simplified Streamlit app to test geographic visualization
"""

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Geo Test", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("data/processed/cities_data.csv")

def main():
    st.title("🗺️ Geographic Visualization Test")
    
    df = load_data()
    
    # Sidebar
    page = st.sidebar.selectbox("Choose Test", [
        "📊 Data Check", 
        "🗺️ Geographic Map Test"
    ])
    
    if page == "📊 Data Check":
        st.header("📊 Data Verification")
        st.write(f"Dataset shape: {df.shape}")
        st.write("Columns:", list(df.columns))
        st.write("Sample data:")
        st.dataframe(df.head())
        
        st.write("Data ranges:")
        st.write(f"Latitude: {df['Latitude'].min():.2f} to {df['Latitude'].max():.2f}")
        st.write(f"Longitude: {df['Longitude'].min():.2f} to {df['Longitude'].max():.2f}")
        st.write(f"UGI: {df['UGI'].min():.1f} to {df['UGI'].max():.1f}")
    
    elif page == "🗺️ Geographic Map Test":
        st.header("🗺️ Geographic Map Test")
        
        try:
            st.write("Creating map...")
            
            # Simple map test
            fig = px.scatter_geo(df, 
                               lat='Latitude', lon='Longitude',
                               size='UGI', color='UGI',
                               hover_name='City',
                               title='India Cities Map Test',
                               color_continuous_scale='RdYlGn',
                               size_max=30)
            
            fig.update_geos(
                projection_type="natural earth",
                showland=True, landcolor="lightgray",
                showocean=True, oceancolor="lightblue",
                center_lat=20, center_lon=78,
                projection_scale=3
            )
            
            fig.update_layout(height=600)
            
            st.plotly_chart(fig, use_container_width=True)
            st.success("✅ Map created successfully!")
            
        except Exception as e:
            st.error(f"❌ Error creating map: {e}")
            st.write("Error details:", str(e))

if __name__ == "__main__":
    main()