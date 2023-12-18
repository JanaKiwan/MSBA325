import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import base64
import plotly.express as px
import plotly.graph_objects as go
import altair as alt

# Set Streamlit theme
st.set_page_config(
    page_title="Hospital Encounters",
	
    layout="wide",
 
)
# Set color palette for visualizations
sns.set_palette("pastel")

# Define the layout
st.title("Hospital Encounters Dashboard")

# Add CSS to set the background image for the title
st.markdown(
    """
    <style>
    h1 {
        background-repeat: no-repeat;
        background-color: lightblue;
        background-position: center;
        background-size: cover;
        color: black;
        padding: 1rem;
        text-align: center;
        font-size: 3rem;
    }

    .left-column {
        flex: 1;
        padding-right: 1rem;
        padding-top: 5rem;
    }
    .right-column {
        flex: 1;
        padding-left: 1rem;
    }
	.analytics-text {
			font-size: 1rem;
			text-align: left;
			margin-top: 1rem;
		}

    </style>
    """,
    unsafe_allow_html=True
)
# Load your data
data = pd.read_csv('Diabestes_Hospital_Encounters(1).csv')








  # Card section
with st.container():
	st.markdown(
			"""
			<style>
			.metric-value {
				font-size: 36px;
				color: blue;
			}
			.metric-label {
				font-size: 15px;
				color: black;
				margin-bottom: 0;
				#font-weight: bold;
			}
			</style>
			""",
			unsafe_allow_html=True
		)
		
		# Create five columns for metrics
	col1, col2, col3, col4, col5 = st.columns(5)
		
		# Metric 1: Total hospital Encounters
	with col1:
			st.markdown("<p class='metric-label'>Total Encounters</p>", unsafe_allow_html=True)
			st.markdown(f"<p class='metric-value'>{len(data)}</p>", unsafe_allow_html=True)
		
		# Metric 2: Readmitted = Yes
	with col2:
			readmitted_yes_count = len(data[data['readmitted'] == 'Yes'])
			total_cases = len(data)

			# Calculate the percentage of readmitted cases
			readmitted_percentage = (readmitted_yes_count / total_cases) * 100
			readmitted_percentage_formatted = "{:.2f}%".format(readmitted_percentage)

			st.markdown("<p class='metric-label'>Readmitted</p>", unsafe_allow_html=True)
			st.markdown(f"<p class='metric-value'>{readmitted_percentage_formatted}</p>", unsafe_allow_html=True)
		
		# Metric 3: Average time in hospital
	with col3:
			average_time_in_hospital = data['time_in_hospital'].mean()
			st.markdown("<p class='metric-label'>Avg days in hospital</p>", unsafe_allow_html=True)
			st.markdown(f"<p class='metric-value'>{average_time_in_hospital:.2f}</p>", unsafe_allow_html=True)
		
		# Metric 4: Average lab procedures
	with col4:
			average_lab_procedures = data['num_lab_procedures'].mean()
			st.markdown("<p class='metric-label'>Avg lab procedures/stay</p>", unsafe_allow_html=True)
			st.markdown(f"<p class='metric-value'>{average_lab_procedures:.2f}</p>", unsafe_allow_html=True)
		
		# Metric 5: Average medications
	with col5:
			average_medications = data['num_medications'].mean()
			st.markdown("<p class='metric-label'>Avg medications/stay</p>", unsafe_allow_html=True)
			st.markdown(f"<p class='metric-value'>{average_medications:.2f}</p>", unsafe_allow_html=True)

	# Add a line between sections
	st.markdown("---")

	# Demographics area

	# Create a container for the demographics section
	demographics_container = st.container()

	# Use the container to add content and apply formatting
with demographics_container:
		
		
		# Create columns for charts
	col1, col2, col3 = st.columns(3)

		# Chart 1: Gender Distribution
	with col1:
			gender_counts = data['gender'].value_counts()

			# Create pie chart
			fig, ax = plt.subplots(figsize=(8, 6))
			wedges, labels, autopct = ax.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', startangle=90, colors=['#2B65EC', '#5CB3FF'])
			# Set plot title and labels
			ax.set_title("Gender\n",fontfamily="Arial", fontsize=18,fontweight='bold')
			# Modify the size of labels
			# Modify the size of labels
			for label in labels:
				label.set_size(8)
			# Show the plot
			st.pyplot(fig)

		# Chart 2: Age Distribution
	with col2:
			# Create countplot
			# Sort the age values in descending order
			sorted_age = data['age'].value_counts().sort_values(ascending=False).index
			fig, ax = plt.subplots(figsize=(8, 6))
			sns.countplot(x="age", data=data,order=sorted_age, palette="Set1")

			# Set plot title and labels
			ax.set_title("Age\n\n\n",fontfamily="Arial",fontsize=24,fontweight='bold')
			ax.set_xlabel("")
			ax.set_ylabel("")
            # Remove the border lines
			ax.spines['top'].set_visible(False)
			ax.spines['right'].set_visible(False)
			ax.spines['bottom'].set_visible(False)
			ax.spines['left'].set_visible(False)
            # Adjust spacing between title and chart
			
			# Show the plot
			st.pyplot(fig)

		# Chart 3: Race Distribution
	with col3:
			# Get the value counts for the race column
			race_counts = data['race'].value_counts()

			# Create a bar chart
			fig, ax = plt.subplots(figsize=(8, 6))
			sns.barplot(x=race_counts.index, y=race_counts.values, color="#1E90FF",ax=ax)

			# Set plot title and labels
			ax.set_title('Race\n\n\n',fontfamily="Arial", fontsize=24,fontweight='bold')
			ax.set_xlabel('')
			ax.set_ylabel('')
            # Remove the border lines
			ax.spines['top'].set_visible(False)
			ax.spines['right'].set_visible(False)
			ax.spines['bottom'].set_visible(False)
			ax.spines['left'].set_visible(False)
			# Rotate the x-axis labels for better readability
			ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

			# Show the plot
			st.pyplot(fig)
			
	# Demographic Analysis Interactive Section
st.markdown("---")
st.subheader("Interactive Demographic Analysis")

# Dropdown for demographic selection
demographic_option = st.selectbox(
    "Select a Demographic Attribute to Analyze", 
    ["Age Group", "Gender", "Race"]
)

# Plot based on selection
if demographic_option == "Age Group":
    fig = px.histogram(data, x="age_group")
    st.plotly_chart(fig)
elif demographic_option == "Gender":
    fig = px.histogram(data, x="gender")
    st.plotly_chart(fig)
else:  # Race
    fig = px.histogram(data, x="race")
    st.plotly_chart(fig)

st.markdown("This section allows users to explore the distribution of patients based on selected demographic attributes.")

# Medication and Readmission Analysis Interactive Section
st.markdown("---")
st.subheader("Medication and Readmission Analysis")

# Dropdown for medication selection
medication_option = st.selectbox(
    "Select a Medication Type to Analyze Readmission Rates", 
    ["Insulin", "Metformin", "Glipizide"]
)

# Plot based on selection
medication_col = medication_option.lower()
fig = px.histogram(data, x=medication_col, color="readmitted")
st.plotly_chart(fig)

st.markdown("This interactive chart shows the relationship between different medication types and patient readmission rates.")
