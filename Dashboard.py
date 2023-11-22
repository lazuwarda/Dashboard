import pandas as pd
import seaborn as sns
import streamlit as st

sns.set(style='dark')


# Helper function yang dibutuhkan untuk menyiapkan berbagai dataframe

def create_count_user_df(df):
    count_user_df = df.resample(rule='D', on='dteday').agg({
        "cnt": "sum",
        "casual": "sum",
        "registered":"sum"
    })
    return count_user_df


def create_byseason_df(df):
    byseason_df = df.groupby(by="season").cnt.sum().reset_index()
    byseason_df.rename(columns={
        "cnt": "user_count"
    }, inplace=True)

    return byseason_df

def create_byweathersit_df(df):
    byweathersit_df = df.groupby(by="weathersit").cnt.sum().reset_index()
    byweathersit_df.rename(columns={
        "cnt": "user_count",
    }, inplace=True)

    return byweathersit_df
def create_byhr_df(df):
    byhr_df = df.groupby(by="hr").agg({
        "cnt": "sum",
        "casual": "sum",
        "registered":"sum"
    })
    return byhr_df

def create_weekday_df(df):
    weekday_df = df.groupby(['hr','weekday']).agg({
        "cnt": "sum",
        "casual": "sum",
        "registered": "sum"
    })
    return weekday_df

def create_byholiday_df(df):
    byholiday_df = df[['holiday','casual','registered','cnt']].copy()
    return byholiday_df

def create_byworkingday_df(df):
    byworkingday_df = df[['workingday','casual','registered','cnt']].copy()
    return byworkingday_df

# Load cleaned data
all_df = pd.read_csv("hour_data.csv")
datetime_columns = ["dteday"]
all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(inplace=True)

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

# Filter data
min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")

    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

    st.subheader('Nama : Naufatul Lazuwarda')
    st.subheader('Email : naufalazuwarda@gmail.com')
    st.subheader('ID Dicoding : Naufalazuwarda')

main_df = all_df[(all_df["dteday"] >= str(start_date)) &
                 (all_df["dteday"] <= str(end_date))]

# st.dataframe(main_df)

# # Menyiapkan berbagai dataframe
count_user_df = create_count_user_df(main_df)
byseason_df = create_byseason_df(main_df)
byweathersit_df = create_byweathersit_df(main_df)
byhr_df = create_byhr_df(main_df)
weekday_df=create_weekday_df(main_df)
byholiday_df=create_byholiday_df(main_df)
byworkingday_df=create_byworkingday_df(main_df)

# plot number of daily bike sharing
st.header('Bike Sharing Analysis Dashboard')
st.subheader('Daily Bike Sharing Users')

total_user = count_user_df.cnt.sum()
st.metric("Total User", value=total_user)

col1, col2 = st.columns(2)

with col1:
    registered_user = count_user_df.registered.sum()
    st.metric("Registered User", value=registered_user)

with col2:
    casual_user = count_user_df.casual.sum()
    st.metric("Casual User", value=casual_user)

# Banyaknya sepeda yang disewa berdasarkan musim dan cuaca
st.subheader("Seasons and Weathersit with the most bike rentals")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

sns.barplot(x="season", y="user_count", data=byseason_df.head(5), ax=ax[0])
ax[0].set_ylabel("User", fontsize=30)
ax[0].set_xlabel("Season", fontsize=30)
ax[0].set_title("Count of user by Season", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)

sns.barplot(x="weathersit", y="user_count", data=byweathersit_df.head(5), ax=ax[1])
ax[1].set_ylabel("User", fontsize=30)
ax[1].set_xlabel("Weathersit", fontsize=30)
ax[1].set_title("Count of user by Weathersit", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)

st.pyplot(fig)

# Banyaknya sepeda yang disewa berdasarkan jam
st.subheader("bike rentals per hour")
fig, ax = plt.subplots(nrows=3,ncols=1,figsize = (35,30))

sns.pointplot(data = byhr_df , x ='hr' , y ='casual', color='red', ax=ax[0])
ax[0].set_ylabel("User", fontsize=30)
ax[0].set_xlabel("Hour", fontsize=30)
ax[0].set_title("Bike Sharing per Hour (Casual User)", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)

sns.pointplot(data = byhr_df , x ='hr' , y ='registered', color='blue', ax=ax[1])
ax[1].set_ylabel("User", fontsize=30)
ax[1].set_xlabel("Hour", fontsize=30)
ax[1].set_title("Bike Sharing per Hour (Registered User)", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)

sns.pointplot(data = byhr_df , x ='hr' , y ='cnt', color='green', ax=ax[2])
ax[2].set_title("Bike Sharing per Hour (All User)", loc="center", fontsize=50)
ax[2].set_ylabel("User", fontsize=30)
ax[2].set_xlabel("Hour", fontsize=30)
ax[2].tick_params(axis='y', labelsize=35)
ax[2].tick_params(axis='x', labelsize=30)

st.pyplot(fig)

# Banyaknya sepeda yang disewa tiap harinya dalam seminggu
st.subheader("Count of bikes everyday of the week")

fig, ax = plt.subplots(nrows=2, ncols=1, figsize = (35,20))

sns.pointplot(data = weekday_df, x ='hr' , y ='casual', hue = 'weekday',palette=sns.color_palette([ "#E69F00", "#56B4E9", "#009E73","#F0E442", "#0072B2", "#D55E00", "#CC79A7"]),ax=ax[0])
ax[0].set_title("Count of bikes during weekdays and weekends by casual user", loc="center", fontsize=50)
ax[0].set_ylabel("User", fontsize=30)
ax[0].set_xlabel("Hour", fontsize=30)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)

sns.pointplot(data =weekday_df , x ='hr' , y ='registered', hue='weekday',palette=sns.color_palette([ "#E69F00", "#56B4E9", "#009E73","#F0E442", "#0072B2", "#D55E00", "#CC79A7"]),ax=ax[1])
ax[1].set_title("Count of bikes during weekdays and weekends by registered user", loc="center", fontsize=50)
ax[1].set_ylabel("User", fontsize=30)
ax[1].set_xlabel("Hour", fontsize=30)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)
st.pyplot(fig)


fig, ax = plt.subplots(nrows=1, ncols=2,figsize = (35,10))
sns.barplot(data =weekday_df , x ='weekday' , y ='casual', color='red', ax=ax[0])
ax[0].set_title("Count of bikes on a week (Casual User)", loc="center", fontsize=50)
ax[0].set_ylabel("Casual User", fontsize=30)
ax[0].set_xlabel("Weekday", fontsize=30)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)

sns.barplot(data =weekday_df, x ='weekday' , y ='registered', color='blue', ax=ax[1])
ax[1].set_title("Count of bikes on a week (Registered User)", loc="center", fontsize=50)
ax[1].set_ylabel("Registered User", fontsize=30)
ax[1].set_xlabel("Weekday", fontsize=30)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)
st.pyplot(fig)

# Banyaknya sepeda yang disewa ketika liburan dan hari kerja
st.subheader("User on Holiday and Workingday")

fig, ax = plt.subplots(nrows=2, ncols=3, figsize = (35,35))
sns.barplot(data = byholiday_df, x ='holiday', y ='casual',ax=ax[0][0])
ax[0][0].set_title("Holiday (Casual User)", loc="center", fontsize=40)
ax[0][0].set_ylabel("Casual", fontsize=30)
ax[0][0].set_xlabel("Holiday", fontsize=30)
ax[0][0].tick_params(axis='y', labelsize=35)
ax[0][0].tick_params(axis='x', labelsize=30)

sns.barplot(data = byholiday_df, x ='holiday', y ='registered',ax=ax[0][1])
ax[0][1].set_title("Holiday (Registered User)", loc="center", fontsize=40)
ax[0][1].set_ylabel("Registered", fontsize=30)
ax[0][1].set_xlabel("Holiday", fontsize=30)
ax[0][1].tick_params(axis='y', labelsize=35)
ax[0][1].tick_params(axis='x', labelsize=30)

sns.barplot(data = byholiday_df, x ='holiday', y ='cnt',ax=ax[0][2])
ax[0][2].set_title("Holiday (All User)", loc="center", fontsize=40)
ax[0][2].set_ylabel("All User", fontsize=30)
ax[0][2].set_xlabel("Holiday", fontsize=30)
ax[0][2].tick_params(axis='y', labelsize=35)
ax[0][2].tick_params(axis='x', labelsize=30)

sns.barplot(data = byworkingday_df , x ='workingday' , y ='casual',ax=ax[1][0])
ax[1][0].set_title("Workingday (Casual User)", loc="center", fontsize=40)
ax[1][0].set_ylabel("Casual", fontsize=30)
ax[1][0].set_xlabel("Workingday", fontsize=30)
ax[1][0].tick_params(axis='y', labelsize=35)
ax[1][0].tick_params(axis='x', labelsize=30)

sns.barplot(data = byworkingday_df , x ='workingday', y ='registered',ax=ax[1][1])
ax[1][1].set_title("Workingday (Registered User)", loc="center", fontsize=40)
ax[1][1].set_ylabel("Registered", fontsize=30)
ax[1][1].set_xlabel("Workingday", fontsize=30)
ax[1][1].tick_params(axis='y', labelsize=35)
ax[1][1].tick_params(axis='x', labelsize=30)

sns.barplot(data = byworkingday_df , x ='workingday', y ='cnt',ax=ax[1][2])
ax[1][2].set_title("Workingday (All User)", loc="center", fontsize=40)
ax[1][2].set_ylabel("cnt", fontsize=30)
ax[1][2].set_xlabel("Workingday", fontsize=30)
ax[1][2].tick_params(axis='y', labelsize=35)
ax[1][2].tick_params(axis='x', labelsize=30)

st.pyplot(fig)

st.caption('Copyright © Dicoding 2023')
