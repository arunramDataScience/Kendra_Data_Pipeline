import streamlit as st
import boto3
import time

# -----------------------------
# AWS Kendra Client Setup
# -----------------------------
REGION = "us-east-1"  # your region
INDEX_ID = "4f781be0-e3b2-4fda-91e1-5ea00b88a189"  # copy from Kendra console

kendra = boto3.client("kendra", region_name=REGION)

# -----------------------------
# Streamlit Config and Custom CSS
# -----------------------------
st.set_page_config(
    page_title="Unified Search - HSSUS & SewaUSA",
    page_icon="🔍",
    layout="wide"
)

st.markdown("""
    <style>
        /* Gradient Header */
        .gradient-header {
            background: linear-gradient(90deg, #2e8b57, #0b3d91);
            padding: 1.5rem;
            border-radius: 12px;
            text-align: center;
            color: white;
            font-size: 2.2rem;
            font-weight: 700;
            margin-bottom: 2rem;
        }

        /* Card Style for Results */
        .result-card {
            background-color: var(--background-color-secondary, #1e1e1e);
            border-radius: 10px;
            padding: 1rem 1.5rem;
            margin-bottom: 1.2rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.15);
        }

        /* Search summary bar */
        .summary-bar {
            background-color: rgba(0, 150, 250, 0.1);
            border: 1px solid rgba(0, 150, 250, 0.3);
            padding: 0.6rem 1rem;
            border-radius: 8px;
            margin: 1rem 0;
            font-weight: 600;
        }

        @media (prefers-color-scheme: dark) {
            :root {
                --background-color-secondary: #2a2a2a;
                --text-color: #f0f0f0;
            }
        }

        @media (prefers-color-scheme: light) {
            :root {
                --background-color-secondary: #f9f9f9;
                --text-color: #222;
            }
        }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# Header
# -----------------------------
st.markdown("<div class='gradient-header'>🔍 Unified Search for HSSUS & SewaUSA</div>", unsafe_allow_html=True)
st.caption("✨ Powered by Amazon Kendra | Built by Arun")

# -----------------------------
# Input Section
# -----------------------------
col1, col2 = st.columns([3, 1])
with col1:
    query = st.text_input("Enter your question:", placeholder="e.g. upcoming events, service programs, or volunteer opportunities...")
with col2:
    source_filter = st.selectbox("Search in:", ["Both", "HSSUS", "SewaUSA"])
search_btn = st.button("Search")

# -----------------------------
# Search Logic
# -----------------------------
if search_btn and query:
    start_time = time.time()
    with st.spinner("🔎 Searching AWS Kendra..."):
        try:
            response = kendra.query(IndexId=INDEX_ID, QueryText=query)
            end_time = time.time()
            duration = end_time - start_time

            # Calculate result count
            total_results = len(response.get("ResultItems", []))

            # Summary Bar
            st.markdown(f"""
                <div class='summary-bar'>
                    🔎 <b>{total_results}</b> results found in <b>{duration:.2f}</b> seconds 
                    (Filter: <b>{source_filter}</b>)
                </div>
            """, unsafe_allow_html=True)

            # Results
            if "ResultItems" in response and total_results > 0:
                for item in response["ResultItems"]:
                    title = item.get("DocumentTitle", {}).get("Text", "Untitled")
                    link = item.get("DocumentURI", "")
                    snippet = item.get("DocumentExcerpt", {}).get("Text", "")
                    domain = "HSSUS" if "hssus.org" in link else "SewaUSA" if "sewausa.org" in link else "Unknown"

                    # Apply Source Filter
                    if source_filter != "Both" and source_filter.lower() not in domain.lower():
                        continue

                    # Display as Card
                    st.markdown(f"""
                        <div class='result-card'>
                            <h4><a href='{link}' target='_blank'>{title}</a></h4>
                            <b>🌐 Source:</b> {domain}<br>
                            <p>{snippet}</p>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("No results found. Try another query or check filter selection.")

        except Exception as e:
            st.error(f"⚠️ Error: {e}")
