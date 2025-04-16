import streamlit as st
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, DensityMatrix, Operator
from qiskit.visualization import plot_bloch_vector
import numpy as np
import matplotlib.pyplot as plt

# Helper: Bloch vector from state
def get_bloch_vector(state):
    if isinstance(state, Statevector):
        a, b = state.data
        x = 2 * np.real(np.conj(a) * b)
        y = 2 * np.imag(np.conj(a) * b)
        z = np.abs(a)**2 - np.abs(b)**2
        return [x, y, z]
    elif isinstance(state, DensityMatrix):
        rho = state.data
        x = 2 * np.real(rho[0, 1])
        y = 2 * np.imag(rho[1, 0])
        z = np.real(rho[0, 0] - rho[1, 1])
        return [x, y, z]

# App
st.title("🔮 Bloch Sphere Visualizer")

st.header("Step 1: Enter Initial State")
input_type = st.selectbox("Select input type:", ["Predefined State", "Custom Pure State", "Density Matrix"])

# 1. Predefined
if input_type == "Predefined State":
    state_options = {
        "|0⟩": Statevector.from_label("0"),
        "|1⟩": Statevector.from_label("1"),
        "|+⟩ = (|0⟩ + |1⟩)/√2": Statevector([1/np.sqrt(2), 1/np.sqrt(2)]),
        "|-⟩ = (|0⟩ - |1⟩)/√2": Statevector([1/np.sqrt(2), -1/np.sqrt(2)]),
        "|i⟩ = (|0⟩ + i|1⟩)/√2": Statevector([1/np.sqrt(2), 1j/np.sqrt(2)]),
        "|-i⟩ = (|0⟩ - i|1⟩)/√2": Statevector([1/np.sqrt(2), -1j/np.sqrt(2)]),
    }
    label = st.selectbox("Choose state:", list(state_options.keys()))
    state = state_options[label]

# 2. Custom Pure State
elif input_type == "Custom Pure State":
    st.write("Enter complex amplitudes for |\u03c8⟩ = a|0⟩ + b|1⟩")
    a_real = st.number_input("Re(a)", value=1.0)
    a_imag = st.number_input("Im(a)", value=0.0)
    b_real = st.number_input("Re(b)", value=0.0)
    b_imag = st.number_input("Im(b)", value=0.0)
    a = complex(a_real, a_imag)
    b = complex(b_real, b_imag)
    norm = np.sqrt(abs(a)**2 + abs(b)**2)
    if norm == 0:
        st.error("Vector cannot be zero.")
        state = None
    else:
        state = Statevector([a / norm, b / norm])

# 3. Density Matrix
elif input_type == "Density Matrix":
    st.write("Enter 2x2 complex density matrix elements ρ01")
    try:
        r00 = complex(st.text_input("ρ00", "0.5"))
        r01 = complex(st.text_input("ρ01", "0.5"))
        r10 = complex(st.text_input("ρ10", "0.5"))
        r11 = complex(st.text_input("ρ11", "0.5"))

        matrix = np.array([[r00, r01], [r10, r11]], dtype=complex)

        is_hermitian = np.allclose(matrix, matrix.conj().T)
        trace = np.trace(matrix)
        is_trace_one = np.allclose(trace, 1)
        eigenvals = np.linalg.eigvalsh(matrix)
        is_positive_semidefinite = np.all(eigenvals >= -1e-10)

        if not is_hermitian:
            st.error("❌ Matrix is not Hermitian (ρ ≠ ρ†).")
        if not is_trace_one:
            st.error(f"❌ Trace is not 1 (Trace = {trace}).")
        if not is_positive_semidefinite:
            st.error(f"❌ Matrix is not positive semi-definite (eigenvalues: {eigenvals}).")

        if is_hermitian and is_trace_one and is_positive_semidefinite:
            state = DensityMatrix(matrix)
            st.success("✅ Valid density matrix!")
        else:
            state = None

    except Exception as e:
        st.error(f"❌ Invalid input: {e}")
        state = None

# Plot initial
if state is not None:
    st.subheader("Initial State on Bloch Sphere")
    fig = plot_bloch_vector(get_bloch_vector(state))
    st.pyplot(fig)

    # Show initial state data
    st.write("🔢 Initial State Mathematical Representation:")
    if isinstance(state, Statevector):
        st.code(str(state.data), language="python")
    elif isinstance(state, DensityMatrix):
        st.code(str(state.data), language="python")


    st.header("Step 2: Apply Gates")
    mode = st.radio("Choose mode:", ["Test Single Gate", "Test Gate Sequence"])

    if mode == "Test Single Gate":
        gate = st.selectbox("Choose a gate to apply:", ["X", "Y", "Z", "H", "S", "Sdg", "T", "Tdg", "RX", "RY", "RZ", "Custom Unitary"])
        angle = 0
        custom_matrix = None

        if gate in ["RX", "RY", "RZ"]:
            angle = st.slider(f"Rotation angle for {gate} (radians)", -2*np.pi, 2*np.pi, 0.0, step=0.01)

        if gate == "Custom Unitary":
            try:
                u00 = complex(st.text_input("U00", "1"))
                u01 = complex(st.text_input("U01", "0"))
                u10 = complex(st.text_input("U10", "0"))
                u11 = complex(st.text_input("U11", "1"))
                custom_matrix = np.array([[u00, u01], [u10, u11]], dtype=complex)
                if not np.allclose(custom_matrix.conj().T @ custom_matrix, np.eye(2)):
                    st.error("❌ Matrix is not unitary.")
                    custom_matrix = None
            except:
                st.error("Invalid matrix elements.")

        if st.button("Apply Gate"):
            qc = QuantumCircuit(1)
            if gate == "X": qc.x(0)
            elif gate == "Y": qc.y(0)
            elif gate == "Z": qc.z(0)
            elif gate == "H": qc.h(0)
            elif gate == "S": qc.s(0)
            elif gate == "Sdg": qc.sdg(0)
            elif gate == "T": qc.t(0)
            elif gate == "Tdg": qc.tdg(0)
            elif gate == "RX": qc.rx(angle, 0)
            elif gate == "RY": qc.ry(angle, 0)
            elif gate == "RZ": qc.rz(angle, 0)
            elif gate == "Custom Unitary" and custom_matrix is not None:
                op = Operator(custom_matrix)
                state = op @ state
                qc = None

            if qc is not None:
                state = state.evolve(qc)

            st.subheader("Final State after Gate")
            fig2 = plot_bloch_vector(get_bloch_vector(state))
            st.pyplot(fig2)
            st.write("Final State Mathematical Representation:")
            st.code(str(state.data), language="python")

    elif mode == "Test Gate Sequence":
        if "gate_sequence" not in st.session_state:
            st.session_state.gate_sequence = []

        gate = st.selectbox("Choose a gate to add:", ["X", "Y", "Z", "H", "S", "Sdg", "T", "Tdg", "RX", "RY", "RZ", "Custom Unitary"])
        angle = 0
        custom_matrix = None

        if gate in ["RX", "RY", "RZ"]:
            angle = st.slider(f"Rotation angle for {gate} (radians)", -2*np.pi, 2*np.pi, 0.0, step=0.01)

        if gate == "Custom Unitary":
            try:
                u00 = complex(st.text_input("U00", "1"))
                u01 = complex(st.text_input("U01", "0"))
                u10 = complex(st.text_input("U10", "0"))
                u11 = complex(st.text_input("U11", "1"))
                custom_matrix = np.array([[u00, u01], [u10, u11]], dtype=complex)
                if not np.allclose(custom_matrix.conj().T @ custom_matrix, np.eye(2)):
                    st.error("❌ Matrix is not unitary.")
                    custom_matrix = None
            except:
                st.error("Invalid matrix elements.")

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Add Gate"):
                if gate in ["RX", "RY", "RZ"]:
                    st.session_state.gate_sequence.append((gate, angle))
                elif gate == "Custom Unitary" and custom_matrix is not None:
                    st.session_state.gate_sequence.append(("Custom", custom_matrix))
                else:
                    st.session_state.gate_sequence.append((gate, None))
        with col2:
            if st.button("Undo Last Gate") and st.session_state.gate_sequence:
                st.session_state.gate_sequence.pop()
        with col3:
            if st.button("Clear Gate Sequence"):
                st.session_state.gate_sequence = []

        def format_gate(g, param):
            if g in ["RX", "RY", "RZ"]:
                return f"{g}({round(param, 2)})"
            elif g == "Custom":
                return "CustomUnitary"
            else:
                return g

        formatted_seq = [format_gate(g, p) for g, p in st.session_state.gate_sequence]
        st.write(f"🧩 Current Gate Sequence: {' → '.join(formatted_seq)}")

        state_applied = state
        for g, p in st.session_state.gate_sequence:
            qc = QuantumCircuit(1)
            if g == "X": qc.x(0)
            elif g == "Y": qc.y(0)
            elif g == "Z": qc.z(0)
            elif g == "H": qc.h(0)
            elif g == "S": qc.s(0)
            elif g == "Sdg": qc.sdg(0)
            elif g == "T": qc.t(0)
            elif g == "Tdg": qc.tdg(0)
            elif g == "RX": qc.rx(p, 0)
            elif g == "RY": qc.ry(p, 0)
            elif g == "RZ": qc.rz(p, 0)
            elif g == "Custom":
                op = Operator(p)
                state_applied = op @ state_applied
                qc = None

            if qc is not None:
                state_applied = state_applied.evolve(qc)

        st.subheader("Final State after Applying Gates")
        fig2 = plot_bloch_vector(get_bloch_vector(state_applied))
        st.pyplot(fig2)
        st.write("🔢 Final State Mathematical Representation:")
        st.code(str(state_applied.data), language="python")
