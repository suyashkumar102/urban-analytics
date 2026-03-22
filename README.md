# 🏙️ PULSE: India Urban Growth Intelligence Platform

*Comprehensive analysis of India's urban development through data-driven insights*

## 🎯 Project Overview

PULSE analyzes 100+ Indian cities across 5 key development pillars to compute an Urban Growth Intelligence (UGI) score. This platform provides actionable insights for urban planning, investment decisions, and policy formulation through advanced data science and interactive visualizations.


## 📊 Key Features

- **Comprehensive Dataset**: 100 Indian cities with 25+ development metrics
- **UGI Scoring System**: Proprietary algorithm across 5 pillars
- **Interactive Maps**: Geospatial analysis with clustering
- **ML Insights**: Predictive modeling for growth patterns
- **Real-time Dashboard**: Streamlit-powered analytics platform

## 🏗️ Project Structure

```
pulse-india-urban-intelligence/
├── data/
│   ├── raw/
│   └── processed/
│       └── cities_data.csv
├── notebooks/
│   ├── 01_data_preparation.ipynb
│   ├── 02_eda_and_visuals.ipynb
│   ├── 03_geospatial_analysis.ipynb
│   └── 04_ml_modeling.ipynb
├── src/
│   ├── app.py
│   ├── utils/
│   └── components/
├── assets/
│   └── images/
├── reports/
│   └── PULSE_Summary_Report.pdf
└── requirements.txt
```

## 🔍 Key Insights

- **Mumbai leads** with highest UGI score (87.3) driven by connectivity and economy
- **Tier-2 cities** show 23% higher growth potential than established metros
- **Southern states** dominate top 15 rankings with balanced development

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=flat&logo=plotly&logoColor=white)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-F7931E?style=flat&logo=scikit-learn&logoColor=white)

## ▶️ Quick Start

```bash
# Clone repository
git clone https://github.com/yourusername/pulse-india-urban-intelligence.git
cd pulse-india-urban-intelligence

# Install dependencies
pip install -r requirements.txt

# Run Streamlit app
streamlit run src/app.py

