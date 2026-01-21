import streamlit as st
import random
import calendar
from datetime import date

# ───────────────── Page Setup ─────────────────
st.set_page_config(layout="wide")
st.title("Trading panel")

# ───────────────── Base Strikes ─────────────────
strikes = [21800, 21900, 22000, 22100, 22200, 22300, 22400]

# ───────────────── Random Option Generator ─────────────────
def gen_option():
    open_price = random.randint(40, 180)
    ltp = max(1, open_price + random.randint(-15, 15))
    oi = random.randint(50_000, 180_000)
    return open_price, ltp, oi

@st.fragment
def nifty_heatmap_calendar():

    st.subheader("📊 NIFTY Yearly Heatmap")

    year = st.selectbox(
        "Select Year",
        options=[2022, 2023, 2024, 2025],
        index=2
    )

    cal = calendar.Calendar(firstweekday=0)

    # ---- Color mapping ----
    def color_for_move(pct):
        if pct >= 1.0:
            return "#2ecc71"   # strong green
        elif pct >= 0.3:
            return "#a9dfbf"   # light green
        elif pct <= -1.0:
            return "#e74c3c"   # strong red
        elif pct <= -0.3:
            return "#f5b7b1"   # light red
        else:
            return "#eeeeee"   # neutral

    def fake_pct():
        return round(random.uniform(-2, 2), 2)

    # ---- Month layout (12 columns) ----
    month_cols = st.columns(12)

    for m in range(1, 13):
        with month_cols[m - 1]:
            st.markdown(
                f"<div style='text-align:center;font-size:13px;margin-bottom:6px;'>"
                f"<b>{calendar.month_abbr[m]}</b></div>",
                unsafe_allow_html=True
            )

            weeks = cal.monthdayscalendar(year, m)

            for week in weeks:
                row_html = "<div style='display:flex;gap:3px;'>"
                for d in week:
                    if d == 0:
                        row_html += "<div style='width:18px;height:12px;'></div>"
                    else:
                        pct = fake_pct()
                        color = color_for_move(pct)
                        row_html += (
                            f"<div title='{pct:+.2f}%' "
                            f"style='width:18px;height:12px;"
                            f"background:{color};"
                            f"border-radius:2px;'></div>"
                        )
                row_html += "</div>"
                st.markdown(row_html, unsafe_allow_html=True)

# ───────────────── NIFTY CARD (AUTO REFRESH) ─────────────────
@st.fragment(run_every="1s")
def nifty_card():

    # Base price (simulate index)
    base_price = 22000

    # Simulate open & movement
    open_price = base_price + random.randint(-50, 50)
    ltp = open_price + random.randint(-120, 120)

    day_high = max(open_price, ltp) + random.randint(0, 40)
    day_low  = min(open_price, ltp) - random.randint(0, 40)

    change = ltp - open_price
    pct = (change / open_price) * 100

    # ───────── Card UI ─────────
    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        label="NIFTY 50",
        value=f"{ltp:,.2f}",
        delta=f"{change:+.2f}"
    )

    col2.metric(
        label="Today's % Move",
        value=f"{pct:+.2f}%"
    )

    col3.metric(
        label="Day Range",
        value=f"{ltp - open_price:+.2f}"
    )


# ───────────────── Fragment (AUTO REFRESH) ─────────────────
@st.fragment(run_every="1s")
def option_chain_fragment():

    # Generate data
    puts = {}
    calls = {}

    for strike in strikes:
        p_open, p_ltp, p_oi = gen_option()
        c_open, c_ltp, c_oi = gen_option()

        puts[strike] = {"Open": p_open, "LTP": p_ltp, "OI": p_oi}
        calls[strike] = {"Open": c_open, "LTP": c_ltp, "OI": c_oi}

    # Max OI (for progress bars)
    max_oi = max(
        max(v["OI"] for v in puts.values()),
        max(v["OI"] for v in calls.values())
    )

    # Build rows
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

    # Render table
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
            "PUT OI %": st.column_config.ProgressColumn(
                "PUT OI", min_value=0, max_value=100
            ),
            "CALL OI %": st.column_config.ProgressColumn(
                "CALL OI", min_value=0, max_value=100
            ),
            "PUT Chg": st.column_config.NumberColumn("PUT Chg", format="+%.2f"),
            "PUT %": st.column_config.NumberColumn("PUT %", format="+%.2f%%"),
            "CALL Chg": st.column_config.NumberColumn("CALL Chg", format="+%.2f"),
            "CALL %": st.column_config.NumberColumn("CALL %", format="+%.2f%%"),
        }
    )

# ───────────────── Run Fragment ─────────────────
nifty_card()
option_chain_fragment()
nifty_heatmap_calendar()
