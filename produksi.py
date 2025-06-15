import streamlit as st
from scipy.optimize import linprog
import pandas as pd

st.title("🔧 Optimasi Produksi - Linear Programming")

st.markdown("Masukkan data produksi di bawah ini:")

# Input parameter keuntungan
profit_A = st.number_input("Keuntungan per unit Produk A", min_value=0.0, value=30.0)
profit_B = st.number_input("Keuntungan per unit Produk B", min_value=0.0, value=20.0)

# Input batasan sumber daya
st.subheader("Batasan Sumber Daya")

resource_1 = st.number_input("Jumlah maksimum Sumber Daya 1 (misal: jam mesin)", min_value=1.0, value=100.0)
resource_2 = st.number_input("Jumlah maksimum Sumber Daya 2 (misal: jam kerja)", min_value=1.0, value=80.0)

# Konsumsi per unit
st.markdown("*Konsumsi per Unit Produk*")

cons_A_r1 = st.number_input("Produk A - konsumsi Sumber Daya 1", min_value=0.0, value=2.0)
cons_B_r1 = st.number_input("Produk B - konsumsi Sumber Daya 1", min_value=0.0, value=1.0)

cons_A_r2 = st.number_input("Produk A - konsumsi Sumber Daya 2", min_value=0.0, value=1.0)
cons_B_r2 = st.number_input("Produk B - konsumsi Sumber Daya 2", min_value=0.0, value=1.0)

if st.button("🔍 Hitung Optimasi"):
    # Fungsi objektif (negatif karena linprog meminimalkan)
    c = [-profit_A, -profit_B]

    # Matriks kendala (Ax <= b)
    A = [
        [cons_A_r1, cons_B_r1],  # kendala sumber daya 1
        [cons_A_r2, cons_B_r2]   # kendala sumber daya 2
    ]
    b = [resource_1, resource_2]

    # Batasan (x >= 0)
    x_bounds = (0, None)
    bounds = [x_bounds, x_bounds]

    # Optimisasi
    result = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')

    if result.success:
        produk_A = result.x[0]
        produk_B = result.x[1]
        keuntungan = -result.fun

        st.success("✅ Optimasi berhasil ditemukan:")
        st.write(f"Produksi Produk A: *{produk_A:.2f} unit*")
        st.write(f"Produksi Produk B: *{produk_B:.2f} unit*")
        st.write(f"Total Keuntungan Maksimum: *Rp {keuntungan:,.2f}*")

        df = pd.DataFrame({
            "Produk": ["A", "B"],
            "Jumlah Produksi": [produk_A, produk_B],
            "Keuntungan per Unit": [profit_A, profit_B],
            "Total Keuntungan": [produk_A * profit_A, produk_B * profit_B]
        })

        st.dataframe(df)
    else:
        st.error("❌ Tidak ditemukan solusi optimal. Periksa parameter dan batasan.")