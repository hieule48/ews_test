import streamlit as st
import pandas as pd

st.set_page_config(page_title="Screening and Analytics", layout="wide", page_icon="🏦")

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* White background everywhere */
body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main, .block-container,
section.main > div {
    background-color: #ffffff !important;
}

/* Sidebar white */
[data-testid="stSidebar"],
[data-testid="stSidebar"] > div {
    background-color: #ffffff !important;
    border-right: 1px solid #e0e0e0;
}

/* Header */
.header-title {
    font-size: 1.25rem; font-weight: 700; color: #1a1a2e;
    padding-bottom: 6px; margin-bottom: 0;
}

/* Avatar fixed top-right */
.avatar-fixed {
    position: fixed; top: 14px; right: 20px; z-index: 9999;
    width: 42px; height: 42px; border-radius: 50%;
    border: 2px solid #555; background: #fff;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.4rem; cursor: pointer;
    box-shadow: 0 2px 6px rgba(0,0,0,0.15);
}

/* Color cells */
.cell-red    { background:#e53935; color:#fff; border-radius:3px; text-align:center; padding:4px 0; }
.cell-yellow { background:#FDD835; color:#333; border-radius:3px; text-align:center; padding:4px 0; }
.cell-green  { background:#43A047; color:#fff; border-radius:3px; text-align:center; padding:4px 0; }
.cell-na     { background:#e0e0e0; color:#999; border-radius:3px; text-align:center; padding:4px 0; }

/* Table */
table.ranking-table { border-collapse: collapse; width: 100%; font-size: 0.88rem; }
table.ranking-table th {
    background: #f5f5f5; border: 1px solid #ddd; padding: 6px 10px;
    text-align: center; font-weight: 600; color: #333;
}
table.ranking-table td { border: 1px solid #ddd; padding: 4px 8px; }
table.ranking-table td.name-cell { text-align: left; font-weight: 500; padding-left: 12px; }
table.ranking-table td.no-cell   { text-align: center; color: #666; }

/* Tooltip */
.tooltip-wrap {
    display: inline-block; position: relative; cursor: default;
    vertical-align: middle;
}
.info-icon {
    color: #6c63ff; font-size: 0.78rem; font-weight: 700;
    border: 1.5px solid #6c63ff; border-radius: 50%;
    padding: 0 4px; margin-left: 4px;
    display: inline-block; line-height: 1.5; vertical-align: middle;
}
.tooltip-wrap .tooltip-box {
    display: none;
    position: absolute; left: 110%; top: -10px;
    background: #fff; border: 1px solid #ccc;
    border-radius: 6px; padding: 10px 14px;
    width: 290px; font-size: 0.8rem; color: #333;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    z-index: 9999; line-height: 1.65;
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
</style>

<!-- Fixed avatar -->
<div class="avatar-fixed">👤</div>
""", unsafe_allow_html=True)

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_excel("Bank_ranking.xlsx")
    df.columns = ["Bank", "Year", "ZScore"]
    df["Year"] = df["Year"].astype(int)
    return df

df = load_data()
all_banks = sorted(df["Bank"].unique().tolist())
all_years = list(range(2010, 2025))

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<div class="header-title">Screening and Analytics</div>', unsafe_allow_html=True)
st.markdown('<hr style="margin-top:4px;margin-bottom:16px;border-color:#1a1a2e">', unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### Filters")

    # ── 1. Institutions ───────────────────────────────────────────────────────
    with st.expander("**Institutions**", expanded=True):
        select_all_banks = st.checkbox("Select all", value=True, key="all_banks")
        if select_all_banks:
            selected_banks = all_banks
            for b in all_banks:
                st.checkbox(b, value=True, disabled=True, key=f"b_{b}")
        else:
            selected_banks = []
            for b in all_banks:
                if st.checkbox(b, value=False, key=f"b_{b}"):
                    selected_banks.append(b)

    # ── 2. Assessments ────────────────────────────────────────────────────────
    with st.expander("**Assessments**", expanded=False):
        st.checkbox("Current safety and soundness position", value=True, disabled=True, key="assess_1")
        st.markdown("""
        <div class="disabled-label"><input type="checkbox" disabled> Forecasting and early warnings</div>
        <div class="disabled-label"><input type="checkbox" disabled> Stress testing</div>
        """, unsafe_allow_html=True)

    # ── 3. Criteria ───────────────────────────────────────────────────────────
    with st.expander("**Criteria**", expanded=True):

        # Read current state for mutual exclusion
        camels_state    = st.session_state.get("crit_camels", False)
        stability_state = st.session_state.get("crit_stability", True)

        # Bank Stability row with tooltip
        col_stab, col_tip = st.columns([8, 1])
        with col_stab:
            crit_stability = st.checkbox(
                "Bank Stability",
                value=stability_state,
                disabled=camels_state,
                key="crit_stability"
            )
        with col_tip:
            st.markdown("""
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
            """, unsafe_allow_html=True)

        # CAMELS — disabled if Bank Stability ticked
        crit_camels = st.checkbox(
            "CAMELS",
            value=camels_state,
            disabled=crit_stability,
            key="crit_camels"
        )

        # CAMELS subsets — always visible, enabled only when CAMELS ticked
        camels_items = [
            ("Capital Adequacy (C)",          "s_capital"),
            ("Asset Quality (A)",             "s_asset"),
            ("Management (M)",                "s_mgmt"),
            ("Earnings (E)",                  "s_earn"),
            ("Liquidity (L)",                 "s_liq"),
            ("Sensitivity to market risk (S)","s_sens"),
        ]
        with st.container():
            st.markdown('<div class="camels-sub">', unsafe_allow_html=True)
            for label, key in camels_items:
                st.checkbox(label, value=False, disabled=not crit_camels, key=key)
            st.markdown('</div>', unsafe_allow_html=True)

        # Technical Default — always disabled
        st.markdown("""
        <div class="disabled-label" style="margin-top:6px">
          <input type="checkbox" disabled> <i>Technical Default</i>
        </div>
        """, unsafe_allow_html=True)

    # ── 4. Time ───────────────────────────────────────────────────────────────
    with st.expander("**Time**", expanded=True):
        select_all_years = st.checkbox("Select all", value=True, key="all_years")
        if select_all_years:
            selected_years = all_years
            for y in reversed(all_years):
                st.checkbox(str(y), value=True, disabled=True, key=f"y_{y}")
        else:
            selected_years = []
            for y in reversed(all_years):
                if st.checkbox(str(y), value=False, key=f"y_{y}"):
                    selected_years.append(y)

# ── Main area ────────────────────────────────────────────────────────────────
if not selected_banks:
    st.info("Vui lòng chọn ít nhất một ngân hàng.")
elif not selected_years:
    st.info("Vui lòng chọn ít nhất một năm.")
else:
    sorted_years = sorted(selected_years, reverse=True)

    filtered = df[df["Bank"].isin(selected_banks) & df["Year"].isin(selected_years)]
    pivot = filtered.pivot(index="Bank", columns="Year", values="ZScore")

    def color_cell(val):
        if pd.isna(val):
            return '<td><div class="cell-na">N/A</div></td>'
        v = int(val)
        if v == 0:   return '<td><div class="cell-red">0</div></td>'
        elif v == 1: return '<td><div class="cell-yellow">1</div></td>'
        else:        return '<td><div class="cell-green">2</div></td>'

    year_headers = "".join(f"<th>{y}</th>" for y in sorted_years)
    sub_headers  = "".join("<th style='color:#888;font-size:0.8rem;font-weight:400'>z</th>" for _ in sorted_years)

    rows_html = ""
    for i, bank in enumerate(sorted(selected_banks), 1):
        cells = ""
        for y in sorted_years:
            if bank in pivot.index and y in pivot.columns:
                cells += color_cell(pivot.loc[bank, y])
            else:
                cells += '<td><div class="cell-na">N/A</div></td>'
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
          <th rowspan="2">NO</th>
          <th rowspan="2">Bank Name</th>
          {year_headers}
        </tr>
        <tr>{sub_headers}</tr>
      </thead>
      <tbody>{rows_html}</tbody>
    </table>
    """
    st.markdown(html_table, unsafe_allow_html=True)

    # Summary stats
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    red_c    = int((filtered["ZScore"] == 0).sum())
    yellow_c = int((filtered["ZScore"] == 1).sum())
    green_c  = int((filtered["ZScore"] == 2).sum())
    col1.metric("🏦 Banks selected",  len(selected_banks))
    col2.metric("🔴 High Risk (z=0)", red_c)
    col3.metric("🟡 Moderate (z=1)",  yellow_c)
    col4.metric("🟢 Safe (z=2)",      green_c)
