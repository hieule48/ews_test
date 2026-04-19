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
# LOGIN PAGE  — single unified HTML/CSS layout, Streamlit widgets overlaid
# ─────────────────────────────────────────────────────────────────────────────
if not st.session_state.logged_in:
    st.markdown("""
    <style>
    /* Hide Streamlit chrome */
    header, [data-testid="stHeader"], [data-testid="stToolbar"],
    [data-testid="stDecoration"], footer { display:none !important; }
    [data-testid="stSidebar"] { display:none !important; }

    /* Full-viewport white canvas */
    body,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    .main { background:#fff !important; margin:0; padding:0 !important; }
    .block-container { padding:0 !important; max-width:100% !important; }

    /* ── Two-column login shell ── */
    .login-shell {
        display:flex; height:100vh; width:100%;
        position:fixed; top:0; left:0; z-index:0;
        pointer-events:none;          /* let Streamlit widgets on top receive clicks */
    }
    .login-left {
        flex:1;
        background: linear-gradient(135deg,#0a2472 0%,#0e4d92 60%,#1a78c2 100%);
        display:flex; flex-direction:column; justify-content:center;
        padding:60px 56px;
    }
    .login-left h1 {
        color:#fff; font-size:2.4rem; font-weight:800;
        line-height:1.25; margin-bottom:18px;
    }
    .login-left p  {
        color:#c8dff7; font-size:1rem; line-height:1.65;
        margin-bottom:28px; max-width:420px;
    }
    .learn-btn {
        display:inline-block; background:#f97316; color:#fff;
        padding:12px 28px; border-radius:8px; font-weight:700;
        font-size:0.95rem; text-decoration:none; pointer-events:all;
    }
    .login-right {
        flex:1; background:#fff;
    }

    /* ── Login card positioned in right half ── */
    /* We'll place it via a Streamlit column, but style its inner elements */
    div[data-testid="column"]:nth-of-type(2) {
        display:flex; flex-direction:column;
        align-items:center; justify-content:center;
    }
    .login-card-title {
        text-align:center; color:#1a3a8f; font-size:1.9rem;
        font-weight:800; margin-bottom:20px;
    }
    /* Override Streamlit button colour for Login */
    div[data-testid="stButton"] > button {
        background:#2563eb !important; color:#fff !important;
        border:none !important; border-radius:8px !important;
        font-weight:700 !important; font-size:1rem !important;
        padding:12px !important;
    }
    div[data-testid="stButton"] > button:hover {
        background:#1d4ed8 !important;
    }
    </style>

    <!-- Static two-column background shell -->
    <div class="login-shell">
      <div class="login-left">
        <h1>Early Warning System for Banking Institutions</h1>
        <p>Get real-time alerts and insights to stay ahead of potential risks
           and threats to the financial system with our early warning system.</p>
        <a class="learn-btn" href="#">Learn More</a>
      </div>
      <div class="login-right"></div>
    </div>
    """, unsafe_allow_html=True)

    # Streamlit columns on top of the shell — left col is transparent, right col has the form
    col_left, col_right = st.columns(2)

    with col_right:
        # Vertical centering: push down ~30vh worth of space
        st.markdown("<div style='height:28vh'></div>", unsafe_allow_html=True)
        st.markdown('<div class="login-card-title">Login</div>', unsafe_allow_html=True)

        # Card wrapper
        st.markdown("""
        <style>
        /* Give the right col's widgets a card look */
        section[data-testid="stMain"] > div > div > div:nth-child(2) .stTextInput input {
            border-radius:8px; padding:12px 14px; background:#f1f5f9;
            border:1px solid #e2e8f0; font-size:1rem;
        }
        </style>
        """, unsafe_allow_html=True)

        st.text_input("", placeholder="Username", key="login_user",
                      label_visibility="collapsed")
        st.text_input("", placeholder="Password", type="password",
                      key="login_pass", label_visibility="collapsed")

        if st.button("Login", use_container_width=True, key="login_btn"):
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
    background-color:#ffffff !important;
}
[data-testid="stSidebar"], [data-testid="stSidebar"] > div {
    background-color:#ffffff !important;
    border-right:1px solid #e0e0e0;
}
.header-title {
    font-size:1.2rem; font-weight:700; color:#1a1a2e; padding-bottom:5px;
}

/* ── Colour cells: fluid width, fixed height ── */
.cell-red    { background:#e53935; border-radius:3px; width:100%; height:36px; display:block; }
.cell-yellow { background:#FDD835; border-radius:3px; width:100%; height:36px; display:block; }
.cell-green  { background:#43A047; border-radius:3px; width:100%; height:36px; display:block; }
.cell-na     { background:#e0e0e0; border-radius:3px; width:100%; height:36px; display:block; }

/* ── Ranking table: fills full width ── */
table.ranking-table {
    border-collapse:collapse; width:100%; table-layout:fixed; font-size:0.82rem;
}
table.ranking-table th {
    background:#f5f5f5; border:1px solid #ddd; padding:5px 2px;
    text-align:center; font-weight:600; color:#333; white-space:nowrap;
    overflow:hidden; text-overflow:ellipsis;
}
table.ranking-table th.name-th  { width:130px; }
table.ranking-table th.no-th    { width:36px; }
table.ranking-table td {
    border:1px solid #ddd; padding:2px 2px;
    text-align:center; vertical-align:middle;
}
table.ranking-table td.name-cell {
    text-align:left; font-weight:500;
    padding-left:8px; white-space:nowrap;
    overflow:hidden; text-overflow:ellipsis;
}
table.ranking-table td.no-cell { text-align:center; color:#666; }

/* ── Tooltip ── */
.tooltip-wrap { display:inline-block; position:relative; cursor:default; vertical-align:middle; }
.info-icon {
    color:#6c63ff; font-size:0.75rem; font-weight:700;
    border:1.5px solid #6c63ff; border-radius:50%;
    padding:0 4px; display:inline-block; line-height:1.5; margin-left:3px;
}
.tooltip-wrap .tooltip-box {
    display:none; position:absolute; left:110%; top:-10px;
    background:#fff; border:1px solid #ccc; border-radius:6px;
    padding:10px 14px; width:290px; font-size:0.8rem; color:#333;
    box-shadow:0 4px 12px rgba(0,0,0,0.15); z-index:9999; line-height:1.65;
}
.tooltip-wrap:hover .tooltip-box { display:block; }

/* ── Disabled sidebar items ── */
.disabled-label {
    color:#bbb; font-size:0.88rem;
    display:flex; align-items:center; gap:7px;
    padding:3px 0; margin-left:2px;
}

/* ── CAMELS sub-items: indented ── */
.camels-sub { margin-left:28px; border-left:2px solid #e5e7eb; padding-left:8px; margin-top:2px; }

/* ── Profile overlay ── */
.profile-overlay {
    position:fixed; top:0; left:0; width:100vw; height:100vh;
    background:rgba(0,0,0,0.40); z-index:8888;
    display:flex; align-items:center; justify-content:center;
}
.profile-card {
    background:#fff; border-radius:16px; padding:40px 36px;
    width:380px; box-shadow:0 8px 40px rgba(0,0,0,0.18); text-align:center;
}
.profile-card h3 { color:#1a3a8f; font-size:1.4rem; font-weight:800; margin-bottom:24px; }
.profile-card .btn-primary {
    display:block; width:100%; padding:14px;
    background:#2563eb; color:#fff; border-radius:8px;
    font-weight:700; font-size:1rem; margin-bottom:12px;
    border:none; cursor:pointer; text-decoration:none;
}
.profile-card .btn-outline {
    display:block; width:100%; padding:13px;
    background:#fff; color:#2563eb; border-radius:8px;
    font-weight:700; font-size:1rem; margin-bottom:16px;
    border:2px solid #2563eb; cursor:pointer; text-decoration:none;
}

/* preview empty */
.preview-empty { color:#555; font-size:1rem; margin-top:10px; line-height:1.7; }
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

df        = load_data()
all_banks = sorted(df["Bank"].unique().tolist())
all_years = list(range(2010, 2025))

# ─────────────────────────────────────────────────────────────────────────────
# HEADER + AVATAR
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<div class="header-title">Screening and Analytics</div>', unsafe_allow_html=True)
st.markdown('<hr style="margin-top:4px;margin-bottom:14px;border-color:#1a1a2e">', unsafe_allow_html=True)

hcol1, hcol2 = st.columns([20, 1])
with hcol2:
    if st.button("👤", key="avatar_btn", help="Profile"):
        st.session_state.show_profile = not st.session_state.show_profile

# ─────────────────────────────────────────────────────────────────────────────
# PROFILE POPUP  — overlay HTML + Streamlit Close button inside the card
# ─────────────────────────────────────────────────────────────────────────────
if st.session_state.show_profile:
    st.markdown("""
    <div class="profile-overlay">
      <div class="profile-card">
        <h3>Profile Actions</h3>
        <a class="btn-primary" href="#">Upload Template</a>
        <a class="btn-outline" href="#">Download Template</a>
        <!-- Streamlit button will render just below this card via st.columns trick -->
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Place "Close" button centred in viewport using columns
    _, close_col, _ = st.columns([2, 1, 2])
    with close_col:
        # Extra top margin so the button lands inside the modal card visually
        st.markdown("<div style='margin-top:-110px'></div>", unsafe_allow_html=True)
        if st.button("Close", key="close_profile", use_container_width=True):
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

    # 2. Assessments  — first option tickable, other two greyed out
    with st.expander("**Assessments**", expanded=False):
        st.checkbox("Current Safety and Soundness Position", value=False, key="assess_1")
        st.markdown("""
        <div class="disabled-label"><input type="checkbox" disabled>
            <i>Forecasting and Early Warnings</i></div>
        <div class="disabled-label"><input type="checkbox" disabled>
            <i>Stress Testing</i></div>
        """, unsafe_allow_html=True)

    # 3. Criteria
    with st.expander("**Criteria**", expanded=True):
        camels_state    = st.session_state.get("crit_camels",    False)
        stability_state = st.session_state.get("crit_stability", False)

        # Bank Stability + inline "i" tooltip using HTML label trick
        # We render the checkbox label ourselves so the ℹ️ sits right next to the text
        st.markdown("""
        <style>
        /* Hide default label of the Bank Stability checkbox, we show our own */
        label[data-testid="stWidgetLabel"]:has(+ div #crit_stability) { display:none; }
        </style>
        """, unsafe_allow_html=True)

        # Row: checkbox | "Bank Stability i"
        bs_col, _ = st.columns([1, 0.01])
        with bs_col:
            crit_stability = st.checkbox(
                "Bank Stability",
                value=stability_state,
                disabled=camels_state,
                key="crit_stability"
            )

        # Overlay a custom label with tooltip immediately after
        st.markdown("""
        <div style="margin-top:-32px; margin-left:28px; font-size:0.9rem;
                    display:flex; align-items:center; gap:0; pointer-events:none;">
          <span>Bank Stability</span>
          <div class="tooltip-wrap" style="pointer-events:all">
            <span class="info-icon">i</span>
            <div class="tooltip-box">
              <b>Measured using the Z-score</b>, which captures the buffer
              a bank has against insolvency:<br><br>
              (ROA + Equity/Assets) / σ_ROA (3 years)<br><br>
              🔴 <b>High risk (Red):</b> Bottom 10% of banks with the lowest Z-scores<br>
              🟡 <b>Medium risk (Yellow):</b> Next 40% of banks<br>
              🟢 <b>Low risk (Green):</b> Remaining 50% of banks
            </div>
          </div>
        </div>
        <div style="height:6px"></div>
        """, unsafe_allow_html=True)

        # CAMELS — disabled when Bank Stability is ticked
        crit_camels = st.checkbox(
            "CAMELS",
            value=camels_state,
            disabled=crit_stability,
            key="crit_camels"
        )

        # CAMELS subsets — always visible, only enabled when CAMELS ticked
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

        # Technical Default — permanently disabled
        st.markdown("""
        <div class="disabled-label" style="margin-top:8px">
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
        '<p class="preview-empty">Please select at least one institution and at least one '
        'criteria (e.g., Z-Score or a CAMELS component) to see the preview.</p>',
        unsafe_allow_html=True
    )
elif not selected_years:
    st.markdown('<p class="preview-empty">Please select at least one year.</p>',
                unsafe_allow_html=True)
else:
    sorted_years = sorted(selected_years, reverse=True)
    n_years      = len(sorted_years)
    filtered     = df[df["Bank"].isin(selected_banks) & df["Year"].isin(selected_years)]
    pivot        = filtered.pivot(index="Bank", columns="Year", values="ZScore")

    def color_cell(val):
        if pd.isna(val):
            return '<td><div class="cell-na"></div></td>'
        v = int(val)
        if   v == 0: return '<td><div class="cell-red"></div></td>'
        elif v == 1: return '<td><div class="cell-yellow"></div></td>'
        else:        return '<td><div class="cell-green"></div></td>'

    # Year column width: distribute remaining space evenly
    # 130px name + 36px NO = 166px fixed; rest splits among years
    year_col_pct = f"calc((100% - 166px) / {n_years})"

    # Build col-group for uniform year widths
    colgroup = (
        '<col style="width:36px">'
        '<col style="width:130px">'
        + f'<col style="width:{year_col_pct}">' * n_years
    )

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
      <colgroup>{colgroup}</colgroup>
      <thead>
        <tr>
          <th class="no-th">NO</th>
          <th class="name-th">Bank Name</th>
          {year_headers}
        </tr>
      </thead>
      <tbody>{rows_html}</tbody>
    </table>
    """
    st.markdown(html_table, unsafe_allow_html=True)

    st.markdown("---")
    c1, c2, c3, c4 = st.columns(4)
    red_c    = int((filtered["ZScore"] == 0).sum())
    yellow_c = int((filtered["ZScore"] == 1).sum())
    green_c  = int((filtered["ZScore"] == 2).sum())
    c1.metric("🏦 Banks selected",  len(selected_banks))
    c2.metric("🔴 High Risk (z=0)", red_c)
    c3.metric("🟡 Moderate (z=1)",  yellow_c)
    c4.metric("🟢 Safe (z=2)",      green_c)
