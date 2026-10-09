import streamlit as st
from supabase import create_client

# Access secrets configured in Streamlit
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]

# Initialize Supabase client
supabase = create_client(url, key)
