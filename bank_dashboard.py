import streamlit as st
import pandas as pd

st.set_page_config(page_title="Screening and Analytics", layout="wide", page_icon="🏦")

# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "show_profile" not in st.session_state:
    st.session_state.show_profile = False

# ─────────────────────────────────────────────────────────────────────────────
# LOGIN PAGE
# ─────────────────────────────────────────────────────────────────────────────
if not st.session_state.logged_in:
    st.markdown("""
    <style>
    body, [data-testid="stAppViewContainer"], [data-testid="stMain"],
    .main, .block-container { background-color: #ffffff !important; padding: 0 !important; }
    header, [data-testid="stHeader"] { display: none !important; }
    [data-testid="stSidebar"] { display: none !important; }
    .login-wrap {
        display: flex; height: 100vh; width: 100%;
    }
    .login-left {
        flex: 1; background: #020b4a url('https://images.unsplash.com/photo-1557804506-669a67965ba0?w=1200') center/cover no-repeat;
        display: flex; flex-direction: column; justify-content: center;
        padding: 60px 56px;
        background-blend-mode: multiply;
    }
    .login-left h1 { color: #fff; font-size: 2.4rem; font-weight: 800; line-height: 1.25; margin-bottom: 18px; }
    .login-left p  { color: #cdd5f3; font-size: 1rem; line-height: 1.65; margin-bottom: 28px; max-width: 420px; }
    .learn-btn {
        display: inline-block; background: #f97316; color: #fff;
        padding: 12px 28px; border-radius: 8px; font-weight: 700;
        font-size: 0.95rem; text-decoration: none; width: fit-content;
    }
    .login-right {
        flex: 1; display: flex; align-items: center; justify-content: center;
        background: #fff;
    }
    .login-card {
        background: #fff; border-radius: 16px; padding: 48px 44px;
        box-shadow: 0 4px 32px rgba(0,0,0,0.10); width: 380px;
    }
    .login-card h2 { text-align: center; color: #1a3a8f; font-size: 1.8rem;
                     font-weight: 800; margin-bottom: 28px; }
    </style>

    <div class="login-wrap">
      <div class="login-left">
        <h1>Early Warning System for Banking Institutions</h1>
        <p>Get real-time alerts and insights to stay ahead of potential risks and threats to the financial system with our early warning system.</p>
        <a class="learn-btn" href="#">Learn More</a>
      </div>
      <div class="login-right">
        <div class="login-card">
          <h2>Login</h2>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Render inputs inside the right panel using Streamlit widgets
    with st.container():
        col_pad1, col_form, col_pad2 = st.columns([3, 2, 3])
        with col_form:
            st.markdown("<div style='height:220px'></div>", unsafe_allow_html=True)
            st.text_input("", placeholder="Username", key="login_user", label_visibility="collapsed")
            st.text_input("", placeholder="Password", type="password", key="login_pass", label_visibility="collapsed")
            if st.button("Login", use_container_width=True, type="primary"):
                st.session_state.logged_in = True
                st.rerun()
    st.stop()

# ─────────────────────────────────────────────────────────────────────────────
# DASHBOARD CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
body, [data-testid="stAppViewContainer"], [data-testid="stMain"],
.main, .block-container, section.main > div {
    background-color: #ffffff !important;
}
[data-testid="stSidebar"], [data-testid="stSidebar"] > div {
    background-color: #ffffff !important;
    border-right: 1px solid #e0e0e0;
}
.header-title {
    font-size: 1.2rem; font-weight: 700; color: #1a1a2e;
    padding-bottom: 5px;
}
/* Compact color cells */
.cell-red    { background:#e53935; border-radius:2px; width:38px; height:38px; display:inline-block; }
.cell-yellow { background:#FDD835; border-radius:2px; width:38px; height:38px; display:inline-block; }
.cell-green  { background:#43A047; border-radius:2px; width:38px; height:38px; display:inline-block; }
.cell-na     { background:#e0e0e0; border-radius:2px; width:38px; height:38px; display:inline-block; }

/* Table */
table.ranking-table { border-collapse: collapse; font-size: 0.85rem; }
table.ranking-table th {
    background: #f5f5f5; border: 1px solid #ddd; padding: 5px 8px;
    text-align: center; font-weight: 600; color: #333; white-space: nowrap;
}
table.ranking-table td {
    border: 1px solid #ddd; padding: 2px 3px;
    text-align: center; vertical-align: middle;
}
table.ranking-table td.name-cell {
    text-align: left; font-weight: 500; padding-left: 10px; white-space: nowrap; padding-right: 10px;
}
table.ranking-table td.no-cell { text-align: center; color: #666; padding: 2px 8px; }

/* Tooltip inline with label */
.stab-row { display: flex; align-items: center; gap: 4px; }
.tooltip-wrap { display: inline-block; position: relative; cursor: default; vertical-align: middle; }
.info-icon {
    color: #6c63ff; font-size: 0.75rem; font-weight: 700;
    border: 1.5px solid #6c63ff; border-radius: 50%;
    padding: 0 4px; display: inline-block; line-height: 1.5;
}
.tooltip-wrap .tooltip-box {
    display: none;
    position: absolute; left: 110%; top: -10px;
    background: #fff; border: 1px solid #ccc; border-radius: 6px;
    padding: 10px 14px; width: 290px; font-size: 0.8rem; color: #333;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15); z-index: 9999; line-height: 1.65;
}
.tooltip-wrap:hover .tooltip-box { display: block; }

/* Disabled items */
.disabled-label {
    color: #bbb; font-size: 0.88rem;
    display: flex; align-items: center; gap: 7px;
    padding: 2px 0; margin-left: 2px;
}
/* CAMELS sub-indent */
.camels-sub { margin-left: 22px; }

/* Avatar button */
.avatar-btn-wrap {
    position: fixed; top: 12px; right: 18px; z-index: 9999;
}
.avatar-btn-wrap button {
    width: 42px !important; height: 42px !important;
    border-radius: 50% !important; border: 2px solid #444 !important;
    background: #fff !important; font-size: 1.3rem !important;
    padding: 0 !important; box-shadow: 0 2px 8px rgba(0,0,0,0.15) !important;
    cursor: pointer !important;
}

/* Profile modal overlay */
.profile-overlay {
    position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
    background: rgba(0,0,0,0.35); z-index: 8888;
    display: flex; align-items: center; justify-content: center;
}
.profile-card {
    background: #fff; border-radius: 16px; padding: 40px 36px;
    width: 360px; box-shadow: 0 8px 40px rgba(0,0,0,0.18);
    text-align: center;
}
.profile-card h3 { color: #1a3a8f; font-size: 1.4rem; font-weight: 800; margin-bottom: 24px; }
.profile-card .btn-primary {
    display: block; width: 100%; padding: 13px;
    background: #2563eb; color: #fff; border-radius: 8px;
    font-weight: 700; font-size: 1rem; margin-bottom: 12px;
    border: none; cursor: pointer; text-decoration: none;
}
.profile-card .btn-outline {
    display: block; width: 100%; padding: 12px;
    background: #fff; color: #2563eb; border-radius: 8px;
    font-weight: 700; font-size: 1rem; margin-bottom: 12px;
    border: 2px solid #2563eb; cursor: pointer; text-decoration: none;
}
.profile-card .btn-close {
    color: #888; font-size: 0.95rem; cursor: pointer;
    background: none; border: none; margin-top: 4px;
}

/* Preview empty text */
.preview-empty {
    color: #555; font-size: 1rem; margin-top: 10px; line-height: 1.7;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_excel("Bank_ranking.xlsx")
    df.columns = ["Bank", "Year", "ZScore"]
    df["Year"] = df["Year"].astype(int)
    return df

df = load_data()
all_banks = sorted(df["Bank"].unique().tolist())
all_years = list(range(2010, 2025))

# ─────────────────────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<div class="header-title">Screening and Analytics</div>', unsafe_allow_html=True)
st.markdown('<hr style="margin-top:4px;margin-bottom:14px;border-color:#1a1a2e">', unsafe_allow_html=True)

# Avatar button (top-right via columns trick)
hcol1, hcol2 = st.columns([20, 1])
with hcol2:
    if st.button("👤", key="avatar_btn", help="Profile"):
        st.session_state.show_profile = not st.session_state.show_profile

# ─────────────────────────────────────────────────────────────────────────────
# PROFILE POPUP
# ─────────────────────────────────────────────────────────────────────────────
if st.session_state.show_profile:
    st.markdown("""
    <div class="profile-overlay">
      <div class="profile-card">
        <h3>Profile Actions</h3>
        <a class="btn-primary" href="#">Upload Template</a>
        <a class="btn-outline" href="#">Download Template</a>
      </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("✕  Close", key="close_profile"):
        st.session_state.show_profile = False
        st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR FILTERS
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### Filters")

    # 1. Institutions
    with st.expander("**Institutions**", expanded=True):
        select_all_banks = st.checkbox("Select all", value=False, key="all_banks")
        if select_all_banks:
            selected_banks = all_banks
            for b in all_banks:
                st.checkbox(b, value=True, disabled=True, key=f"b_{b}")
        else:
            selected_banks = []
            for b in all_banks:
                if st.checkbox(b, value=False, key=f"b_{b}"):
                    selected_banks.append(b)

    # 2. Assessments
    with st.expander("**Assessments**", expanded=False):
        st.checkbox("Current safety and soundness position", value=True, disabled=True, key="assess_1")
        st.markdown("""
        <div class="disabled-label"><input type="checkbox" disabled> Forecasting and early warnings</div>
        <div class="disabled-label"><input type="checkbox" disabled> Stress testing</div>
        """, unsafe_allow_html=True)

    # 3. Criteria
    with st.expander("**Criteria**", expanded=True):
        camels_state    = st.session_state.get("crit_camels", False)
        stability_state = st.session_state.get("crit_stability", False)

        # Bank Stability + tooltip (inline)
        col_cb, col_tip = st.columns([6, 1])
        with col_cb:
            crit_stability = st.checkbox(
                "Bank Stability",
                value=stability_state,
                disabled=camels_state,
                key="crit_stability"
            )
        with col_tip:
            st.markdown("""
            <div style="margin-top:6px">
            <div class="tooltip-wrap">
              <span class="info-icon">i</span>
              <div class="tooltip-box">
                <b>Measured using the Z-score</b>, which captures the buffer a bank has against insolvency:<br><br>
                (ROA + Equity/Assets) / σ_ROA (3 years)<br><br>
                🔴 <b>High risk (Red):</b> Bottom 10% of banks with the lowest Z-scores<br>
                🟡 <b>Medium risk (Yellow):</b> Next 40% of banks<br>
                🟢 <b>Low risk (Green):</b> Remaining 50% of banks
              </div>
            </div>
            </div>
            """, unsafe_allow_html=True)

        # CAMELS
        crit_camels = st.checkbox(
            "CAMELS",
            value=camels_state,
            disabled=crit_stability,
            key="crit_camels"
        )

        camels_items = [
            ("Capital Adequacy (C)",           "s_capital"),
            ("Asset Quality (A)",              "s_asset"),
            ("Management (M)",                 "s_mgmt"),
            ("Earnings (E)",                   "s_earn"),
            ("Liquidity (L)",                  "s_liq"),
            ("Sensitivity to market risk (S)", "s_sens"),
        ]
        st.markdown('<div class="camels-sub">', unsafe_allow_html=True)
        for label, key in camels_items:
            st.checkbox(label, value=False, disabled=not crit_camels, key=key)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="disabled-label" style="margin-top:6px">
          <input type="checkbox" disabled> <i>Technical Default</i>
        </div>
        """, unsafe_allow_html=True)

    # 4. Time
    with st.expander("**Time**", expanded=True):
        select_all_years = st.checkbox("Select all", value=False, key="all_years")
        if select_all_years:
            selected_years = all_years
            for y in reversed(all_years):
                st.checkbox(str(y), value=True, disabled=True, key=f"y_{y}")
        else:
            selected_years = []
            for y in reversed(all_years):
                if st.checkbox(str(y), value=False, key=f"y_{y}"):
                    selected_years.append(y)

# ─────────────────────────────────────────────────────────────────────────────
# MAIN AREA
# ─────────────────────────────────────────────────────────────────────────────
criteria_selected = crit_stability or crit_camels

st.markdown("**Preview (selected items):**")

if not selected_banks or not criteria_selected:
    st.markdown(
        '<p class="preview-empty">Please select at least one institution and at least one criteria '
        '(e.g., Z-Score or a CAMELS component) to see the preview.</p>',
        unsafe_allow_html=True
    )
elif not selected_years:
    st.markdown('<p class="preview-empty">Please select at least one year.</p>', unsafe_allow_html=True)
else:
    sorted_years = sorted(selected_years, reverse=True)
    filtered = df[df["Bank"].isin(selected_banks) & df["Year"].isin(selected_years)]
    pivot = filtered.pivot(index="Bank", columns="Year", values="ZScore")

    def color_cell(val):
        if pd.isna(val):
            return '<td><div class="cell-na"></div></td>'
        v = int(val)
        if v == 0:   return '<td><div class="cell-red"></div></td>'
        elif v == 1: return '<td><div class="cell-yellow"></div></td>'
        else:        return '<td><div class="cell-green"></div></td>'

    year_headers = "".join(f"<th>{y}</th>" for y in sorted_years)

    rows_html = ""
    for i, bank in enumerate(sorted(selected_banks), 1):
        cells = ""
        for y in sorted_years:
            if bank in pivot.index and y in pivot.columns:
                cells += color_cell(pivot.loc[bank, y])
            else:
                cells += '<td><div class="cell-na"></div></td>'
        rows_html += f"""
        <tr>
          <td class="no-cell">{i}</td>
          <td class="name-cell">{bank}</td>
          {cells}
        </tr>"""

    html_table = f"""
    <table class="ranking-table">
      <thead>
        <tr>
          <th>NO</th>
          <th>Bank Name</th>
          {year_headers}
        </tr>
      </thead>
      <tbody>{rows_html}</tbody>
    </table>
    """
    st.markdown(html_table, unsafe_allow_html=True)

    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    red_c    = int((filtered["ZScore"] == 0).sum())
    yellow_c = int((filtered["ZScore"] == 1).sum())
    green_c  = int((filtered["ZScore"] == 2).sum())
    col1.metric("🏦 Banks selected",  len(selected_banks))
    col2.metric("🔴 High Risk (z=0)", red_c)
    col3.metric("🟡 Moderate (z=1)",  yellow_c)
    col4.metric("🟢 Safe (z=2)",      green_c)
