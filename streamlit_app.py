import streamlit as st
import random
import time

st.set_page_config(layout="wide")
st.title("Live Option Chain (Simulated)")

REFRESH_SEC = 2
st.caption(f"Auto refresh every {REFRESH_SEC} seconds")

# ───────────── Base Strikes ─────────────
strikes = [21800, 21900, 22000, 22100, 22200, 22300, 22400]

# ───────────── Random Generator ─────────────
def gen_option():
    open_price = random.randint(40, 180)
    ltp = max(1, open_price + random.randint(-15, 15))
    oi = random.randint(50_000, 180_000)
    return open_price, ltp, oi

puts = {}
calls = {}

for s in strikes:
    p_open, p_ltp, p_oi = gen_option()
    c_open, c_ltp, c_oi = gen_option()

    puts[s] = {"Open": p_open, "LTP": p_ltp, "OI": p_oi}
    calls[s] = {"Open": c_open, "LTP": c_ltp, "OI": c_oi}

# ───────────── Max OI ─────────────
max_oi = max(
    max(v["OI"] for v in puts.values()),
    max(v["OI"] for v in calls.values())
)

# ───────────── Build Table ─────────────
rows = []

for strike in strikes:
    p = puts[strike]
    c = calls[strike]

    p_chg = p["LTP"] - p["Open"]
    c_chg = c["LTP"] - c["Open"]

    rows.append({
        "PUT OI %": round((p["OI"] / max_oi) * 100, 2),
        "PUT OI": f'{p["OI"]:,}',
        "PUT Chg": round(p_chg, 2),
        "PUT %": round((p_chg / p["Open"]) * 100, 2),
        "PUT LTP": p["LTP"],

        "Strike": strike,

        "CALL LTP": c["LTP"],
        "CALL %": round((c_chg / c["Open"]) * 100, 2),
        "CALL Chg": round(c_chg, 2),
        "CALL OI": f'{c["OI"]:,}',
        "CALL OI %": round((c["OI"] / max_oi) * 100, 2),
    })

# ───────────── Render ─────────────
st.dataframe(
    rows,
    use_container_width=True,
    height=420,
    column_order=[
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
    ],
    column_config={
        "PUT OI %": st.column_config.ProgressColumn("PUT OI", 0, 100),
        "CALL OI %": st.column_config.ProgressColumn("CALL OI", 0, 100),
        "PUT Chg": st.column_config.NumberColumn("PUT Chg", format="+%.2f"),
        "PUT %": st.column_config.NumberColumn("PUT %", format="+%.2f%%"),
        "CALL Chg": st.column_config.NumberColumn("CALL Chg", format="+%.2f"),
        "CALL %": st.column_config.NumberColumn("CALL %", format="+%.2f%%"),
    }
)

# ───────────── Safe Auto Refresh ─────────────
time.sleep(REFRESH_SEC)
st.experimental_rerun()
