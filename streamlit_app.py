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
    st.session_state.next_round = None
st.write("Baseline: $300M taxable purchase")

# -------------------------
# ROLE SELECTION
# -------------------------
if st.session_state.role is None:
    st.header("Choose Your Role")

    st.write("You will play directly against the computer.")
    st.write("Choose whether you want to play as the Buyer or the Seller.")

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
# ROUND TRANSITION SCREEN
# -------------------------
if st.session_state.next_round is not None:

    st.success("Congratulations — the parties reached agreement.")

    st.write(f"The game will now proceed to Round {st.session_state.next_round}.")

    if st.button("Continue"):

        st.session_state.round = st.session_state.next_round
        st.session_state.next_round = None
        st.session_state.round_attempts = 0
        st.rerun()

    st.stop()


# -------------------------
# ROUND 1
# -------------------------
if st.session_state.round == 1:
    st.header("Round 1 — Improve Tax Efficiency for the Seller - Moving Off the $300M Taxable Baseline")

    st.write("In this round the seller would like to improve it's tax efficiency, recognizing this change  causes tax issues for the buyer. An appropriate price reduction may satisfy both parties. The seller proposes changing the terms to an all stock tax free sale.  Refer to the case materials for pricing guidance.")
    st.write("If the parties agree, the agreed price becomes P₁, the structure changes to a tax free stock purchase,  and the game moves to Round 2.")

    if st.session_state.role == "seller":
        st.subheader("You are the Seller")
        st.write("You act first. Make a revised all stock tax free purchase offer to the buyer. Adjust the starting offer of $300M to reflect the buyer's increased tax cost due to loss of basis step up. Remember they have their own views of the cost/benefit of the proposal.")
        st.write("You have determined how much the tax free deal is worth to you. You cannot offer to reduce the price less than $270M.")

        price = st.number_input(
            "Enter your seller offer ($M)",
            min_value=0,
            max_value=400,
            value=None,
            placeholder="Enter offer here..."
        )
        
        if st.button("Submit Round 1 Offer"):
            if price < 270:
                st.error("Invalid offer. As seller, you have determined you cannot offer to reduce the price below $270M.")
                st.session_state.history.append(f"Round 1: Seller offered ${price}M → invalid, below seller minimum")
            
            elif price <= 275:
                st.success("Computer Buyer accepts. Round 1 succeeds.")
                st.session_state.p1 = price
                st.session_state.history.append(f"Round 1: Seller offered ${price}M → accepted")
                st.session_state.next_round = 2
                st.rerun()
                
            else:
                st.error("Computer Buyer rejects. Your offer is still too high for the buyer.")
                st.session_state.history.append(f"Round 1: Seller offered ${price}M → rejected")

    elif st.session_state.role == "buyer":
        st.subheader("You are the Buyer")
        st.write("The computer seller wants to improve it's tax efficiency versus the taxable sale baseline. They offer to reduce purchase price to $278M in exchange for a tax free all stock purchase.")
        st.write("You have determined you cannot pay more than $275M if the deal is changed to tax free because of the loss of tax benefits to you.")
        st.write("You would prefer to pay the lowest price you think the seller would accept.")
        st.info("Computer Seller offer: $278M")

        price = st.number_input(
           "Enter your buyer counteroffer ($M)",
           min_value=0,
           max_value=400,
           value=None,
           placeholder="Enter counteroffer here..."
        ) 

        if st.button("Submit Round 1 Counteroffer"):
            
            if price > 275:
                st.error("Invalid counteroffer. As buyer, you cannot offer more than $275M.")
                st.session_state.history.append(f"Round 1: Buyer countered ${price}M → invalid, above buyer maximum")

            elif price >= 270:
                st.success("Computer Seller accepts. Round 1 succeeds.")
                st.session_state.p1 = price
                st.session_state.history.append(f"Round 1: Buyer countered ${price}M → accepted")
                st.session_state.next_round = 2
                st.rerun()

            else:
               st.error("Computer Seller rejects. The price is too low for the seller.")
               st.session_state.history.append(f"Round 1: Buyer countered ${price}M → rejected")    
   

# -------------------------
# ROUND 2
# -------------------------
elif st.session_state.round == 2:
    st.header("Round 2 — Seller requests cash boot in the new stock purchase, buyer requests additional price concession to provide.")

    p1 = st.session_state.p1

    st.write(f"Round 1 agreed price: ${p1}M")
    st.write("In this round, the seller has approached the buyer requesting some boot into the new all stock deal. The buyer is amenable, but recognizes they can extract a lowered purchase price for accomodating the seller")
    st.write("Both parties want to preserve the tax free nature of the revised deal.")
    st.write("If the parties cannot agree, the negotiation ends using the Round 1 price.")
    
   
    if st.session_state.role == "buyer":
        st.subheader("You are the Buyer")
        st.write("You act first. You request a higher price in exchange for including boot.")
        st.write(f"You have determined you cannot offer more than ${p1 + 15}M in Round 2.")

        price = st.number_input(
            "Enter your Round 2 buyer offer ($M)",
            min_value=0,
            max_value=400,          
            value=None,
            placeholder="Enter offer here..."
        )

        if st.button("Submit Round 2 Offer"):

            if price is None:
                st.error("Please enter an offer.")

            elif price > p1 + 15:
                st.error(f"Invalid offer. As buyer, you cannot offer more than ${p1 + 15}M.")
                st.session_state.history.append(f"Round 2: Buyer offered ${price}M → invalid, above buyer maximum")

            elif price >= p1 + 10:
                st.success("Computer Seller agrees to the price concession. Round 2 succeeds.")
                st.session_state.p2 = price
                st.session_state.history.append(f"Round 2: Buyer offered ${price}M → accepted")
                st.session_state.next_round = 3
                st.rerun()

            else:
                st.error("Computer Seller rejects. The offer is not high enough.")
                st.session_state.final = p1
                st.session_state.history.append(f"Round 2: Buyer offered ${price}M → rejected; final price remains ${p1}M")
                st.session_state.round = 99
                st.rerun()

    elif st.session_state.role == "seller":
        st.subheader("You are the Seller")

        computer_offer = p1 + 8

        st.write("The computer buyer opens with a Round 2 offer.")
        st.info(f"Computer Buyer offer: ${computer_offer}M")

        price = st.number_input(
            "Enter your seller Round 2 counteroffer ($M)",
            min_value=0,
            max_value=400,
            value=None,
            placeholder="Enter counteroffer here..."
        )

        if st.button("Submit Round 2 Counteroffer"):

            if price is None:
                st.error("Please enter a counteroffer.")

            elif price < p1 + 10:
                st.error(f"Invalid counteroffer. As seller, you should not accept less than ${p1 + 10}M.")

            elif price <= p1 + 15:
                st.success("Computer Buyer accepts. Round 2 succeeds.")
                st.session_state.p2 = price
                st.session_state.history.append(f"Round 2: Seller countered ${price}M → accepted")
                st.session_state.next_round = 3
                st.rerun()
  
            else:
                st.session_state.round_attempts += 1
                st.error("Computer Buyer rejects. Your counteroffer is too high.")
                st.session_state.history.append(f"Round 2: Seller countered ${price}M → rejected")

            if st.session_state.round_attempts >= 3:
                st.session_state.final = p1
                st.session_state.history.append(f"Round 2 ended after 3 rejected offers → final price remains ${p1}M")
                st.session_state.round = 99
                st.rerun()
            else:
                st.write(f"Counteroffers remaining: {3 - st.session_state.round_attempts}")

# -------------------------
# ROUND 3
# -------------------------

elif st.session_state.round == 3:
    st.header("Round 3 — Buyer requests a business structure accommodation")

    p2 = st.session_state.p2

    st.write(f"Current Price: ${p2}M")
    st.write("In this round, the buyer seeks a structure that reduces execution risk and preserves business continuity. Specifically, the buyer is concerned about a structure tht will ensure acquired licenses stay intact inside of the current legal entity.")
    st.write("If the parties do not agree, the game ends using the last successful price.")

    if st.session_state.role == "buyer":
        st.subheader("You are the Buyer")
        st.write("You act first. Offer a modest price increase to compensate the seller for added complexity.")

        price = st.number_input(
            "Enter your Round 3 buyer offer ($M)",
            min_value=0,
            max_value=400,
            value=None,
            placeholder="Enter final offer here..."
        )

        if st.button("Submit Round 3 Offer"):

            if price is None:
                st.error("Please enter an offer.")

            elif price > p2 + 7:
                st.error(f"Invalid offer. As buyer, you cannot offer more than ${p2 + 7}M.")

            elif price >= p2 + 4:
                st.success("Computer Seller accepts. Final deal reached.")
                st.session_state.final = price
                st.session_state.history.append(f"Round 3: Buyer offered ${price}M → accepted")
                st.session_state.round = 99
                st.rerun()

            else:
                st.error("Computer Seller rejects. The offer is not high enough.")
                st.session_state.final = p2
                st.session_state.history.append(f"Round 3: Buyer offered ${price}M → rejected; final price remains ${p2}M")
                st.session_state.round = 99
                st.rerun()

    elif st.session_state.role == "seller":
        st.subheader("You are the Seller")

        computer_offer = p2 + 3

        st.write("The computer buyer asks for a business structure accommodation.")
        st.write("You may counter with a price that compensates you for added complexity.")
        st.info(f"Computer Buyer offer: ${computer_offer}M")

        price = st.number_input(
            "Enter your Round 3 seller counteroffer ($M)",
            min_value=0,
            max_value=400,
            value=None,
            placeholder="Enter counteroffer here..."
        )

        if st.button("Submit Round 3 Counteroffer"):

            if price is None:
                st.error("Please enter a counteroffer.")

            elif price < p2 + 4:
                st.error(f"Invalid counteroffer. As seller, you should not accept less than ${p2 + 4}M.")

            elif price <= p2 + 7:
                st.success("Computer Buyer accepts. Final deal reached.")
                st.session_state.final = price
                st.session_state.history.append(f"Round 3: Seller countered ${price}M → accepted")
                st.session_state.round = 99
                st.rerun()

            else:
                st.error("Computer Buyer rejects. Your counteroffer is too high.")
                st.session_state.final = p2
                st.session_state.history.append(f"Round 3: Seller countered ${price}M → rejected; final price remains ${p2}M")
                st.session_state.round = 99
                st.rerun()

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
    st.write("Congratultions. Starting from a base case of a $300M all cash purchases, you have negotiated mutually agreed changes that have benefited both parties tax and business needs.")
    st.write("You will now answer a bonus question. Based on whichever round you successfully completed, Identify the type of tax-free reorganization that fits the final deal. Explain why you chose tht answer, remembering that several types of reorganizations could be correct depending on which round you completed. The bonus question answer will be discussed in class.")
   
    answer = st.text_area("Your answer")

# -------------------------
# RESET
# -------------------------
if st.button("Restart Game"):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.rerun()
