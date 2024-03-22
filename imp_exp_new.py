import streamlit as st
import pandas as pd
import altair as alt

# Load the dataset
@st.cache_data
def load_data():
    imp_data = pd.read_csv("pakistan_import_data.csv")
    exp_data = pd.read_csv("pakistan_export_data.csv")
    return imp_data, exp_data

imp_data, exp_data = load_data()

# Sidebar
st.sidebar.title("Select Data")
selected_category = st.sidebar.radio("Select Category:", ("Imports", "Exports"))
selected_type = st.sidebar.radio("Select Data Type:", ("Top", "Low"))
num_countries = st.sidebar.text_input("Enter the number of countries:", "5")

try:
    num_countries = int(num_countries)
    if num_countries > 243:
        num_countries = 243
except:
    num_countries = 5

# Option to include Trade Deficit
include_trade_deficit = st.sidebar.checkbox("Include Trade Deficit/Surplus", value=True)

try:
    num_countries = int(num_countries)
    if num_countries > 243:
        num_countries = 243
except:
    num_countries = 5

# Main content
st.title("Trade Analysis: Pakistan (2015-2019)")


try:

    if selected_category == "Imports":
        if selected_type == "Top":
            st.write(f"Top {num_countries} Countries with the Most Imports:")
            df_top = imp_data.groupby(['Country']).agg(Value=('Value', 'sum')).nlargest(num_countries, 'Value')
            color = 'blue'
        else:
            st.write(f"Top {num_countries} Countries with the Least Imports:")
            df_top = imp_data.groupby(['Country']).agg(Value=('Value', 'sum')).nsmallest(num_countries, 'Value')
            color = 'red'
    else:
        if selected_type == "Top":
            st.write(f"Top {num_countries} Countries with the Most Exports:")
            df_top = exp_data.groupby(['Country']).agg(Value=('Value', 'sum')).nlargest(num_countries, 'Value')
            color = 'green'
        else:
            st.write(f"Top {num_countries} Countries with the Least Exports:")
            df_top = exp_data.groupby(['Country']).agg(Value=('Value', 'sum')).nsmallest(num_countries, 'Value')
            color = 'orange'

    # Display top countries bar chart
    st.subheader(f"{selected_type} Countries - {selected_category}")
    chart_top_countries = alt.Chart(df_top.reset_index()).mark_bar(color=color).encode(
        x=alt.X('Value:Q', axis=alt.Axis(title="Value (in $)")),
        y=alt.Y('Country:N', axis=alt.Axis(title="Country")),
        tooltip=['Country', 'Value']
    ).properties(
        width=700,
        height=400,
        title=f"{selected_type} Countries - {selected_category}"
    )
    st.altair_chart(chart_top_countries)

    # Allow user to select a specific country from the top countries
    selected_country = st.selectbox("Select a country:", df_top.index)
    
    if selected_country:
        st.subheader(f"Import and Export Data for {selected_country}")
        if selected_category == "Imports":
            country_data = imp_data[imp_data['Country'] == selected_country]
        else:
            country_data = exp_data[exp_data['Country'] == selected_country]

        # Display import and export trends as bar plots
        st.subheader("Import Trend:")
        imp_chart = alt.Chart(country_data).mark_bar(color='blue').encode(
            x='Year',
            y='Value',
            tooltip=['Year', 'Value', 'Commodity']
        ).properties(
            width=700,
            height=300,
            title='Import Trend'
        )
        st.altair_chart(imp_chart)

        st.subheader("Export Trend:")
        exp_chart = alt.Chart(country_data).mark_bar(color='green').encode(
            x='Year',
            y='Value',
            tooltip=['Year', 'Value', 'Commodity']
        ).properties(
            width=700,
            height=300,
            title='Export Trend'
        )
        st.altair_chart(exp_chart)

        # Allow user to select whether they want to see top or low products
        selected_product_type = st.radio("Select Product Type:", ("Top", "Low"))

        if selected_product_type == "Top":
            st.write(f"Top Products for {selected_country} - {selected_category}:")
            df_products = country_data.nlargest(10, 'Value')  # Display top 10 products
        else:
            st.write(f"Low Products for {selected_country} - {selected_category}:")
            df_products = country_data.nsmallest(10, 'Value')  # Display lowest 10 products

        # Display bar chart for products
        st.subheader(f"Product-wise {selected_product_type} Products - {selected_category}")
        product_chart = alt.Chart(df_products.reset_index()).mark_bar(color=color).encode(
            x=alt.X('Value:Q', axis=alt.Axis(title="Value (in $)")),
            y=alt.Y('Commodity:N', axis=alt.Axis(title="Product")),
            tooltip=['Commodity', 'Value']
        ).properties(
            width=700,
            height=400,
            title=f"{selected_product_type} Products - {selected_category}"
        )
        st.altair_chart(product_chart)

        # Allow user to select products for stacked bar chart
        selected_products_stacked = st.multiselect("Select Products:", df_products['Commodity'].unique())
        if selected_products_stacked:
            # Filter data for selected products
            selected_product_data_stacked = country_data[country_data['Commodity'].isin(selected_products_stacked)]

            # Group by year and product
            grouped_data_stacked = selected_product_data_stacked.groupby(['Year', 'Commodity']).agg({'Value': 'sum'}).reset_index()

            # Stacked Bar Chart for Year-wise data
            stacked_bar_chart = alt.Chart(grouped_data_stacked).mark_bar().encode(
                x='Year:N',
                y='Value:Q',
                color='Commodity:N',
                tooltip=['Year', 'Commodity', 'Value']
            ).properties(
                width=700,
                height=400,
                title='Year-wise Data'
            )
            st.subheader("Year-wise Data:")
            st.altair_chart(stacked_bar_chart)

except ValueError:
    st.write("Please enter a valid number.")

# Now, add the new code snippet provided

# Trade Deficit Calculation
if include_trade_deficit:
    st.write("Trade Deficit")
    st.write("Trade deficit is a crucial economic indicator that measures the difference between the value of a country's imports and exports. If a country's imports exceed its exports, it incurs a trade deficit. This can indicate that the country is consuming more than it is producing, relying on imports to meet its needs.")
    st.write("Trade Surplus")
    st.write("On the other hand, if a country's exports exceed its imports, it experiences a trade surplus. A trade surplus can suggest that the country is producing more than it consumes, leading to an excess of goods and services for export.")
    st.write("Here, we're analyzing that Pakistan's overall imports have exceeded its exports during this period, leading to a trade deficit.")

    df = imp_data.groupby(['Year']).agg(Imports=('Value','sum'))
    df2 = exp_data.groupby(['Year']).agg(Exports=('Value','sum'))

    # Calculate the trade deficit by subtracting exports from imports
    df['Trade Deficit'] = df2['Exports'] - df['Imports']

    # Calculate overall totals for imports, exports, and trade deficit
    total_imports = df['Imports'].sum()
    total_exports = df2['Exports'].sum()
    overall_trade = total_imports + total_exports
    overall_deficit = df['Trade Deficit'].sum()

    # Calculate percentage values
    df['Imports (%)'] = df['Imports'] / total_imports * 100
    df2['Exports (%)'] = df2['Exports'] / total_exports * 100
    df['Trade Deficit (%)'] = df['Trade Deficit'] / overall_deficit * 100

    st.subheader('Yearwise Trade Deficit')

    # Display line chart for imports
    st.subheader("Imports Over Time")
    imp_chart = alt.Chart(df.reset_index()).mark_bar(color='blue').encode(
        x='Year:N',
        y='Imports',
        tooltip=['Year', 'Imports']
    ).properties(
        width=600,
        height=300,
        title='Imports Over Time'
    )
    st.altair_chart(imp_chart)

    # Display line chart for exports
    st.subheader("Exports Over Time")
    exp_chart = alt.Chart(df2.reset_index()).mark_bar(color='green').encode(
        x='Year:N',
        y='Exports',
        tooltip=['Year', 'Exports']
    ).properties(
        width=600,
        height=300,
        title='Exports Over Time'
    )
    st.altair_chart(exp_chart)

    # Display line chart for trade deficit
    st.subheader("Trade Deficit Over Time")
    deficit_chart = alt.Chart(df.reset_index()).mark_bar(color='red').encode(
        x='Year:N',
        y='Trade Deficit',
        tooltip=['Year', 'Trade Deficit']
    ).properties(
        width=600,
        height=300,
        title='Trade Deficit Over Time'
    )
    st.altair_chart(deficit_chart)

    # Display tabular data for yearly imports, exports, and trade deficit with percentages
    st.subheader("Yearly Trade and Deficit Data")
    trade_deficit_data = df.merge(df2, on='Year')
    trade_deficit_data = trade_deficit_data[['Imports', 'Imports (%)', 'Exports', 'Exports (%)', 'Trade Deficit', 'Trade Deficit (%)']]
    st.write(trade_deficit_data)

    # Display overall percentage data
    st.subheader("Overall Trade and Deficit Percentage (2015-2019)")
    overall_data = pd.DataFrame({
        'Total Imports': [total_imports, total_imports / overall_trade * 100],
        'Total Exports': [total_exports, total_exports / overall_trade * 100],
        'Total Trade Deficit': [overall_deficit, overall_deficit / overall_trade * 100]
    }, index=['Total Value', 'Percentage of Total Trade'])
    st.write(overall_data)
