🚔 Traffic Violation Prediction & Analysis Dashboard
    This project analyzes police stop and traffic violation data to uncover insights on arrest rates, violations, and stop patterns.
    It also includes a Streamlit dashboard for interactive data exploration and prediction.

📊 Dataset Overview
   File: vehicle_check.csv
   The dataset contains information about vehicle stops — including driver demographics like age, gender, race, country, violations, search details, arrest status, and stop timings.
   It is used to analyze trends and predict outcomes based on input attributes.

🧹 Data Preprocessing (in secure_check.ipynb)
   Data cleaning and preprocessing steps include:
   1. Filled missing values in search_type:
       "unknown" if search_conducted = 1
       "no search" if search_conducted = 0
   2. Merged stop_date and stop_time into a single column stop_datetime for easier time-based analysis.
   3. Removed unnecessary columns not relevant for analysis.
   4. Standardized and adjusted stop_duration_min for consistent units.
   5. Converted NumPy datatypes to Python datatypes (for MySQL compatibility).
   6. Created SQL connection and migrated the cleaned dataset to MySQL(tiDB) using CREATE TABLE and INSERT commands.

🧠 SQL Analysis
   Performed several analytical queries (as documented in the project notebook) to explore:
    1. Arrest rates by violation
    2. Search patterns by vehicle
    3. Stops by time of day
    4. Driver demographics by country
    5. Yearly breakdowns of stops and arrests and many more..

📈 Streamlit Dashboard (in secure_check.py)
   The dashboard enables users to interactively explore data, visualize trends, and predict outcomes.
   Key Components:
   📘 Project Overview
       1. Describes the project purpose and workflow
       2. Displays key KPIs:
           Total Stops
           Total Arrests
           Total Searches
       3. Includes charts like Top 5 Violations with High Arrest Rate and Most Common Stop Times
       
   📊 SQL Query Explorer
      1. Users can select from multiple SQL queries to visualize insights
      2. Runs run_query(query) and get_connection() functions
      3. Displays results using matplotlib bar charts (e.g., Top 10 Vehicles, Arrest Rate by Age)
      
   📝 Add New Log & Predict Outcome
      1. Form-based input for new police stop data
      2. Predicts likely violation, outcome, and arrest status based on historical patterns
      3. Automatically inserts the new record into the MySQL database

⚙️ Tech Stack
Languages & Libraries
  Python
  Pandas
  SQL / MySQL
  Streamlit
  Matplotlib
  Tabulate

📂 Project Structure
📁 Traffic_Violation_Prediction/
│
├── secure_check.py          # Streamlit dashboard app
├── secure_check.ipynb       # Data preprocessing and SQL analysis
├── vehicle_check.csv        # Dataset used for analysis
├── requirements.txt         # Dependencies
└── README.md                # Project documentation

🚀 How to Run
pip install -r requirements.txt
streamlit run secure_check.py
