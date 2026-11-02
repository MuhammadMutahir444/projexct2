
import streamlit as st
from datetime import date

# ---------------------------------
# PAGE CONFIGURATION
# ---------------------------------

st.set_page_config(
    page_title="Personal Expense Tracker",
    page_icon="💰",
    layout="wide"
)

# ---------------------------------
# SESSION STATE INITIALIZATION
# ---------------------------------

if "expenses" not in st.session_state:
    st.session_state.expenses = []

if "expense_id" not in st.session_state:
    st.session_state.expense_id = 0


# ---------------------------------
# FUNCTIONS
# ---------------------------------

def add_expense(name, amount, category, expense_date):
    """Add a new expense to session state."""

    st.session_state.expense_id += 1

    expense = {
        "ID": st.session_state.expense_id,
        "Expense Name": name,
        "Amount": amount,
        "Category": category,
        "Date": expense_date
    }

    st.session_state.expenses.append(expense)


def delete_expense(expense_id):
    """Delete an expense using its unique ID."""

    st.session_state.expenses = [
        expense for expense in st.session_state.expenses
        if expense["ID"] != expense_id
    ]


def calculate_total():
    """Calculate total expenses."""

    return sum(
        expense["Amount"]
        for expense in st.session_state.expenses
    )


def get_highest_expense():
    """Find the highest expense."""

    if not st.session_state.expenses:
        return None

    return max(
        st.session_state.expenses,
        key=lambda expense: expense["Amount"]
    )


def get_category_totals():
    """Calculate category-wise expenses."""

    category_totals = {}

    for expense in st.session_state.expenses:
        category = expense["Category"]

        if category not in category_totals:
            category_totals[category] = 0

        category_totals[category] += expense["Amount"]

    return category_totals


def filter_expenses(expenses, search, category, amount_range):
    """Apply search, category and amount filters."""

    filtered = []

    for expense in expenses:

        # Search filter
        if search.lower() not in expense["Expense Name"].lower():
            continue

        # Category filter
        if category != "All Categories":
            if expense["Category"] != category:
                continue

        # Amount filter
        if not (
            amount_range[0]
            <= expense["Amount"]
            <= amount_range[1]
        ):
            continue

        filtered.append(expense)

    return filtered


# ---------------------------------
# APPLICATION TITLE
# ---------------------------------

st.title("💰 Personal Expense Tracker")

st.write(
    "Manage your daily expenses, track spending, "
    "and monitor your financial activities."
)

st.divider()


# ---------------------------------
# TASK 1: ADD EXPENSE
# ---------------------------------

st.header("➕ Add New Expense")

with st.form("expense_form"):

    expense_name = st.text_input(
        "Expense Name",
        placeholder="Enter expense name"
    )

    amount = st.number_input(
        "Amount",
        min_value=0.0,
        value=0.0,
        step=100.0
    )

    category = st.selectbox(
        "Category",
        ["Food", "Travel", "Shopping", "Bills", "Other"]
    )

    expense_date = st.date_input(
        "Expense Date",
        value=date.today()
    )

    submitted = st.form_submit_button(
        "Add Expense",
        use_container_width=True
    )

    if submitted:

        if not expense_name.strip():
            st.error("Please enter an expense name.")

        elif amount <= 0:
            st.error("Amount must be greater than zero.")

        else:
            add_expense(
                expense_name.strip(),
                amount,
                category,
                expense_date
            )

            st.success("Expense added successfully! 🎉")


st.divider()


# ---------------------------------
# TASK 2: DASHBOARD SUMMARY
# ---------------------------------

st.header("📊 Dashboard Summary")

total_expenses = calculate_total()

total_transactions = len(st.session_state.expenses)

highest_expense = get_highest_expense()

if highest_expense:
    highest_amount = highest_expense["Amount"]
else:
    highest_amount = 0.0


col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Total Expenses",
        value=f"Rs. {total_expenses:,.2f}"
    )

with col2:
    st.metric(
        label="Total Transactions",
        value=total_transactions
    )

with col3:
    st.metric(
        label="Highest Expense",
        value=f"Rs. {highest_amount:,.2f}"
    )


# Display highest expense details

if highest_expense:

    st.success(
        f"Highest Expense: "
        f"{highest_expense['Expense Name']} "
        f"(Rs. {highest_amount:,.2f})"
    )

else:
    st.warning("No expenses recorded yet.")


st.divider()


# ---------------------------------
# TASK 3 & 4: SIDEBAR FILTERS
# ---------------------------------

st.sidebar.title("🔍 Search & Filters")

st.sidebar.subheader("Search Expense")

search_query = st.sidebar.text_input(
    "Search by expense name",
    placeholder="e.g. Grocery"
)

st.sidebar.subheader("Category Filter")

selected_category = st.sidebar.selectbox(
    "Select Category",
    [
        "All Categories",
        "Food",
        "Travel",
        "Shopping",
        "Bills",
        "Other"
    ]
)


# Amount filter

if st.session_state.expenses:

    max_amount = max(
        expense["Amount"]
        for expense in st.session_state.expenses
    )

    st.sidebar.subheader("Amount Filter")

    amount_range = st.sidebar.slider(
        "Select Amount Range",
        min_value=0.0,
        max_value=float(max_amount),
        value=(0.0, float(max_amount))
    )

else:
    amount_range = (0.0, 0.0)

    st.sidebar.info(
        "Add an expense to enable amount filtering."
    )


# Apply all filters

filtered_expenses = filter_expenses(
    st.session_state.expenses,
    search_query,
    selected_category,
    amount_range
)


# ---------------------------------
# TASK 3: EXPENSE RECORDS
# ---------------------------------

st.header("📋 Expense Records")

st.write(
    f"Showing {len(filtered_expenses)} "
    f"of {total_transactions} transactions."
)

if filtered_expenses:

    # Prepare records for display

    display_records = []

    for expense in filtered_expenses:

        display_records.append({
            "Expense Name": expense["Expense Name"],
            "Amount": f"Rs. {expense['Amount']:,.2f}",
            "Category": expense["Category"],
            "Date": expense["Date"]
        })

    st.dataframe(
        display_records,
        use_container_width=True,
        hide_index=True
    )

else:

    st.warning(
        "No expense records found. "
        "Try changing your search or filters."
    )


st.divider()


# ---------------------------------
# TASK 5: DELETE EXPENSE
# ---------------------------------

st.header("🗑️ Delete Expense")

if filtered_expenses:

    st.write("Select an expense to delete:")

    for expense in filtered_expenses:

        col1, col2 = st.columns([4, 1])

        with col1:

            st.write(
                f"**{expense['Expense Name']}** | "
                f"Rs. {expense['Amount']:,.2f} | "
                f"{expense['Category']} | "
                f"{expense['Date']}"
            )

        with col2:

            if st.button(
                "Delete",
                key=f"delete_{expense['ID']}"
            ):

                delete_expense(expense["ID"])

                st.success(
                    "Expense deleted successfully!"
                )

                st.rerun()

else:

    st.info("No expenses available to delete.")


st.divider()


# ---------------------------------
# TASK 6: CATEGORY-WISE SUMMARY
# ---------------------------------

st.header("📂 Category-wise Expense Summary")

if st.session_state.expenses:

    category_totals = get_category_totals()

    for category_name, category_amount in category_totals.items():

        st.write(
            f"**{category_name}:** "
            f"Rs. {category_amount:,.2f}"
        )

else:

    st.warning(
        "Category-wise summary is unavailable "
        "because there are no expenses."
    )


# ---------------------------------
# FOOTER
# ---------------------------------

st.divider()

st.caption(
    "Personal Expense Tracker | "
    "Developed using Python and Streamlit"
)
