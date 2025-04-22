# 🔮 Bloch Sphere Visualizer

A Streamlit-based interactive tool for visualizing single-qubit quantum states on the Bloch sphere. Built using Qiskit, this app allows you to prepare custom states, apply quantum gates, and explore how they affect the qubit’s state vector.

## 🚀 Features

- Visualize pure states and density matrices on the Bloch sphere.
- Support for standard gates (X, Y, Z, H, S, T, S†, T†, RX, RY, RZ).
- Create and apply custom unitary gates.
- Two operation modes:
  - **Single-Gate Mode**: Instantly see the effect of any one gate.
  - **Gate Sequence Mode**: Build and simulate a series of gates step-by-step.
- View and compare initial and final quantum state data.


## 📦 Requirements

Install dependencies with:

```bash
pip install -r requirements.txt
```

## ▶️ Run the App

```bash
streamlit run app.py
```

## 🧠 Quantum Concepts Covered

- Qubit states and statevectors
- Bloch sphere representation
- Density matrices
- Quantum gates and rotations


## ✨ Made With

- [Streamlit](https://streamlit.io/)
- [Qiskit](https://qiskit.org/)
