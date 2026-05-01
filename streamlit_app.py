import streamlit as st

st.set_page_config(page_title="Tax Negotiation Game")

st.title("Tax Negotiation Game")

# -------------------------
# Initialize state
# -------------------------
if "round" not in st.session_state:
    st.session_state.round = 1
    st.session_state.p1 = None
    st.session_state.p2 = None
    st.session_state.history = []
    st.session_state.final = None

st.write("Baseline: $300M taxable purchase")

# -------------------------
# ROUND 1
# -------------------------
if st.session_state.round == 1:
    st.header("Round 1 — Seller acts first")

    price = st.number_input("Enter seller offer ($M)", 0, 400, 275)

    if st.button("Submit Round 1"):
        if 270 <= price <= 275:
            st.success("Accepted: price compensates buyer for moving off taxable baseline")
            st.session_state.p1 = price
            st.session_state.history.append(f"Round 1: {price} → accepted")
            st.session_state.round = 2
        else:
           else:
    st.session_state.history.append(f"Round 1: {offer:.0f} → rejected")
    st.error("Rejected. Seller may make another offer. The game only ends if the parties stop negotiating.")

# -------------------------
# ROUND 2
# -------------------------
elif st.session_state.round == 2:
    st.header("Round 2 — Buyer acts first")

    st.write(f"Round 1 Price: ${st.session_state.p1}M")

    price = st.number_input("Enter buyer offer ($M)", 0, 400, st.session_state.p1 + 12)

    if st.button("Submit Round 2"):
        if st.session_state.p1 + 10 <= price <= st.session_state.p1 + 15:
            st.success("Accepted: seller compensated for partial tax tradeoff")
            st.session_state.p2 = price
            st.session_state.history.append(f"Round 2: {price} → accepted")
        else:
            st.warning("Rejected: revert to Round 1 price")
            st.session_state.p2 = st.session_state.p1
            st.session_state.history.append(f"Round 2: {price} → rejected")

        st.session_state.round = 3

# -------------------------
# ROUND 3
# -------------------------
elif st.session_state.round == 3:
    st.header("Round 3 — Buyer acts first")

    st.write(f"Current Price: ${st.session_state.p2}M")

    price = st.number_input("Enter buyer final offer ($M)", 0, 400, st.session_state.p2 + 5)

    if st.button("Submit Round 3"):
        if st.session_state.p2 + 4 <= price <= st.session_state.p2 + 7:
            st.success("Accepted: seller compensated for added complexity")
            st.session_state.final = price
            st.session_state.history.append(f"Round 3: {price} → accepted")
        else:
            st.warning("Rejected: price remains unchanged")
            st.session_state.final = st.session_state.p2
            st.session_state.history.append(f"Round 3: {price} → rejected")

        st.session_state.round = 99

# -------------------------
# FINAL SCREEN
# -------------------------
elif st.session_state.round == 99:
    st.header("Final Deal")

    st.metric("Final Price", f"${st.session_state.final}M")

    st.subheader("Price History")

    # 👉 THIS IS YOUR ITEM 13 IMPLEMENTED EXACTLY
    for h in st.session_state.history:
        st.write(h)

    st.subheader("Bonus Question")
    st.write("Identify the type of tax-free reorganization that fits the final deal.")

    answer = st.text_area("Your answer")

# -------------------------
# RESET
# -------------------------
if st.button("Restart Game"):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.rerun()
