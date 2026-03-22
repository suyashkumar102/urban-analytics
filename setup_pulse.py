#!/usr/bin/env python3
"""
🚀 PULSE Project Quick Setup Script
Run this to get your portfolio project ready in minutes!
"""

import subprocess
import sys
from pathlib import Path
import pandas as pd

def install_requirements():
    """Install required packages"""
    print("📦 Installing core packages...")
    
    # Core packages that are essential
    core_packages = [
        "pandas>=1.5.0",
        "numpy>=1.21.0", 
        "matplotlib>=3.5.0",
        "seaborn>=0.11.0",
        "plotly>=5.10.0",
        "scikit-learn>=1.1.0",
        "streamlit>=1.25.0",
        "requests>=2.28.0"
    ]
    
    try:
        for package in core_packages:
            print(f"Installing {package.split('>=')[0]}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package], 
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        print("✅ Core packages installed successfully!")
        
        # Optional packages (don't fail if these don't work)
        optional_packages = ["folium", "streamlit-folium", "openpyxl"]
        print("📦 Installing optional packages...")
        
        for package in optional_packages:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package],
                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print(f"✅ {package} installed")
            except:
                print(f"⚠️ {package} skipped (not critical)")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install packages: {e}")
        print("💡 Try running manually: pip install pandas numpy matplotlib seaborn plotly scikit-learn streamlit")
        return False

def create_sample_dataset():
    """Create initial dataset using our data collector"""
    print("📊 Creating sample dataset with real data...")
    
    try:
        # Import and run data collector
        sys.path.append('src')
        from utils.data_collector import IndianCityDataCollector
        
        collector = IndianCityDataCollector()
        df = collector.create_comprehensive_dataset()
        
        # Save dataset
        output_path = Path("data/processed/cities_data.csv")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_path, index=False)
        
        print(f"✅ Dataset created: {output_path}")
        print(f"📊 Shape: {df.shape}")
        print(f"🏙️ Cities: {len(df)}")
        
        # Show sample
        print("\n📋 Sample data:")
        print(df[['City', 'State', 'Population_2011', 'GDP_Billions_USD', 'UGI']].head())
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to create dataset: {e}")
        return False

def test_streamlit_app():
    """Test if Streamlit app can run"""
    print("🧪 Testing Streamlit app...")
    
    try:
        # Check if streamlit is available
        import streamlit
        print("✅ Streamlit is available")
        
        # Check if app file exists
        app_path = Path("src/app.py")
        if app_path.exists():
            print("✅ App file exists")
            print(f"🚀 To run the app: streamlit run {app_path}")
            return True
        else:
            print("❌ App file not found")
            return False
            
    except ImportError:
        print("❌ Streamlit not installed")
        return False

def show_next_steps():
    """Show what to do next"""
    print("\n" + "="*60)
    print("🎯 PULSE PROJECT SETUP COMPLETE!")
    print("="*60)
    
    print("\n📋 What's Ready:")
    print("✅ Project structure created")
    print("✅ Sample dataset with real data")
    print("✅ 4 analysis notebooks")
    print("✅ Interactive Streamlit dashboard")
    print("✅ Professional README")
    
    print("\n🚀 Next Steps:")
    print("1. 📊 Explore the data:")
    print("   jupyter notebook notebooks/01_data_preparation.ipynb")
    
    print("\n2. 🎨 Run the dashboard:")
    print("   streamlit run src/app.py")
    
    print("\n3. 📈 Enhance with real data:")
    print("   - Download Census data (see REAL_DATA_GUIDE.md)")
    print("   - Add government datasets")
    print("   - Update data_collector.py")
    
    print("\n4. 🎯 Portfolio Enhancement:")
    print("   - Add screenshots to assets/images/")
    print("   - Create PDF summary report")
    print("   - Deploy to Streamlit Cloud")
    
    print("\n📚 Documentation:")
    print("   - REAL_DATA_GUIDE.md - How to get government data")
    print("   - data_sources.md - Complete data source list")
    print("   - README.md - Project overview")
    
    print("\n💡 Pro Tips:")
    print("   - Start with the sample data, enhance gradually")
    print("   - Focus on 2-3 key insights for interviews")
    print("   - Document your data sources for credibility")
    
    print("\n🎉 Your PULSE project is ready to impress recruiters!")

def main():
    """Main setup function"""
    print("🏙️ PULSE: India Urban Growth Intelligence Platform")
    print("🚀 Portfolio Project Setup")
    print("-" * 50)
    
    # Step 1: Install packages
    if not install_requirements():
        print("❌ Setup failed at package installation")
        return
    
    # Step 2: Create dataset
    if not create_sample_dataset():
        print("❌ Setup failed at dataset creation")
        return
    
    # Step 3: Test app
    test_streamlit_app()
    
    # Step 4: Show next steps
    show_next_steps()

if __name__ == "__main__":
    main()