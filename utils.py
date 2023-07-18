from pennylane import numpy as np
import pennylane as qml
from rdkit import Chem
import streamlit as st

device = qml.device("default.qubit", wires=6)

def read_mol(selected_mol):
    mol = Chem.rdmolfiles.MolFromXYZFile(f"assets/{selected_mol}.xyz")
    mol_block = Chem.MolToMolBlock(mol)

    symbols = []
    coordinates = []

    uploaded_molecule = "Uploaded molecule: \n \n"
    for i, atom in enumerate(mol.GetAtoms()):
        positions = mol.GetConformer().GetAtomPosition(i)
        uploaded_molecule += f"{atom.GetSymbol()}:    {positions.x:.3f}     {positions.y:.3f}     {positions.z:.3f} \n \n"
        
        symbols.append(atom.GetSymbol())
        coordinates.extend([positions.x, positions.y, positions.z])

    coordinates = np.array(coordinates, requires_grad=True)

    st.sidebar.info(uploaded_molecule)

    return mol_block, symbols, coordinates


def get_hamiltonian(symbols, coordinates):
    hamiltonian = qml.qchem.molecular_hamiltonian(symbols, coordinates, charge=1)[0]
    return hamiltonian


def get_hf_state(n_electrons=2, n_orbitals=6):
    hf_state = qml.qchem.hf_state(electrons=n_electrons, orbitals=n_orbitals)
    return hf_state


@qml.qnode(device, interface="autograd")
def circuit(params, obs, wires, hf_state):
    qml.BasisState(hf_state, wires=wires)
    qml.DoubleExcitation(params[0], wires=[0, 1, 2, 3])
    qml.DoubleExcitation(params[1], wires=[0, 1, 4, 5])
    return qml.expval(obs)


def loss_func(params, coordinates, n_wires=6):
    hamiltonian = get_hamiltonian(coordinates)
    return circuit(params, obs=hamiltonian, wires=range(n_wires))
