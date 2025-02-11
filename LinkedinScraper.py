from staffspy import LinkedInAccount, SolverType, DriverType, BrowserType
import pandas as pd
import streamlit as st


def read_user_data(file_name: list):
    users_df = pd.read_csv(file_name)
    users_df["profile_key"] = users_df["profile_url"].str.split('/').str[-2]
    return users_df

def sign_in():
    account = LinkedInAccount(
        session_file="session.pkl", # save login cookies to only log in once (lasts a week or so)
        log_level=1, # 0 for no logs
    )

    return account

def fetch_user_data(account, user_ids: list):
    users = account.scrape_users(
        user_ids=user_ids
    )
    return users

# upload file
uploaded_file = st.file_uploader(
    "Choose a CSV file"
)

if uploaded_file:
    # grab users we want to search
    users_df = read_user_data(uploaded_file)

    # sign into an account and fetch data for those users
    account = sign_in()
    users_info_df = fetch_user_data(account, users_df["profile_key"].values)

    # save the user data to a new CSV
    users_info_df.to_csv(f"{uploaded_file.name}_with_details.csv", index=False)

    st.dataframe(users_info_df)