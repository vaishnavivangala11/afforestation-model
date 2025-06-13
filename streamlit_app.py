import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import tempfile
import os
from fpdf import FPDF

# Load your updated Excel data
df = pd.read_excel("local_tree_species_data.xlsx")

st.set_page_config(page_title="Afforestation Impact – East Godavari")
st.title("🌳 Afforestation Impact Modelling")

# Tree dropdown
tree = st.selectbox("Select a Tree Species", df["Tree Name"])

# Tree age input
age = st.slider("Enter Tree Age (in Years)", min_value=1, max_value=200)

# Get selected row
selected_tree = df[df["Tree Name"] == tree].iloc[0]

# Adjusted CO₂ based on survival and growth
survival_rate = selected_tree["Survival_rate"]
growth_factor = selected_tree["Growth_factor"]
adjusted_co2 = age * selected_tree["CO2_per_year_kg"] * survival_rate * growth_factor

# Display CO₂ and other details
st.success(f"🌱 A {tree} tree absorbs approx. **{adjusted_co2:.1f} kg of CO₂** over {age} years (adjusted for growth & survival).")
st.info(f"🧪 **Soil Type:** {selected_tree['Soil_Type']}\n\n📍 **Best Place to Plant:** {selected_tree['Best_Place_to_Plant']}")

# 📉 CO₂ Sequestration Over Time
st.subheader("📈 CO₂ Sequestration Over 20 Years")

selected_species = st.selectbox("Choose a tree species for the graph:", df["Tree Name"])
species_row = df[df["Tree Name"] == selected_species].iloc[0]
co2_rate = species_row["CO2_per_year_kg"]
survival = species_row["Survival_rate"]
growth = species_row["Growth_factor"]

years = list(range(1, 21))
co2_values = [co2_rate * year * survival * growth for year in years]

fig, ax = plt.subplots()
ax.plot(years, co2_values, marker='o', color='green')
ax.set_xlabel("Year")
ax.set_ylabel("Cumulative CO₂ Captured (kg)")
ax.set_title(f"CO₂ Capture by {selected_species} Over 20 Years")
st.pyplot(fig)

# What if 1000 trees
st.subheader("🧠 What if 1000 Trees Are Planted?")
co2_1000_trees = [co2_rate * year * 1000 * survival * growth for year in years]
total_20_years = co2_1000_trees[-1]

fig2, ax2 = plt.subplots()
ax2.plot(years, co2_1000_trees, marker='s', color='orange')
ax2.set_xlabel("Year")
ax2.set_ylabel("Total CO₂ Captured (kg)")
ax2.set_title(f"CO₂ Sequestration for 1000 {selected_species} Trees Over 20 Years")
st.pyplot(fig2)

st.success(f"🌍 Planting 1000 {selected_species} trees can absorb **{total_20_years:,.0f} kg** of CO₂ in 20 years.")

# PDF Report
st.subheader("📄 Generate PDF Report")
if st.button("📄 Create and Download PDF Report"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=16)
    pdf.cell(200, 10, txt="Afforestation CO2 Report", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Tree Species: {selected_species}", ln=True)
    pdf.cell(200, 10, txt=f"Soil Type: {species_row['Soil_Type']}", ln=True)
    pdf.cell(200, 10, txt=f"Best Place to Plant: {species_row['Best_Place_to_Plant']}", ln=True)
    pdf.cell(200, 10, txt=f"CO2 Absorbed by 1000 Trees in 20 years: {int(total_20_years):,} kg", ln=True)

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
    except:
        pass

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as pdf_file:
        pdf.output(pdf_file.name)
        with open(pdf_file.name, "rb") as f:
            st.download_button("⬇️ Download PDF Report", f, file_name="afforestation_report.pdf", mime="application/pdf")

# Map
st.subheader("🗺️ East Godavari Map")
map_df = pd.DataFrame({'lat': [17.0], 'lon': [82.2]})
st.map(map_df, zoom=9)

# SDG Text
st.subheader("🌍 SDG Impact")
st.markdown("""
### 🎯 Sustainable Development Goals (SDGs) Impact

By promoting tree planting using real local species in East Godavari, this project actively supports the following SDGs:

- ✅ **SDG 13: Climate Action**  
  Trees capture atmospheric CO₂, directly contributing to climate change mitigation.

- ✅ **SDG 15: Life on Land**  
  Afforestation enhances biodiversity, restores degraded lands, and supports ecosystem balance.

- ✅ **SDG 6: Clean Water and Sanitation**  
  Improved green cover supports better water infiltration and protects watersheds.

- ✅ **SDG 3: Good Health and Well-being**  
  More trees mean cleaner air, shade, and improved physical and mental health for communities.

- ✅ **SDG 1 & 8: No Poverty & Decent Work**  
  Tree plantation drives create jobs and improve rural livelihoods through nursery and forestry work.

---
By combining science, local knowledge, and technology, our project promotes sustainability . 💚
""")
🌱 *st.markdown("""
---
🌳 st.markdown("""
---
🌳 *Your simple act of planting a tree supports global goals and local futures.*  
✅ From cleaner air to better jobs, every tree brings us one step closer to the SDGs.
""")

