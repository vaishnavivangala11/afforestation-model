from fpdf import FPDF
import io
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import tempfile
import os

# Load Excel data
df = pd.read_excel("local_tree_species_data.xlsx")

st.set_page_config(page_title="Afforestation Impact – East Godavari")
st.title("🌳 Afforestation Impact Modelling")

# Tree dropdown
tree = st.selectbox("Select a Tree Species", df["Tree Name"])

# Tree age input
age = st.slider("Enter Tree Age (in Years)", min_value=1, max_value=200)

# Get selected row
selected_tree = df[df["Tree Name"] == tree].iloc[0]

# Adjusted CO2 calculation
co2_per_year = selected_tree["CO2_per_year_kg"]
survival_rate = selected_tree["Survival_rate"] / 100

growth_factor = selected_tree["Growth_Factor"] / 100
adjusted_co2 = age * co2_per_year * survival_rate * growth_factor

# Display CO2
st.success(f"🌱 A {tree} tree absorbs approx. **{adjusted_co2:.1f} kg of CO₂** over {age} years (adjusted for survival & growth).")

# CO₂ Sequestration Over 20 Years
st.subheader("📈 CO₂ Sequestration Over 20 Years")

selected_species = st.selectbox("Choose a tree species for the graph:", df["Tree Name"])
species_row = df[df["Tree Name"] == selected_species].iloc[0]

# Adjusted rate for graph
co2_rate = species_row["CO2_per_year_kg"]
survival = species_row["Survival_Rate"] / 100
growth = species_row["Growth_Factor"] / 100
adjusted_rate = co2_rate * survival * growth

years = list(range(1, 21))
co2_values = [adjusted_rate * year for year in years]

# Plot graph 1
fig, ax = plt.subplots()
ax.plot(years, co2_values, marker='o', color='green')
ax.set_xlabel("Year")
ax.set_ylabel("Cumulative CO₂ Captured (kg)")
ax.set_title(f"CO₂ Capture by {selected_species} Over 20 Years")
st.pyplot(fig)

# What if 1000 trees
st.subheader("🧠 What if 1000 Trees Are Planted?")
co2_per_tree = adjusted_rate
co2_1000_trees = [co2_per_tree * year * 1000 for year in years]

# Plot graph 2
fig2, ax2 = plt.subplots()
ax2.plot(years, co2_1000_trees, marker='s', color='orange')
ax2.set_xlabel("Year")
ax2.set_ylabel("Total CO₂ Captured (kg)")
ax2.set_title(f"CO₂ Sequestration for 1000 {selected_species} Trees Over 20 Years")
st.pyplot(fig2)

total_20_years = co2_1000_trees[-1]
st.success(f"🌍 Planting 1000 {selected_species} trees can absorb **{total_20_years:,.0f} kg** of CO₂ in 20 years.")

# PDF Report Generation
st.subheader("📄 Generate PDF Report")
if st.button("📄 Create and Download PDF Report"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=16)
    pdf.cell(200, 10, txt="Afforestation CO2 Report", ln=True, align='C')

    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Tree Species: {selected_species}", ln=True)
    pdf.cell(200, 10, txt=f"Tree Age: {age} years", ln=True)
    pdf.cell(200, 10, txt=f"Adjusted CO2 by 1 Tree: {adjusted_co2:.2f} kg", ln=True)
    pdf.cell(200, 10, txt=f"CO2 by 1000 Trees in 20 years: {int(total_20_years):,} kg", ln=True)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
        fig3, ax3 = plt.subplots()
        ax3.plot(years, co2_1000_trees, marker='s', color='orange')
        ax3.set_xlabel("Year")
        ax3.set_ylabel("Total CO₂ Captured (kg)")
        ax3.set_title(f"1000 {selected_species} Trees Over 20 Years")
        fig3.savefig(tmpfile.name)
        plt.close(fig3)

        pdf.image(tmpfile.name, x=10, y=80, w=180)

    try:
        os.remove(tmpfile.name)
    except PermissionError:
        pass

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as pdf_file:
        pdf.output(pdf_file.name)
        with open(pdf_file.name, "rb") as f:
            st.download_button("⬇️ Download PDF Report", f, file_name="afforestation_report.pdf", mime="application/pdf")

# Map of East Godavari
st.subheader("🗺️ East Godavari Map")

east_godavari_coords = {
    "latitude": 17.0,
    "longitude": 82.2
}
map_df = pd.DataFrame({
    'lat': [east_godavari_coords["latitude"]],
    'lon': [east_godavari_coords["longitude"]]
})
st.map(map_df, zoom=9)

# SDG Impact Section
st.subheader("🌍 SDG Impact")
st.markdown("""
Afforestation initiative in East Godavari aligns with several **United Nations Sustainable Development Goals (SDGs)**:

- 🌳 **SDG 13: Climate Action**  
  Trees absorb CO₂, helping fight climate change.

- 💧 **SDG 6: Clean Water and Sanitation**  
  Forests improve water retention and prevent soil erosion.

- 🐾 **SDG 15: Life on Land**  
  Supports biodiversity by creating habitats for wildlife.

- 👩‍🌾 **SDG 1 & 8: No Poverty & Decent Work**  
  Tree-planting creates local jobs and improves livelihoods.

Together, these make project **socially impactful and environmentally powerful**. 💚
""")

