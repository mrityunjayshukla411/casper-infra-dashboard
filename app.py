import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(
    page_title="CASPER Infrastructure Dashboard",
    page_icon="🖥️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
        margin: 0.5rem 0;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #1f77b4;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #666;
        margin-top: 0.25rem;
    }
</style>
""", unsafe_allow_html=True)

# Main title
st.title("🖥️ CASPER Infrastructure Resource Distribution")

# Infrastructure data
infrastructure_data = {
    'Machine name': ['ISCA', 'MICRO', 'HPCA', 'USEC', 'ASPLOS', 'usenix', 'sharcserver1', 'dhristi'],
    'Physical location': ['Kresit server room (3rd floor)', 'Kresit server room (3rd floor)', 
                         'Kresit server room (basement)', 'Kresit server room (basement)',
                         'Kresit server room (conference room)',
                         'Kresit server room (basement)', 'Kresit server room (3rd floor)',
                         'Kresit server room (basement)'],
    'Threads': [96, 96, 96, 48, 96, 128, 64, 512],
    'Storage(nvme)': ['1T', '1T', '1T', '1T', '1T', '2T', '406G', '1T'],
    'Storage (hard disk)': ['4T', '4T', '2T', '6T', '2T', '10T', '18T', '20T'],
    'RAM': [128, 128, 128, 128, 204, 64, 64, 512],  # in GB
    'Swap': ['119G', '119G', '230G', '64G', '93G', '93G', '64G', '128G'],
    'GPU': ['', '', '', '', '', 'NVIDIA RTX A6000', 'AMD RX7990 XT', '']
}

df = pd.DataFrame(infrastructure_data)

# Calculate summary statistics
total_machines = len(df)
total_threads = df['Threads'].sum()
total_ram = df['RAM'].dropna().sum()
gpu_machines = len([gpu for gpu in df['GPU'] if gpu.strip() != ''])

# CASPER Infrastructure Summary
st.header("📊 CASPER Infrastructure Summary")

# First row: Total Threads and Total RAM
col1, col2 = st.columns(2)

with col1:
    st.metric(
        label="Total Threads", 
        value=f"{total_threads:,}",
        help="Combined CPU threads across all machines"
    )

with col2:
    st.metric(
        label="Total RAM", 
        value=f"{int(total_ram):,}GB",
        help="Combined RAM across all machines (excluding trustlab)"
    )

# Second row: Total Machines and GPU Machines
col3, col4 = st.columns(2)

with col3:
    st.metric(
        label="Total Machines", 
        value=total_machines,
        help="Total number of machines in the infrastructure"
    )

with col4:
    st.metric(
        label="GPU Machines", 
        value=gpu_machines,
        help="Number of machines with dedicated GPUs"
    )

st.markdown("---")

# Create pie charts
st.header("📈 Resource Distribution Charts")

# Prepare data for pie charts
threads_data = df[['Machine name', 'Threads']].copy()
ram_data = df[['Machine name', 'RAM']].dropna().copy()

# Define colors for consistency
colors = ['#8884d8', '#82ca9d', '#ffc658', '#ff7c7c', '#8dd1e1', 
          '#d084d0', '#ffb347', '#87ceeb', '#98fb98']

# Create two columns for pie charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("🔧 CPU Threads Distribution")
    
    # Create threads pie chart
    fig_threads = px.pie(
        threads_data, 
        values='Threads', 
        names='Machine name',
        title=f'Total: {total_threads:,} Threads',
        color_discrete_sequence=colors
    )
    
    fig_threads.update_traces(
        textposition='inside', 
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Threads: %{value}<br>Percentage: %{percent}<extra></extra>'
    )
    
    fig_threads.update_layout(
        showlegend=True,
        height=500,
        title_x=0.5,
        font=dict(size=12)
    )
    
    st.plotly_chart(fig_threads, use_container_width=True)

with col2:
    st.subheader("💾 RAM Distribution")
    
    # Create RAM pie chart
    fig_ram = px.pie(
        ram_data, 
        values='RAM', 
        names='Machine name',
        title=f'Total: {int(total_ram):,}GB RAM',
        color_discrete_sequence=colors
    )
    
    fig_ram.update_traces(
        textposition='inside', 
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>RAM: %{value}GB<br>Percentage: %{percent}<extra></extra>'
    )
    
    fig_ram.update_layout(
        showlegend=True,
        height=500,
        title_x=0.5,
        font=dict(size=12)
    )
    
    st.plotly_chart(fig_ram, use_container_width=True)

st.markdown("---")

# Additional insights
st.header("🔍 Infrastructure Insights")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Top 3 Machines by Threads")
    top_threads = df.nlargest(3, 'Threads')[['Machine name', 'Threads']]
    for idx, row in top_threads.iterrows():
        percentage = (row['Threads'] / total_threads) * 100
        st.write(f"**{row['Machine name']}**: {row['Threads']} threads ({percentage:.1f}%)")

with col2:
    st.subheader("Top 3 Machines by RAM")
    top_ram = df.dropna(subset=['RAM']).nlargest(3, 'RAM')[['Machine name', 'RAM']]
    for idx, row in top_ram.iterrows():
        percentage = (row['RAM'] / total_ram) * 100
        st.write(f"**{row['Machine name']}**: {int(row['RAM'])}GB ({percentage:.1f}%)")

# GPU Information
st.subheader("🎮 GPU-Enabled Machines")
gpu_machines_df = df[df['GPU'].str.strip() != ''][['Machine name', 'GPU']]
if not gpu_machines_df.empty:
    for idx, row in gpu_machines_df.iterrows():
        st.write(f"**{row['Machine name']}**: {row['GPU']}")
else:
    st.write("No GPU information available")

st.markdown("---")

# Data table
st.header("📋 Complete Infrastructure Data")
st.dataframe(
    df, 
    use_container_width=True,
    hide_index=True
)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; font-size: 0.9rem;'>"
    "CASPER Infrastructure Dashboard | Data as of latest update"
    "</div>", 
    unsafe_allow_html=True
)
