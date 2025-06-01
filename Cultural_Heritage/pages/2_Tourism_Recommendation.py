import streamlit as st
import pandas as pd
import re
import streamlit.components.v1 as components
import base64
from utils import data_loaders
from utils.common_css import add_logo

st.set_page_config(page_title="🇮🇳 India Tourism Recommender", layout="wide")

add_logo("data/BGs/logo_app.png")

# ---------- DATA HANDLER ----------
class DataHandler:
    def __init__(self):
        self.places_df = data_loaders.load_places()

# ---------- SEARCH ----------
class SearchEngine:
    def __init__(self, df):
        self.df = df

    def search(self, query, state):
        filtered_df = self.df.copy()

        if not query.strip() and state != "All States":
            filtered_df = filtered_df[filtered_df['State'] == state]

        if query.strip():
            pattern = re.compile(re.escape(query.strip()), re.IGNORECASE)
            filtered_df = filtered_df[
                filtered_df['Name'].str.contains(pattern) |
                filtered_df['City'].str.contains(pattern) |
                filtered_df['State'].str.contains(pattern)
            ]

        return filtered_df

    def dynamic_filter(self, df, filters):
        for col, value in filters.items():
            if isinstance(value, list) and value:
                df = df[df[col].isin(value)]
            elif isinstance(value, tuple) and len(value) == 2:
                df = df[df[col].between(value[0], value[1])]
        return df

# ---------- UI ----------
class UI:
    def render(self, df, columns_to_display):
        if df.empty:
            st.warning("⚠️ No results found!")
            return

        view_mode = st.radio("View Mode", ["🃏 Card View", "📊 Table View"], horizontal=True)

        if view_mode == "📊 Table View":
            self._render_table(df, columns_to_display)
        else:
            self._render_cards(df, columns_to_display)

    def _render_cards(self, df, columns_to_display):
        card_html = """
        <style>
        .card-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 20px; padding: 10px; }
        .card {
            background: linear-gradient(to bottom right, #1c1c1c, #333);
            color: #fff; border-radius: 15px; padding: 20px;
            box-shadow: 0 6px 18px rgba(0,0,0,0.5);
            text-align: center; transition: 0.4s ease;
        }
        .card:hover { transform: scale(1.05); }
        .card h3 { font-family: 'Orbitron', sans-serif; font-size: 26px; margin: 10px; color: #FFD700; }
        .card p { font-size: 16px; }
        </style>
        <div class="card-grid">
        """
        for _, row in df.iterrows():
            card_html += "<div class='card'>"
            card_html += f"<h3>📍 {row['Name']}</h3><p>📌 {row['City']}, {row['State']}</p>"
            for col in columns_to_display:
                if col not in ['Name', 'City', 'State']:
                    card_html += f"<p><b>{col.replace('_',' ')}:</b> {row[col]}</p>"
            card_html += "</div>"
        card_html += "</div>"
        components.html(card_html, height=900, scrolling=True)

    def _render_table(self, df, columns_to_display):
        table_html = """
        <style>
        .table-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(450px, 1fr)); gap: 15px; padding: 15px; }
        .box {
            background: #1b1b1b; color: #fff;
            border: 2px solid #444; padding: 15px;
            border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.5);
            transition: 0.3s ease;
        }
        .box:hover { transform: scale(1.03); }
        h4 { color: #FFD700; font-family: 'Orbitron'; font-size: 22px; }
        </style>
        <div class='table-grid'>
        """
        for _, row in df.iterrows():
            table_html += "<div class='box'>"
            table_html += f"<h4>📍 {row['Name']}</h4><p>📌 {row['City']}, {row['State']}</p>"
            for col in columns_to_display:
                if col not in ['Name', 'City', 'State']:
                    table_html += f"<p><b>{col.replace('_',' ')}:</b> {row[col]}</p>"
            table_html += "</div>"
        table_html += "</div>"

        components.html(table_html, height=900, scrolling=True)

# ---------- MAIN APP ----------
class TourismApp:
    def __init__(self):
        self.data_handler = DataHandler()
        self.search_engine = SearchEngine(self.data_handler.places_df)
        self.ui = UI()

    def run(self):
        self._add_dashboard_background()
        self.dashboard()

    def _add_dashboard_background(self):
        image_path = "data/BGs/logo.png"
        with open(image_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
        st.markdown(f"""
            <style>
            .stApp {{
                background: linear-gradient(to bottom, rgba(0,0,0,0.6), rgba(0,0,0,0.7)), 
                            url("data:image/png;base64,{encoded}");
                background-size: cover;
                background-position: center;
            }}
            </style>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <style>
            section[data-testid="stSidebar"] {{
                background: linear-gradient(to bottom, rgba(0,0,0,0.85), rgba(0,0,0,0.85)), 
                            url("data:image/png;base64,{encoded}");
                background-position: center center;
                background-repeat: no-repeat;
                background-size: cover;
            }}
            </style>
        """, unsafe_allow_html=True)

    def dashboard(self):
        st.markdown("<h1 style='text-align:center;font-family:Orbitron;color:#FFD700;'>🌏 India Cultural & Tourism Explorer</h1>", unsafe_allow_html=True)

        query = st.text_input("🔎 Search")

        state_list = ["All States"] + sorted(self.data_handler.places_df["State"].unique())
        selected_state = st.selectbox("Select State", state_list)

        filtered_df = self.search_engine.search(query, selected_state)

        columns_available = [col for col in self.data_handler.places_df.columns if col not in ["Name", "City", "State"]]
        selected_cols = st.multiselect("Select additional fields to view:", columns_available, default=[])
        fields_to_display = ["Name", "City", "State"] + selected_cols

        with st.sidebar:
            filters = {}
            if selected_cols:
                st.header("⚙️ Advanced Filters")
            for field in selected_cols:
                if self.data_handler.places_df[field].dtype == "object":
                    options = sorted(self.data_handler.places_df[field].dropna().unique().tolist())
                    filters[field] = st.multiselect(f"{field}", options, default=[])
                elif self.data_handler.places_df[field].dtype in ['int64', 'float64']:
                    min_val = float(self.data_handler.places_df[field].min())
                    max_val = float(self.data_handler.places_df[field].max())
                    filters[field] = st.slider(f"{field}", min_val, max_val, (min_val, max_val))

            filtered_df = self.search_engine.dynamic_filter(filtered_df, filters)

        self.ui.render(filtered_df, fields_to_display)

# --------- RUN ------------
TourismApp().run()
