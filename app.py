import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title = "Startup Analysis",
    layout = "wide",
    initial_sidebar_state= "auto"
)

dataFrame = pd.read_csv(filepath_or_buffer = "startup_cleaned.csv")

dataFrame["date"] = pd.to_datetime(dataFrame["date"], errors='coerce')
dataFrame['month'] = dataFrame['date'].dt.month

# dataFrame["investor"] = dataFrame["investor"].fillna("Undisclosed")
# dataFrame.info()

# print(dataFrame.describe())

def load_overall_analysis():
    st.title("Overall analysis")

    col1, col2, col3, col4 = st.columns(4)

    # total investes ammount
    with col1:
        total = round(dataFrame['ammount'].sum())

        st.metric(label = "Total", value = str(total) + "Cr")

    # max investedValue

    allInvesments = dataFrame.groupby("startup")['ammount'].sum().sort_values(ascending = False)

    maxInvesment = allInvesments.values[0]

    # topInvestor = allInvesments.index[0]

    avgInvenmentPerStartup = dataFrame.groupby("startup")['ammount'].sum().mean()

    totalNumberOfStartups = dataFrame['startup'].nunique()

    with col2:
        st.metric(label = "Max Invesment", value = maxInvesment)

    #top Investror

    with col3:
        # st.metric(label = "Top Investor", value = topInvestor)
        st.metric(label = "Avg", value = str(round(avgInvenmentPerStartup)) + "Cr")

    with col4:
        st.metric(label = "Number of Startups", value = totalNumberOfStartups)


    st.header("MoM Invesment")

    temp_df = dataFrame.groupby(['year', "month"])['ammount'].sum().reset_index()
    temp_df['x_axis'] = dataFrame['month'].astype("str") + "-" + dataFrame['year'].astype('str')

    fig, ax = plt.subplots()

    ax.bar(temp_df['x_axis'], temp_df['ammount'])

    st.pyplot(fig)

def load_investor_details(investor):
    st.title(investor)
    lastFiveDf = dataFrame[dataFrame["investor"].str.contains(investor)].head()

    lastFiveDf = lastFiveDf[[
        "date",
        'startup',
        'vertical',
        'city',
        'round',
        'ammount'
    ]]

    st.subheader(
        body = "last five invesments"
    )

    st.dataframe(lastFiveDf)


    col1, col2 = st.columns(2)

    with col1:

    # biggest investment
        st.subheader(
            body = "Biggest invesments"
        )

        bigSeries = dataFrame[dataFrame['investor'].str.contains(investor)].groupby("startup")['ammount'].sum().sort_values(
            ascending= False
        ).head()

        # st.dataframe(bigSeries)
        fig, ax = plt.subplots()

        ax.bar(bigSeries.index, bigSeries.values)

        st.pyplot(fig)

    with col2:
        st.subheader(
            body = "Sectors invested in"
        )
        verticalSeries = dataFrame[
            dataFrame["investor"].str.contains(investor)
        ].groupby("vertical")["ammount"].sum()

        fig1, ax1 = plt.subplots()

        ax1.pie(verticalSeries, labels = verticalSeries.index, autopct= "%0.01f%%")

        st.pyplot(fig1)

    # for city and round

    col3, col4 = st.columns(2)

    with col3:
        st.subheader(
            body = "City of invesments"
        )

        citySeries = dataFrame[dataFrame['investor'].str.contains(investor)].groupby("city")['ammount'].sum().sort_values(
            ascending= False
        ).head()

        # st.dataframe(bigSeries)
        fig2, ax2 = plt.subplots()

        ax2.pie(citySeries, labels = citySeries.index, autopct= "%0.01f%%")

        st.pyplot(fig2)

    with col4:
        st.subheader(
            body = "Round invested in"
        )
        roundSeries = dataFrame[
            dataFrame["investor"].str.contains(investor)
        ].groupby("round")["ammount"].sum()

        fig4, ax4 = plt.subplots()

        ax4.pie(roundSeries, labels = roundSeries.index, autopct= "%0.01f%%")

        st.pyplot(fig4)

    # year by Year invesment

    st.subheader("Year on year invesments")

    yearOnYearInvesmentSeries = dataFrame[dataFrame['investor'].str.contains(investor)].groupby("year")['ammount'].sum()

    fig5, ax5 = plt.subplots()

    ax5.plot(
        yearOnYearInvesmentSeries.index,
        yearOnYearInvesmentSeries.values
    )

    st.pyplot(fig5)



st.sidebar.title("Indian Startup Funding Analysis")

options = [
        "Overall Analysis",
        "Startup",
        "Investor"
    ]

option = st.sidebar.selectbox(
    label = "Select one",
    options = options
)


if option == options[0]:
    # st.title("Overall analysis")
    btn0 = st.sidebar.button(label = "show overall analysis")

    if btn0:
        load_overall_analysis()
elif option == options[1]:
    st.sidebar.selectbox(
        label= "Select startup",
        options = sorted(dataFrame["startup"].unique().tolist())
    )
    btn1 = st.sidebar.button(label = "find Startup details")
else:
    selectedInvestor = st.sidebar.selectbox(
        label = "select investor",
        options = sorted(set(dataFrame["investor"].str.split(",").sum()))
    )
    btn2 = st.sidebar.button(label = "find Investor details")

    if btn2:
        load_investor_details(selectedInvestor)

