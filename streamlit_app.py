import streamlit as st

st.title("Tax Negotiation Game")

if "round" not in st.session_state:
    st.session_state.round = 1

st.write(f"Current Round: {st.session_state.round}")

price = st.number_input("Enter offer price ($M)", 0, 400, 275)

if st.button("Submit Offer"):
    if st.session_state.round == 1:
        if 270 <= price <= 275:
            st.success("Round 1 success")
            st.session_state.round = 2
        else:
            st.error("Round 1 failed → default $300M")

    elif st.session_state.round == 2:
        st.success("Round 2 submitted")
        st.session_state.round = 3

    elif st.session_state.round == 3:
        st.success("Game complete")
