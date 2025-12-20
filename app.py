import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="Data Assistant AI Web App",
    page_icon="🤖",
    layout="wide"
)

# -------------------------------
# Initialize Users (Session-based)
# -------------------------------
if "USERS" not in st.session_state:
    st.session_state.USERS = {
        "admin@gmail.com": "admin123",
        "vidhisa@gmail.com": "data123"
    }

# -------------------------------
# Session State
# -------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_user" not in st.session_state:
    st.session_state.current_user = None

# -------------------------------
# LOGIN UI
# -------------------------------
def login():
    st.markdown(
        """
        <div style='max-width:400px;margin:auto;
        padding:30px;border-radius:12px;
        box-shadow:0px 0px 15px #ddd'>
        <h2 style='text-align:center'>🔐 Data Assistant Login</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    option = st.radio(
        "",
        ["Sign In", "Forgot Password", "Don't have an account?"]
    )

    if option == "Sign In":
        email = st.text_input("📧 Email")
        password = st.text_input("🔑 Password", type="password")

        if st.button("🚀 Sign In"):
            if email in st.session_state.USERS and st.session_state.USERS[email] == password:
                st.session_state.logged_in = True
                st.session_state.current_user = email
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid email or password")

    elif option == "Forgot Password":
        st.info(
            "🔒 Password reset is disabled for security.\n\n"
            "Please contact the **Admin** to reset your password.\n\n"
            "📧 admin@gmail.com"
        )

    else:
        st.warning(
            "🚫 Public registration is disabled.\n\n"
            "To get access, please contact the **Admin**.\n\n"
            "📧 admin@gmail.com"
        )

# -------------------------------
# LOGOUT
# -------------------------------
def logout():
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.rerun()

# -------------------------------
# LOGIN CHECK
# -------------------------------
if not st.session_state.logged_in:
    login()

# ===============================
# MAIN APP
# ===============================
else:
    st.sidebar.title("📌 Navigation")
    st.sidebar.write(f"👤 {st.session_state.current_user}")

    menu_items = [
        "Upload & Overview",
        "Dashboard",
        "Data Preview",
        "Filter & Download",
        "Advanced Charts",
        "Ask Your Data (AI)"
    ]

    # Admin Panel only for admin
    if st.session_state.current_user == "admin@gmail.com":
        menu_items.append("Admin Panel")

    menu = st.sidebar.radio("Go to", menu_items)

    if st.sidebar.button("🚪 Logout"):
        logout()

    st.title("🤖 Data Assistant AI Web App")

    uploaded_file = st.file_uploader("Upload CSV file", type="csv")

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        num_cols = df.select_dtypes(include="number").columns
        cat_cols = df.select_dtypes(exclude="number").columns

        if menu == "Upload & Overview":
            c1, c2, c3 = st.columns(3)
            c1.metric("Rows", df.shape[0])
            c2.metric("Columns", df.shape[1])
            c3.metric("Missing Values", df.isnull().sum().sum())

        elif menu == "Dashboard":
            if len(num_cols) > 0:
                st.metric("Average Value", round(df[num_cols[0]].mean(), 2))

        elif menu == "Data Preview":
            st.dataframe(df, use_container_width=True)

        elif menu == "Filter & Download":
            col = st.selectbox("Select column", df.columns)
            val = st.selectbox("Select value", df[col].astype(str).unique())
            filtered_df = df[df[col].astype(str) == val]

            st.dataframe(filtered_df, use_container_width=True)

            st.download_button(
                "⬇️ Download Full Dataset",
                df.to_csv(index=False).encode(),
                "full_dataset.csv"
            )

            st.download_button(
                "⬇️ Download Filtered Dataset",
                filtered_df.to_csv(index=False).encode(),
                "filtered_dataset.csv"
            )

        elif menu == "Advanced Charts":
            chart = st.selectbox("Chart Type", ["Pie", "Histogram", "Box"])

            if chart == "Pie":
                col = st.selectbox("Category Column", cat_cols)
                fig, ax = plt.subplots()
                df[col].value_counts().plot.pie(autopct="%1.1f%%", ax=ax)
                st.pyplot(fig)

            elif chart == "Histogram":
                col = st.selectbox("Numeric Column", num_cols)
                fig, ax = plt.subplots()
                ax.hist(df[col], bins=20)
                st.pyplot(fig)

            elif chart == "Box":
                col = st.selectbox("Numeric Column", num_cols)
                fig, ax = plt.subplots()
                ax.boxplot(df[col])
                st.pyplot(fig)

        elif menu == "Ask Your Data (AI)":
            q = st.text_input("Ask a question")

            if q:
                q = q.lower()
                if "rows" in q:
                    st.success(df.shape[0])
                elif "columns" in q:
                    st.success(df.shape[1])
                elif "average" in q:
                    for col in num_cols:
                        if col.lower() in q:
                            st.success(df[col].mean())
                else:
                    st.warning("Question not understood")

        # -------------------------------
        # ADMIN PANEL
        # -------------------------------
        elif menu == "Admin Panel":
            st.subheader("🛠 Admin Panel")

            st.markdown("### ➕ Add User")
            new_email = st.text_input("New User Email")
            new_pass = st.text_input("New Password", type="password")

            if st.button("Add User"):
                if new_email and new_pass:
                    st.session_state.USERS[new_email] = new_pass
                    st.success("User added successfully")

            st.markdown("### ❌ Remove User")
            user_to_remove = st.selectbox(
                "Select user",
                [u for u in st.session_state.USERS if u != "admin@gmail.com"]
            )

            if st.button("Remove User"):
                del st.session_state.USERS[user_to_remove]
                st.success("User removed")

    else:
        st.info("⬆️ Upload a CSV file to begin")
