import streamlit as st
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt

# Load the dataset
@st.cache_data
def load_data():
    imp_data = pd.read_csv("pakistan_import_data.csv")
    exp_data = pd.read_csv("pakistan_export_data.csv")
    return imp_data, exp_data

imp_data, exp_data = load_data()

# Sidebar
# st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Select Pages: ", ("Import Analysis", "Export Analysis", "Trade Comparison","Overall Trade Analysis"))

if page == "Import Analysis":
    # Import Analysis
    st.title("Import Analysis")
    
    # Sidebar for Import Analysis
    st.sidebar.title("Import Analysis Options")
    selected_type_imp = st.sidebar.radio("Select Data Type:", ("Top", "Low"))
    num_countries_imp = st.sidebar.text_input("Enter the number of countries:", "10")

    try:
        num_countries_imp = int(num_countries_imp)
        if num_countries_imp > 243:
            num_countries_imp = 243
    except:
        num_countries_imp = 10

    # Main content for Import Analysis
    try:
        if selected_type_imp == "Top":
            st.write(f"Top {num_countries_imp} Countries with the Most Imports:")
            df_top_imp = imp_data.groupby(['Country']).agg(Value=('Value', 'sum')).nlargest(num_countries_imp, 'Value')
            color_imp = 'blue'
        else:
            st.write(f"Top {num_countries_imp} Countries with the Least Imports:")
            df_top_imp = imp_data.groupby(['Country']).agg(Value=('Value', 'sum')).nsmallest(num_countries_imp, 'Value')
            color_imp = 'red'

        # chart_color_imp = st.sidebar.color_picker("Select Chart Color", "#0732FF")  # Default color: blue

        # Display top countries bar chart for imports
        st.subheader(f"{selected_type_imp} Countries with the Most Imports")
        chart_top_countries_imp = alt.Chart(df_top_imp.reset_index()).mark_bar(color=color_imp).encode(
            x=alt.X('Value:Q', axis=alt.Axis(title="Value (in $)"), sort='-y'),  # Sort descending by value
            y=alt.Y('Country:N', axis=alt.Axis(title="Country")),
            tooltip=['Country', 'Value']
        ).properties(
            width=700,
            height=400,
            title=f"{selected_type_imp} Countries with the Most Imports"
        )
        st.altair_chart(chart_top_countries_imp)

        # Allow user to select a specific country from the top countries for imports
        selected_country_imp = st.selectbox("Select a country:", df_top_imp.index)
        
        if selected_country_imp:
            st.subheader(f"Import Data for {selected_country_imp}")
            country_data_imp = imp_data[imp_data['Country'] == selected_country_imp]

            # Display import trend as bar plot for imports
            st.subheader("Import Trend:")
            imp_chart = alt.Chart(country_data_imp).mark_bar(color='blue').encode(
                x='Year',
                y='Value',
                tooltip=['Year', 'Value', 'Commodity']
            ).properties(
                width=700,
                height=300,
                title='Import Trend'
            )
            st.altair_chart(imp_chart)
            
            # Allow user to select whether they want to see top or low products for imports
            selected_product_type_imp = st.radio("Select Product Type:", ("Top", "Low"))

            if selected_product_type_imp == "Top":
                st.write(f"Top Products for {selected_country_imp} - Imports:")
                df_products_imp = country_data_imp.nlargest(10, 'Value')  # Display top 10 products for imports
            else:
                st.write(f"Low Products for {selected_country_imp} - Imports:")
                df_products_imp = country_data_imp.nsmallest(10, 'Value')  # Display lowest 10 products for imports

            # Display bar chart for products for imports
            st.subheader(f"Product-wise {selected_product_type_imp} Products - Imports")
            product_chart_imp = alt.Chart(df_products_imp.reset_index()).mark_bar(color=color_imp).encode(
                x=alt.X('Value:Q', axis=alt.Axis(title="Value (in $)"), sort='-y'),  # Sort descending by value
                y=alt.Y('Commodity:N', axis=alt.Axis(title="Product")),
                tooltip=['Commodity', 'Value']
            ).properties(
                width=700,
                height=400,
                title=f"{selected_product_type_imp} Products - Imports"
            )
            st.altair_chart(product_chart_imp)

            selected_products_stacked = st.multiselect("Select Products:", df_products_imp['Commodity'].unique())
            if selected_products_stacked:
                # Filter data for selected products
                selected_product_data_stacked = country_data_imp[country_data_imp['Commodity'].isin(selected_products_stacked)]

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

elif page == "Export Analysis":
    # Export Analysis
    st.title("Export Analysis")
    
    # Sidebar for Export Analysis
    st.sidebar.title("Export Analysis Options")
    selected_type_exp = st.sidebar.radio("Select Data Type:", ("Top", "Low"))
    num_countries_exp = st.sidebar.text_input("Enter the number of countries:", "10")

    try:
        num_countries_exp = int(num_countries_exp)
        if num_countries_exp > 243:
            num_countries_exp = 243
    except:
        num_countries_exp = 10

    # Main content for Export Analysis
    try:
        if selected_type_exp == "Top":
            st.write(f"Top {num_countries_exp} Countries with the Most Exports:")
            df_top_exp = exp_data.groupby(['Country']).agg(Value=('Value', 'sum')).nlargest(num_countries_exp, 'Value')
            color_exp = 'green'
        else:
            st.write(f"Top {num_countries_exp} Countries with the Least Exports:")
            df_top_exp = exp_data.groupby(['Country']).agg(Value=('Value', 'sum')).nsmallest(num_countries_exp, 'Value')
            color_exp = 'orange'

        # chart_color_exp = st.sidebar.color_picker("Select Chart Color", "#2ca02c")  
        # Display top countries bar chart for exports
        st.subheader(f"{selected_type_exp} Countries with the Most Exports")
        chart_top_countries_exp = alt.Chart(df_top_exp.reset_index()).mark_bar(color=color_exp).encode(
            x=alt.X('Value:Q', axis=alt.Axis(title="Value (in $)"), sort='-y'),  # Sort descending by value
            y=alt.Y('Country:N', axis=alt.Axis(title="Country")),
            tooltip=['Country', 'Value']
        ).properties(
            width=700,
            height=400,
            title=f"{selected_type_exp} Countries with the Most Exports"
        )
        st.altair_chart(chart_top_countries_exp)

        # Allow user to select a specific country from the top countries for exports
        selected_country_exp = st.selectbox("Select a country:", df_top_exp.index)
        
        if selected_country_exp:
            st.subheader(f"Export Data for {selected_country_exp}")
            country_data_exp = exp_data[exp_data['Country'] == selected_country_exp]

            # Display export trend as bar plot for exports
            st.subheader("Export Trend:")
            exp_chart = alt.Chart(country_data_exp).mark_bar(color='green').encode(
                x='Year',
                y='Value',
                tooltip=['Year', 'Value', 'Commodity']
            ).properties(
                width=700,
                height=300,
                title='Export Trend'
            )
            st.altair_chart(exp_chart)
            
            # Allow user to select whether they want to see top or low products for exports
            selected_product_type_exp = st.radio("Select Product Type:", ("Top", "Low"))

            if selected_product_type_exp == "Top":
                st.write(f"Top Products for {selected_country_exp} - Exports:")
                df_products_exp = country_data_exp.nlargest(10, 'Value')  # Display top 10 products for exports
            else:
                st.write(f"Low Products for {selected_country_exp} - Exports:")
                df_products_exp = country_data_exp.nsmallest(10, 'Value')  # Display lowest 10 products for exports

            # Display bar chart for products for exports
            st.subheader(f"Product-wise {selected_product_type_exp} Products - Exports")
            product_chart_exp = alt.Chart(df_products_exp.reset_index()).mark_bar(color=color_exp).encode(
                x=alt.X('Value:Q', axis=alt.Axis(title="Value (in $)"), sort='-y'),  # Sort descending by value
                y=alt.Y('Commodity:N', axis=alt.Axis(title="Product")),
                tooltip=['Commodity', 'Value']
            ).properties(
                width=700,
                height=400,
                title=f"{selected_product_type_exp} Products - Exports"
            )
            st.altair_chart(product_chart_exp)


            selected_products_stacked = st.multiselect("Select Products:", df_products_exp['Commodity'].unique())
            if selected_products_stacked:
                # Filter data for selected products
                selected_product_data_stacked = country_data_exp[country_data_exp['Commodity'].isin(selected_products_stacked)]

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

elif page == "Trade Comparison":
    st.title("Country-Wise Trade Comparison")
    
    # Calculate top countries imports and exports
    df3 = imp_data.groupby(['Country']).agg(Value=('Value', 'sum'))
    df3 = df3.sort_values(by='Value', ascending=False)
    df3 = df3

    df4 = exp_data.groupby(['Country']).agg(Value=('Value', 'sum'))
    df4 = df4.sort_values(by='Value', ascending=False)
    df4 = df4

    # Dropdown menu for selecting a country
    selected_country = st.selectbox("Select a Country:", df3.index)

    if selected_country:
        imp_value = imp_data[imp_data['Country'].str.contains(selected_country, case=False)]['Value'].sum()
        exp_value = exp_data[exp_data['Country'].str.contains(selected_country, case=False)]['Value'].sum()
        st.write(f"Total Import value from {selected_country}: {imp_value}")
        st.write(f"Total Export value to {selected_country}: {exp_value}")
        if imp_value and exp_value:
            imp_country_data = imp_data[imp_data['Country'].str.contains(selected_country, case=False)]
            exp_country_data = exp_data[exp_data['Country'].str.contains(selected_country, case=False)]

            # Combine import and export data
            combined_data = pd.concat([imp_country_data, exp_country_data])

            # Color imports and exports differently
            combined_data['Type'] = ['Import'] * len(imp_country_data) + ['Export'] * len(exp_country_data)

            # Plot combined data
            bar_chart = alt.Chart(combined_data).mark_bar().encode(
                x='Year',
                y='Value',
                color='Type',
                tooltip=['Year', 'Value', 'Type']
            ).properties(
                width=700,
                height=400
            )

            st.altair_chart(bar_chart)
        

elif page == "Overall Trade Analysis":
    # Trade Deficit Analysis
    st.title("Overall Trade Analysis")

    # Rest of the code for trade deficit analysis...
    # Add the new code snippet provided for Trade Deficit Analysis here...
    # Ensure to maintain the indentation and structure of the code

    # Trade Deficit Calculation
    df_imp = imp_data.groupby(['Year']).agg(Imports=('Value','sum'))
    df_exp = exp_data.groupby(['Year']).agg(Exports=('Value','sum'))

    # Calculate the trade deficit by subtracting exports from imports
    df_imp['Trade Deficit'] = df_exp['Exports'] - df_imp['Imports']

    # Calculate overall totals for imports, exports, and trade deficit
    total_imports = df_imp['Imports'].sum()
    total_exports = df_exp['Exports'].sum()
    overall_trade = total_imports + total_exports
    overall_deficit = df_imp['Trade Deficit'].sum()

    # Calculate percentage values
    df_imp['Imports (%)'] = df_imp['Imports'] / total_imports * 100
    df_exp['Exports (%)'] = df_exp['Exports'] / total_exports * 100
    df_imp['Trade Deficit (%)'] = df_imp['Trade Deficit'] / overall_deficit * 100

    st.subheader('Yearwise Trade Deficit/Surplus')

    st.write("Here, we're analyzing that Pakistan's overall imports have exceeded its exports during this period, leading to a trade deficit.")

    # Display line chart for imports
    st.subheader("Imports Over Time")
    imp_chart = alt.Chart(df_imp.reset_index()).mark_bar(color='blue').encode(
        x='Year:N',
        y='Imports',
        tooltip=['Year', 'Imports']
    ).properties(
        width=600,
        height=300,
    )
    st.altair_chart(imp_chart)

    # Display line chart for exports
    st.subheader("Exports Over Time")
    exp_chart = alt.Chart(df_exp.reset_index()).mark_bar(color='green').encode(
        x='Year:N',
        y='Exports',
        tooltip=['Year', 'Exports']
    ).properties(
        width=600,
        height=300,
    )
    st.altair_chart(exp_chart)

    # Display line chart for trade deficit
    st.subheader("Trade Deficit Over Time")
    deficit_chart = alt.Chart(df_imp.reset_index()).mark_bar(color='red').encode(
        x='Year:N',
        y='Trade Deficit',
        tooltip=['Year', 'Trade Deficit']
    ).properties(
        width=600,
        height=300,
    )
    st.altair_chart(deficit_chart)

    # Display tabular data for yearly imports, exports, and trade deficit with percentages
    st.subheader("Yearly Trade and Deficit Data")
    trade_deficit_data = df_imp.merge(df_exp, on='Year')
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


# # Feedback Section
# st.sidebar.title("Feedback")
# user_feedback = st.sidebar.text_area("Share your feedback")

# if st.sidebar.button("Submit"):
#     if user_feedback:
#         st.sidebar.success("Thank you for your feedback!")
#     else:
#         st.sidebar.warning("Please provide your feedback before submitting.")
