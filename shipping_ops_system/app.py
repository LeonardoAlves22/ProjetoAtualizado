import streamlit as st

from database.database import init_db
from ui.dashboard import render_dashboard

from services.vessel_loader import load_vessels
from services.prospect_engine import process_prospects

from services.free_pratique_checker import check_free_pratique
from services.anuencia_checker import check_entry_clearance, check_departure_clearance
from services.remessa_checker import check_remessa

init_db()

st.sidebar.title("System Control")

if st.sidebar.button("Run Intelligence Scan"):

    check_free_pratique()
    check_entry_clearance()
    check_departure_clearance()
    check_remessa()

    st.success("Operational checks completed")

if st.sidebar.button("Load Vessel List"):
    vessels = load_vessels()
    st.success("Vessels loaded")

if st.sidebar.button("Run Prospect Scan"):
    vessels = load_vessels()
    process_prospects(vessels["SLZ"] + vessels["BELEM"])
    st.success("Prospects processed")

render_dashboard()

import streamlit as st

from database.database import init_db
from ui.dashboard import render_dashboard

from services.vessel_loader import load_vessels
from services.prospect_engine import process_prospects

from services.free_pratique_checker import check_free_pratique
from services.anuencia_checker import check_entry_clearance, check_departure_clearance
from services.remessa_checker import check_remessa

init_db()

st.sidebar.title("System Control")

if st.sidebar.button("Run Intelligence Scan"):

    check_free_pratique()
    check_entry_clearance()
    check_departure_clearance()
    check_remessa()

    st.success("Operational checks completed")

if st.sidebar.button("Load Vessel List"):
    vessels = load_vessels()
    st.success("Vessels loaded")

if st.sidebar.button("Run Prospect Scan"):
    vessels = load_vessels()
    process_prospects(vessels["SLZ"] + vessels["BELEM"])
    st.success("Prospects processed")

render_dashboard()
