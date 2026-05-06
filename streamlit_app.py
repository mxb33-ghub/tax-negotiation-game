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
    st.session_state.role = None
st.write("Baseline: $300M taxable purchase")

# -------------------------
# ROLE SELECTION
# -------------------------
if st.session_state.role is None:
    st.header("Choose Your Role")

    st.write("You will play directly against the computer.")
    st.write("Choose whether you want to represent the Buyer or the Seller.")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Play as Seller"):
            st.session_state.role = "seller"
            st.rerun()

    with col2:
        if st.button("Play as Buyer"):
            st.session_state.role = "buyer"
            st.rerun()

    st.stop()

# -------------------------
# ROUND 1
# -------------------------
if st.session_state.round == 1:
    st.header("Round 1 — Moving Off the $300M Taxable Baseline")

    st.write("In this round, the price should move off the $300M taxable baseline. Refer to the seller's materials for pricing guidance.")
    st.write("If the parties agree, the agreed price becomes P₁ and the game moves to Round 2.")

    if st.session_state.role == "seller":
        st.subheader("You are the Seller")
        st.write("You act first. Make a seller offer to the computer buyer.")
        price = st.number_input("Enter your seller offer ($M)", 0, 400, 275)

        if st.button("Submit Round 1 Offer"):
            if 270 <= price <= 275:
                st.success("Computer Buyer accepts. Round 1 succeeds.")
                st.session_state.p1 = price
                st.session_state.history.append(f"Round 1: Seller offered ${price}M → accepted")
                st.session_state.round = 2
                st.rerun()
            else:
                st.error("Computer Buyer rejects. Try another seller offer.")
                st.session_state.history.append(f"Round 1: Seller offered ${price}M → rejected")

    elif st.session_state.role == "buyer":
        st.subheader("You are the Buyer")
        st.write("The computer seller opens with a demand of $278M.")
        st.info("Computer Seller offer: $278M")

        price = st.number_input("Enter your buyer counteroffer ($M)", 0, 400, 272)

        if st.button("Submit Round 1 Counteroffer"):
            if 270 <= price <= 275:
                st.success("Computer Seller accepts. Round 1 succeeds.")
                st.session_state.p1 = price
                st.session_state.history.append(f"Round 1: Buyer countered ${price}M → accepted")
                st.session_state.round = 2
                st.rerun()
            else:
                st.error("Computer Seller rejects. Try another buyer counteroffer.")
                st.session_state.history.append(f"Round 1: Buyer countered ${price}M → rejected") 
   
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
