import json
from pathlib import Path
import pandas as pd
import streamlit as st
from models.inventory_optimization import build_inventory_policies
from models.ai_demand_forecasting import create_future_forecast
from models.ai_supplier_risk_agent import score_suppliers
from models.ai_document_parser import parse_manifest_text
from utils.io import RAW, OUTPUT

st.set_page_config(page_title='Supply Chain AI Optimizer', page_icon='🚚', layout='wide')
st.title('🚚 Supply Chain Optimization & AI Risk Copilot')
st.caption('Inventory optimization · demand forecasting · supplier risk · OCR document parsing')

page = st.sidebar.radio('Navigation', ['Executive Overview','Demand Forecast','Supplier Risk','Inventory Policy','Manifest Parser'])

if page == 'Executive Overview':
    suppliers = pd.read_csv(RAW/'suppliers_master_data.csv')
    demand = pd.read_csv(RAW/'customer_orders_demand.csv')
    c1,c2,c3 = st.columns(3)
    c1.metric('Suppliers', len(suppliers))
    c2.metric('SKUs', demand['sku'].nunique())
    c3.metric('Historical Orders', len(demand))
    st.info('Run `python scripts/run_pipeline.py` to refresh all AI recommendations and output files.')

elif page == 'Demand Forecast':
    with st.spinner('Training model and forecasting demand...'):
        forecast = create_future_forecast(90)
    st.dataframe(forecast, use_container_width=True)
    chart = forecast.groupby('order_date')['forecast_quantity'].sum().reset_index()
    st.line_chart(chart, x='order_date', y='forecast_quantity')

elif page == 'Supplier Risk':
    risk = score_suppliers()
    st.dataframe(risk[['supplier_name','country','operational_risk_score','risk_level','recommended_action']], use_container_width=True)
    st.bar_chart(risk, x='supplier_name', y='operational_risk_score')

elif page == 'Inventory Policy':
    policies = build_inventory_policies(pd.read_csv(RAW/'customer_orders_demand.csv'), pd.read_csv(RAW/'suppliers_master_data.csv'))
    st.dataframe(policies, use_container_width=True)

elif page == 'Manifest Parser':
    text = st.text_area('Paste manifest/OCR text', height=220, value=(RAW/'shipping_manifests_scans/sample_manifest.txt').read_text())
    if st.button('Parse manifest'):
        st.json(parse_manifest_text(text))
