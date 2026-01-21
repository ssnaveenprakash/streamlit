import streamlit as st

st.set_page_config(layout="wide")
st.title("Option Chain (Single Table)")

# ───────────── Hardcoded Data (7 PUT, 7 CALL) ─────────────
puts = [
    {"Strike": 22400, "Open": 42,  "LTP": 55,  "OI": 62000},
    {"Strike": 22300, "Open": 58,  "LTP": 71,  "OI": 81000},
    {"Strike": 22200, "Open": 76,  "LTP": 68,  "OI": 102000},
    {"Strike": 22100, "Open": 98,  "LTP": 112, "OI": 135000},
    {"Strike": 22000, "Open": 120, "LTP": 98,  "OI": 155000},
    {"Strike": 21900, "Open": 145, "LTP": 162, "OI": 140000},
    {"Strike": 21800, "Open": 175, "LTP": 192, "OI": 110000},
]

calls = [
    {"Strike": 21800, "Open": 185, "LTP": 210, "OI": 82000},
    {"Strike": 21900, "Open": 150, "LTP": 165, "OI": 95000},
    {"Strike": 22000, "Open": 120, "LTP": 145, "OI": 120000},
    {"Strike": 22100, "Open": 95,  "LTP": 88,  "OI": 98000},
    {"Strike": 22200, "Open": 70,  "LTP": 92,  "OI": 150000},
    {"Strike": 22300, "Open": 52,  "LTP": 46,  "OI": 76000},
    {"Strike": 22400, "Open": 38,  "LTP": 31,  "OI": 54000},
]

# ───────────── Precompute Max OI ─────────────
max_oi = max(
    max(p["OI"] for p in puts),
    max(c["OI"] for c in calls)
)

# ───────────── Build Single Table ─────────────
rows = []

for p, c in zip(puts, calls):
    p_change = p["LTP"] - p["Open"]
    c_change = c["LTP"] - c["Open"]

    rows.append({
        # PUT side
        "PUT OI %": round((p["OI"] / max_oi) * 100, 2),
        "PUT OI": f'{p["OI"]:,}',
        "PUT Chg": round(p_change, 2),
        "PUT %": round((p_change / p["Open"]) * 100, 2),
        "PUT LTP": p["LTP"],

        # STRIKE
        "Strike": p["Strike"],

        # CALL side
        "CALL LTP": c["LTP"],
        "CALL %": round((c_change / c["Open"]) * 100, 2),
        "CALL Chg": round(c_change, 2),
        "CALL OI": f'{c["OI"]:,}',
        "CALL OI %": round((c["OI"] / max_oi) * 100, 2),
    })

# ───────────── Column Order (IMPORTANT) ─────────────
column_order = [
    "PUT OI %",
    "PUT OI",
    "PUT Chg",
    "PUT %",
    "PUT LTP",
    "Strike",
    "CALL LTP",
    "CALL %",
    "CALL Chg",
    "CALL OI",
    "CALL OI %",
]

# ───────────── Render Table ─────────────
st.dataframe(
    rows,
    use_container_width=True,
    height=420,
    column_order=column_order,
    column_config={
        "PUT OI %": st.column_config.ProgressColumn(
            "PUT OI",
            min_value=0,
            max_value=100
        ),
        "CALL OI %": st.column_config.ProgressColumn(
            "CALL OI",
            min_value=0,
            max_value=100
        ),
        "PUT Chg": st.column_config.NumberColumn("PUT Chg", format="+%.2f"),
        "PUT %": st.column_config.NumberColumn("PUT %", format="+%.2f%%"),
        "CALL Chg": st.column_config.NumberColumn("CALL Chg", format="+%.2f"),
        "CALL %": st.column_config.NumberColumn("CALL %", format="+%.2f%%"),
    }
)
