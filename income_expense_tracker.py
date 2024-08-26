import calendar #Core Caleder Module
from datetime import datetime #Core Caleder Module
#from streamlit_option_menu import option_menu #pip install streamlit-option-menu
import streamlit as st #pip install streamlit
import plotly.graph_objects as go # pip istall plotly


#---------------SETTINGS----------------------
income = [ "Salary", "Investments", "Other Income"]
expenses = ["Rent", "Groceries", "Utilities", "Car", "Other Expenses","Savings"]
currency = "ZAR"
page_title = "Income and Expense Tracker"
page_icon = ":money_with_wings:"  # https://www.webfx.com/tools/emoji-cheat-sheet
layout = "centered"
#---------------------------------------------


st.set_page_config(page_title=page_title, page_icon=page_icon,layout=layout)
st.title(page_title + " " + page_icon)

#---DROP DOWN VALUE FOR SELECTING THE PERIOD---
years= [datetime.today().year, datetime.today().year + 1]
months= list(calendar.month_name[1:])

# --- NAVIGATION MENU ---
#selected = option_menu(
    #menu_title=None,
    #options=["Data Entry", "Data Visualization"],
    #icons=["pencil-fill", "bar-chart-fill"],  # https://icons.getbootstrap.com/
    #orientation="horizontal",
#)

#---INPUT & SAVE PERIOD---
st.header(f"Data Entry in {currency}")
with st.form("entry_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    col1.selectbox("Select Month:", months, key="month")
    col2.selectbox("Select Year:", years, key="year")

    "---"
    with st.expander("Income"):
        for income in income:
            st.number_input(f"{income}:", min_value=0, format="%i", step=10, key=income)
    with st.expander("Expenses"):
        for expense in expenses:
            st.number_input(f"{expense}:", min_value=0, format="%i", step=10, key=expense)
    with st.expander("Comment"):
        comment = st.text_area("", placeholder="Enter a comment here...")

        "---"
        submitted =st.form_submit_button("Save Data")
        if submitted:
            period = str(st.session_state["year"]) + "_" + str(st.session_state["month"])
            incomes = {income: st.session_state[income] for income in income}
            expenses = {expense: st.session_state[expense] for expense in expenses}
            # TODO: Insert values into database
            st.write(f"incomes: {incomes}")
            st.write(f"expenses: {expenses}")
            st.success("Data saved!")
        
# --- PLOT PERIODS ---
st.header("Data Visualization")
with st.form("saved_periods"):
    #TODO: Get periods from database
    period = st.selectbox("Select Period:", [2024])
    submitted = st.form_submit_button("Plot Period")
    if submitted:
        #TODO: Ged data from database
        comment = "Some Comment"
        incomes = {'Salary': 15000, 'Other Income': 1500, 'Investments': 450}
        expenses = { 'Rent': 4500, 'Utilities': 600, 'Groceries': 2500, 'Car': 4000,
                     'Other Expenses': 250, 'Saving': 500}
        
         # Create metrics
        total_income = sum(incomes.values())
        total_expense = sum(expenses.values())
        remaining_budget = total_income - total_expense
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Income", f"{total_income} {currency}")
        col2.metric("Total Expense", f"{total_expense} {currency}")
        col3.metric("Remaining Budget", f"{remaining_budget} {currency}")
        st.text(f"Comment: {comment}")

 # Create sankey chart
        label = list(incomes.keys()) + ["Total Income"] + list(expenses.keys())
        source = list(range(len(incomes))) + [len(incomes)] * len(expenses)
        target = [len(incomes)] * len(incomes) + [label.index(expense) for expense in expenses.keys()]
        value = list(incomes.values()) + list(expenses.values())

        # Data to dict, dict to sankey
        link = dict(source=source, target=target, value=value)
        node = dict(label=label, pad=20, thickness=30, color="#E694FF")
        data = go.Sankey(link=link, node=node)

        # Plot it!
        fig = go.Figure(data)
        fig.update_layout(margin=dict(l=0, r=0, t=5, b=5))
        st.plotly_chart(fig, use_container_width=True)

