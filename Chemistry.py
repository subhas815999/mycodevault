!pip install pubchempy -q

import pubchempy as pcp

def get_basic_compound_info(compound_name):
    try:
        # Fetch compound data from PubChem
        compound = pcp.get_compounds(compound_name, 'name')[0]
        iupac_name = compound.iupac_name or "N/A"
        formula = compound.molecular_formula or "N/A"

        print("\n--- Compound Info ---")
        print("🔍 Name       :", compound_name)
        print("🧬 IUPAC Name :", iupac_name)
        print("🧫 Formula    :", formula)

    except Exception as e:
        print("❌ Error:", e)
        print("Compound not found or there is a connection issue.")

compound_input = input("🔍 Enter any compound name: ")
get_basic_compound_info(compound_input)
