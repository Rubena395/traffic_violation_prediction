import pandas as pd
import mysql.connector
from tabulate import tabulate
import streamlit as st
import matplotlib.pyplot as plt

def get_connection():
    return mysql.connector.connect(
      host = "gateway01.eu-central-1.prod.aws.tidbcloud.com",
      port = 4000,
      user = "4HRQRPypJvdSYNG.root",
      password = "IOTAQOIa0EjHZU5V",
      database="guvi")

def run_query(query):
    try:
       connection=get_connection()
       df=pd.read_sql(query,connection)
    finally:
       connection.close()
    return df

st.set_page_config(page_title="Police Data Dashboard", layout="wide")
st.title("Police Stop Analysis Dashboard")
st.markdown("### A data-driven look into police stop patterns, violations, and outcomes")


st.sidebar.header("Navigation Menu")
menu=st.sidebar.radio("Choose what to explore", 
        ["Project Introduction", "SQL Queries with Visualization", "Add New Police Log and Predict Outcome"])


if menu=="Project Introduction":
    st.header("Project Overview")
    st.write("""
    This dashboard provides an analytical view of **police stop data** —
    exploring trends in arrests, searches, and violations across different
    age groups, countries, and time periods.
    - Run SQL analyses directly from Streamlit
    - Visualize KPIs and trends
    - Allow new log entries and predictions""")

    st.subheader("KPIs & Trends Overview")

    #show some kpis like total stop, arrest, search count
    tot_stop_query="SELECT count(*) AS total_stops FROM police_log"
    tot_arrest_query="SELECT count(*) AS total_arrests FROM police_log WHERE is_arrested=1"
    tot_search_query="SELECT count(*) AS total_searches FROM police_log WHERE search_conducted=1"

    total_stops = run_query(tot_stop_query).iloc[0,0]
    total_arrests = run_query(tot_arrest_query).iloc[0,0]
    total_searches = run_query(tot_search_query).iloc[0,0]

    col1,col2,col3=st.columns(3)

    col1.metric("Total Stops", total_stops)
    col2.metric("Total Arrests", total_arrests)
    col3.metric("Total Searches", total_searches)

    #show some trends
    #top 5 violation with arrest 
    violation_query="""WITH rate_table as
                    (SELECT violation,
                           (COUNT(CASE WHEN is_arrested=1 THEN 1 END) / COUNT(*)) * 100.0 AS arrest_rate
                    FROM police_log
                    GROUP BY violation)
                    SELECT violation, arrest_rate, RANK() OVER(ORDER BY arrest_rate DESC) AS rate_rank
                    FROM rate_table LIMIT 5
                    """
    violation_df=run_query(violation_query)

    # time of day with most traffic stops
    time_day_query="""SELECT CASE WHEN HOUR(stop_datetime) BETWEEN 5 AND 11 THEN 'Morning'
                                WHEN HOUR(stop_datetime) BETWEEN 12 AND 16 THEN 'Afternoon'
                                WHEN HOUR(stop_datetime) BETWEEN 17 AND 20 THEN 'Evening'
                                ELSE 'Night'
                            END AS time_of_day, COUNT(*) AS stop_count
                    FROM police_log GROUP BY time_of_day ORDER BY stop_count DESC"""
    timeday_df=run_query(time_day_query)

    col1,col2=st.columns(2)
    with col1:
       st.subheader("Top 5 violation with high arrest rate")
       #st.bar_chart(violation_df.set_index("violation")["arrest_rate"])
       fig1, ax = plt.subplots(figsize=(10, 6))
       ax.bar(violation_df["violation"], violation_df["arrest_rate"], color="skyblue")
       ax.set_xlabel("Violation")
       ax.set_ylabel("Arrest Rate")
       ax.set_title("Top 5 Violation with Arrest Rate")
       plt.xticks(rotation=45, ha="right")
       plt.tight_layout()
       st.pyplot(fig1)
       plt.close(fig1)
    
    with col2:
       st.subheader("Time of day with most traffic stops")
       #st.bar_chart(timeday_df.set_index("time_of_day"))
       fig2, ax = plt.subplots(figsize=(10, 6))
       ax.bar(timeday_df["time_of_day"], timeday_df["stop_count"], color="skyblue")
       ax.set_xlabel("Time of Day")
       ax.set_ylabel("Stop Count")
       ax.set_title("Time of Day with most Traffic stops")
       plt.xticks(rotation=45, ha="right")
       plt.tight_layout()
       st.pyplot(fig2)
       plt.close(fig2)



elif menu=="SQL Queries with Visualization":
    st.header("SQL Query Explorer")
    selected_query=st.selectbox("choose a query to run",
        ["Top 10 Vehicles in Drug Stops",
        "Most Frequently Searched Vehicles",
        "Driver Age with highest Arrest Rate",
        "Average Stop Duration by Violation",
        "Stops by Time of Day",
        "Driver Demographics by Country",
        "Yearly Breakdown of Stops/Arrests by Country"])
    if selected_query=="Top 10 Vehicles in Drug Stops":
        query="""SELECT vehicle_number, COUNT(vehicle_number) AS vehicle_count  
        FROM police_log where drugs_related_stop=1 
        GROUP BY vehicle_number ORDER BY vehicle_count DESC LIMIT 10"""
        df=run_query(query)
        st.subheader("Top 10 Vehicles Involved in Drug-Related Stops")
        st.dataframe(df)  
        #st.bar_chart(df.set_index("vehicle_number")) 
        fig1, ax = plt.subplots(figsize=(10, 6))
        ax.bar(df["vehicle_number"], df["vehicle_count"], color="skyblue")
        ax.set_xlabel("Vehicle Number")
        ax.set_ylabel("Count")
        ax.set_title("Top 10 Vehicles in Drug Stops")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        st.pyplot(fig1)
        plt.close(fig1)
    elif selected_query=="Most Frequently Searched Vehicles":
        query="""SELECT vehicle_number, COUNT(vehicle_number) AS vehicle_count 
        FROM police_log WHERE search_conducted=1 
        GROUP BY vehicle_number ORDER BY vehicle_count DESC"""
        df=run_query(query)
        st.subheader("Most Frequently Searched Vehicles")
        st.dataframe(df)  
        #st.bar_chart(df.set_index("vehicle_number")) 
        fig2, ax = plt.subplots(figsize=(10, 6))
        ax.bar(df["vehicle_number"], df["vehicle_count"], color="skyblue")
        ax.set_xlabel("Vehicle Number")
        ax.set_ylabel("Count")
        ax.set_title("Most frequently searched vehicles")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        st.pyplot(fig2)
        plt.close(fig2)
    elif selected_query=="Driver Age with highest Arrest Rate":
        query="""SELECT driver_age, (COUNT(CASE WHEN is_arrested=1 THEN 1 END) / COUNT(driver_age))* 100.0 AS arrest_rate 
        FROM police_log GROUP BY driver_age ORDER BY arrest_rate DESC LIMIT 1"""
        df=run_query(query)
        st.subheader("Driver Age with highest Arrest Rate")
        st.dataframe(df)  
        age=int(df.iloc[0]['driver_age'])
        rate=round(df.iloc[0]['arrest_rate'],2)
        st.metric(label=f"Driver Age with highest arrest rate", 
                  value=f"{age} years",
                  delta=f"{rate}% Arrest Rate")
    elif selected_query=="Average Stop Duration by Violation":
        query="""SELECT violation, AVG(stop_duration_min) AS avg_stop_duration
          FROM police_log GROUP BY violation ORDER BY avg_stop_duration DESC"""
        df=run_query(query)
        st.subheader("Average Stop Duration by Violation")
        st.dataframe(df)  
        #st.bar_chart(df.set_index("violation"))
        fig4, ax = plt.subplots(figsize=(10, 6))
        ax.bar(df["violation"], df["avg_stop_duration"], color="skyblue")
        ax.set_xlabel("Violation")
        ax.set_ylabel("Avg_stop_duration")
        ax.set_title("Avearge Stop Duration by Violation ")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        st.pyplot(fig4)
        plt.close(fig4)
    elif selected_query=="Stops by Time of Day":
        query="""SELECT CASE WHEN HOUR(stop_datetime) BETWEEN 5 AND 11 THEN 'Morning'
                                WHEN HOUR(stop_datetime) BETWEEN 12 AND 16 THEN 'Afternoon'
                                WHEN HOUR(stop_datetime) BETWEEN 17 AND 20 THEN 'Evening'
                                ELSE 'Night'
                            END AS time_of_day, COUNT(*) AS stop_count
                    FROM police_log GROUP BY time_of_day ORDER BY stop_count DESC"""
        df=run_query(query)
        st.subheader("Stops by Time of Day")
        st.dataframe(df)  
        #st.bar_chart(df.set_index("time_of_day"))
        fig5, ax = plt.subplots(figsize=(10, 6))
        ax.bar(df["time_of_day"], df["stop_count"], color="skyblue")
        ax.set_xlabel("Time of Day")
        ax.set_ylabel("Stop count")
        ax.set_title("Stops by Time of Day")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        st.pyplot(fig5)
        plt.close(fig5)
    elif selected_query=="Driver Demographics by Country":
        query="""SELECT country_name, driver_age, driver_gender, driver_race, COUNT(*) AS count, (COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(PARTITION BY country_name)) AS pct_of_country
        FROM police_log GROUP BY country_name, driver_race, driver_age, driver_gender ORDER BY country_name, driver_race, driver_age DESC"""
        df=run_query(query)
        st.subheader("Driver Demographics by Country")
        st.dataframe(df)  
        race_summary = df.groupby(["country_name", "driver_race"])["count"].sum().unstack(fill_value=0)

        fig6, ax = plt.subplots(figsize=(10, 6))

        race_summary.plot(kind="bar", stacked=True, ax=ax)

        ax.set_title("Driver Demographics by Country (Stacked by Race)", fontsize=14)
        ax.set_xlabel("Country", fontsize=12)
        ax.set_ylabel("Driver Count", fontsize=12)
        ax.legend(title="Driver Race", bbox_to_anchor=(1.05, 1), loc="upper left")
        plt.tight_layout()

        st.pyplot(fig6)
        plt.close(fig6)
    elif selected_query=="Yearly Breakdown of Stops/Arrests by Country":
        query="""SELECT country_name,year,tot_stops,arrest_count,
                (arrest_count / tot_stops) * 100 AS arrest_rate,
                SUM(arrest_count) OVER(PARTITION BY country_name ORDER BY year) AS arrest_tot
                FROM (
                SELECT country_name,YEAR(stop_datetime) AS year,
                COUNT(CASE WHEN is_arrested = 1 THEN 1 END) AS arrest_count,
                COUNT(*) AS tot_stops
                FROM police_log
                GROUP BY country_name, YEAR(stop_datetime)
                ) AS year_table
                ORDER BY country_name, year"""
        df=run_query(query)
        st.subheader("Yearly Breakdown of Stops/Arrests by Country")
        st.dataframe(df)  
        st.write("Arrest rate by country in the year 2020")
        #st.bar_chart(df.set_index("country_name")["arrest_rate"])
        fig7, ax = plt.subplots(figsize=(10, 6))
        ax.bar(df["country_name"], df["arrest_rate"], color="skyblue")
        ax.set_xlabel("Country")
        ax.set_ylabel("Arrest Rate")
        ax.set_title("Arrest Rate by Country in 2020")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        st.pyplot(fig7)
        plt.close(fig7)
    
elif menu=="Add New Police Log and Predict Outcome":
    st.subheader("Add New Police Log and Predict Outcome")

    st.write("### Enter new stop details")
    with st.form("add_log_form"):
        driver_age=st.number_input("Driver age", min_value=16, max_value=90)
        driver_gender=st.selectbox("Driver gender",['Male','Female'])
        driver_race=st.selectbox("Driver race",['Asian','White','Black','Hispanic','Other'])
        country_name=st.text_input("Country Name")
        vehicle_number=st.text_input("vehicle number")
        drugs_related_stop=st.selectbox("Drugs related stop",[0,1])
        search_conducted=st.selectbox("Search conducted",[0,1])
        stop_duration_min=st.number_input("Stop duration (mins)", min_value=1, max_value=180)
        stop_date = st.date_input("Stop date")
        stop_time = st.time_input("Stop time")
        submitted=st.form_submit_button("Predict & Add log details")

    if submitted:
        if not driver_race or not search_conducted or not driver_age or not driver_gender or not country_name or not vehicle_number:
            st.warning("Please fill all required fields before submitting.")
            st.stop()  # stops further execution of the block

        from datetime import datetime     
        stop_datetime = datetime.combine(stop_date, stop_time)
        connection=get_connection()
        mycursor=connection.cursor(buffered=True)
        check_query=f"""SELECT violation, stop_outcome, is_arrested, search_type FROM police_log 
                    WHERE driver_age={driver_age} AND
                          driver_gender='{driver_gender}' AND
                          driver_race='{driver_race}' AND
                          search_conducted={search_conducted} 
                    LIMIT 1"""
        df=run_query(check_query)
        if not df.empty:
            violation=df.iloc[0]['violation']
            stop_outcome=df.iloc[0]['stop_outcome']
            is_arrested=df.iloc[0]['is_arrested']
            search_type=df.iloc[0]['search_type']
        else:
            df_all=run_query("SELECT * FROM police_log")
            subset = df_all[
                (df_all['driver_gender'] == driver_gender) &
                (df_all['driver_race'] == driver_race) &
                (df_all['drugs_related_stop'] == drugs_related_stop)]
            if subset.empty:
                subset = df_all  
            violation = subset['violation'].mode()[0]
            stop_outcome = subset['stop_outcome'].mode()[0]
            is_arrested = subset['is_arrested'].mode()[0]
            search_type = subset['search_type'].mode()[0]
        arrest_val = "get arrested" if is_arrested == 1 else "not get arrested"

        st.markdown(f"""
        ### Prediction Summary
        - **Violation:** {violation}
        - **Stop Outcome:** {stop_outcome}
        - **Search Type:** {search_type}
        - **Predicted Arrest Status:** Person might **{arrest_val}**
        """)

        insert_query = """INSERT INTO police_log 
            (country_name, driver_gender, driver_age_raw, driver_age, driver_race, violation_raw, violation,
             search_conducted, search_type, stop_outcome, is_arrested, drugs_related_stop, 
             vehicle_number,stop_datetime, stop_duration_min)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        
        driver_age = int(driver_age)
        search_conducted = int(search_conducted)
        is_arrested = int(is_arrested)
        drugs_related_stop = int(drugs_related_stop)
        stop_duration_min = int(stop_duration_min)

        violation = str(violation)
        stop_outcome = str(stop_outcome)
        search_type = str(search_type)

        
        values = (country_name, driver_gender, driver_age, driver_age, driver_race, violation, violation,
             search_conducted, search_type, stop_outcome, is_arrested, drugs_related_stop, 
             vehicle_number,stop_datetime, stop_duration_min)
            
        mycursor.execute(insert_query, values)
        connection.commit()

        st.success("✅ New police log added successfully!")
        connection.close()                  


        


