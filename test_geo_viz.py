"""
Test geographic visualization functionality
"""

import pandas as pd
import plotly.express as px

def test_geographic_visualization():
    """Test if geographic visualization works"""
    print("🧪 Testing Geographic Visualization...")
    
    try:
        # Load data
        df = pd.read_csv('data/processed/cities_data.csv')
        print(f"✅ Data loaded: {df.shape}")
        
        # Check required columns
        required_cols = ['Latitude', 'Longitude', 'UGI', 'City', 'State']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            print(f"❌ Missing columns: {missing_cols}")
            return False
        
        print(f"✅ All required columns present: {required_cols}")
        
        # Test basic map creation
        fig = px.scatter_geo(df, 
                           lat='Latitude', lon='Longitude',
                           size='UGI', color='UGI',
                           hover_name='City',
                           title='Test India Map',
                           color_continuous_scale='RdYlGn')
        
        print("✅ Basic map created successfully")
        
        # Test map with geo settings
        fig.update_geos(
            projection_type="natural earth",
            showland=True, landcolor="lightgray",
            center_lat=20, center_lon=78,
            projection_scale=3
        )
        
        print("✅ Map geo settings applied successfully")
        
        # Save test map
        fig.write_html('test_geo_map.html')
        print("✅ Test map saved as test_geo_map.html")
        
        # Check data ranges
        print(f"\n📊 Data Ranges:")
        print(f"Latitude: {df['Latitude'].min():.2f} to {df['Latitude'].max():.2f}")
        print(f"Longitude: {df['Longitude'].min():.2f} to {df['Longitude'].max():.2f}")
        print(f"UGI: {df['UGI'].min():.1f} to {df['UGI'].max():.1f}")
        
        # Check for any null values
        null_counts = df[required_cols].isnull().sum()
        if null_counts.sum() > 0:
            print(f"⚠️ Null values found: {null_counts[null_counts > 0].to_dict()}")
        else:
            print("✅ No null values in required columns")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_geographic_visualization()
    
    if success:
        print("\n🎉 Geographic visualization test PASSED!")
        print("The issue might be in the Streamlit app interface.")
        print("\n💡 Possible solutions:")
        print("1. Try refreshing the browser page")
        print("2. Clear browser cache")
        print("3. Check browser console for JavaScript errors")
        print("4. Try a different browser")
    else:
        print("\n❌ Geographic visualization test FAILED!")
        print("There's an issue with the data or plotting functionality.")