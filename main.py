import streamlit as st
from stmol import showmol
import py3Dmol
from utils import read_mol

from rdkit import Chem
from rdkit.Chem import AllChem


def display_molecule(xyz):
    xyzview = py3Dmol.view()#(width=400,height=400)
    xyzview.addModel(xyz,'mol')
    xyzview.setStyle({'sphere':{}})
    xyzview.setBackgroundColor('white')
    xyzview.zoomTo()
    showmol(xyzview, height=500, width=500)


def main():
    st.header("Optimize molecular geometry using VQE")
    selected_mol = st.sidebar.selectbox("Select example molecule", ["H2O", "H3"])
    uploaded_xyz = st.sidebar.file_uploader("Upload XYZ file", accept_multiple_files=False, type="xyz")
    compound_smiles = st.sidebar.text_input('Provide SMILES string', '')
    molblock = read_mol(selected_mol)
    display_molecule(molblock)

if __name__ == "__main__":
    main()