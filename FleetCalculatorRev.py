import streamlit as st
import pandas as pd

# Data konversi jarak
data_konversi = {
    "jarak": [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2,
              1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3,
              2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0, 3.1, 3.2, 3.3, 3.4,
              3.5, 3.6, 3.7, 3.8, 3.9, 4.0, 4.1, 4.2, 4.3, 4.4, 4.5,
              4.6, 4.7, 4.8, 4.9, 5.0, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6,
              5.7, 5.8, 5.9, 6.0, 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7],
    "konversi": [1.342, 1.342, 1.342, 1.342, 1.342, 1.231, 1.140, 1.064, 1.000,
                 0.945, 0.898, 0.856, 0.820, 0.787, 0.758, 0.732, 0.708, 0.687,
                 0.667, 0.649, 0.632, 0.617, 0.603, 0.590, 0.578, 0.566, 0.555,
                 0.545, 0.536, 0.527, 0.519, 0.511, 0.504, 0.497, 0.490, 0.483,
                 0.477, 0.469, 0.461, 0.454, 0.447, 0.440, 0.433, 0.427, 0.420,
                 0.412, 0.405, 0.399, 0.392, 0.386, 0.379, 0.373, 0.368, 0.362,
                 0.357, 0.352, 0.347, 0.342, 0.337, 0.332, 0.328, 0.324, 0.322,
                 0.319, 0.315, 0.312]
}
df_konversi = pd.DataFrame(data_konversi)

def get_konversi(jarak_input):
    return float(df_konversi.set_index("jarak").interpolate(method="linear").loc[jarak_input]["konversi"])

# Target produktivitas loader berdasarkan EGI unit
target_loader_map = {
    "EX1765": 950,  # PC2000-11R
    "EX1862": 950,
    "EX1836": 800,  # PC2000-8
    "EX1791": 800,
    "EX1250": 525,  # PC1250 Series
    "EX1284": 525,
    "EX1266": 525,
    "EX1280": 525,
    "EX1262": 525,
    "EX1260": 525,
    "EX1283": 525,
    "EX1183": 525,
    "EX1313": 525,
    "EX1185": 525,
    "EX1171": 525,
}

# Judul Aplikasi
st.title("Fleet Performance Calculator")

# Form Input
with st.form("input_form"):
    st.markdown("### Masukkan Parameter")
    unit_loader = st.selectbox(
        "Pilih Unit Loader:",
        ("EX1765", "EX1250", "EX1284", "EX1183", "EX1862",
         "EX1791", "EX1266", "EX1280", "EX1313", "EX1262", 
         "EX1260", "EX1185", "EX1836", "EX1283", "EX1171"))
    jumlah_hd = st.number_input("Jumlah HD785 (unit):", min_value=0.0, value=0.0, step=1.0, format="%.2f")
    cycle_time_pc = st.number_input("Cycle Time Loader (detik):", min_value=0.0, value=0.0, step=0.1)
    loading_time_pc = st.number_input("Loading Time Loader (menit):", min_value=0.0, value=0.0, step=0.1)
    jumlah_passing = st.number_input("Jumlah Passing Loader:", min_value=0.0, value=0.0, step=1.0)
    cycle_time_hd = st.number_input("Cycle Time HD (menit):", min_value=0.0, value=0.0, step=0.1)
    jarak = st.number_input("Jarak Front ke Disposal (KM):", min_value=0.0, value=0.0, step=0.1)
    submit = st.form_submit_button("Hitung")

if submit:
    if all([jumlah_hd > 0, cycle_time_pc > 0, loading_time_pc > 0, jumlah_passing > 0, cycle_time_hd > 0, jarak > 0]):
        unit_productivity_map = {
            "EX1862": 13,
            "EX1765": 12, "EX1836": 12, "EX1791": 12,
            "EX1250": 7, "EX1284": 7, "EX1266": 7, "EX1280": 7, "EX1262": 7, "EX1260": 7, "EX1283": 7,
            "EX1183": 6.5, "EX1313": 6.5, "EX1185": 6.5, "EX1171": 6.5,
            "EX2411": 5, "EX2363": 5
        }

        x = unit_productivity_map.get(unit_loader, 0)
        konversi_jarak = get_konversi(jarak)

        Productivity_Loader = (((x * 0.85) * (3600 * 0.8)) / cycle_time_pc) / 1.43
        Productivity_Hauler = Productivity_Loader / jumlah_hd / konversi_jarak
        Kebutuhan_HD = (cycle_time_hd * Productivity_Loader) / (60 * 60 * 0.8) + 1
        Matching_Factor = (jumlah_hd * Productivity_Hauler) / Productivity_Loader
        Ach_Ritasi = Productivity_Loader / 42

        # Ambil target produktivitas berdasarkan loader
        target_loader = target_loader_map.get(unit_loader, 0)
        target_hauler = 231  # Target HD785 konversi

        st.markdown("### Hasil Perhitungan")
        st.write(f"**Match Factor:** {Matching_Factor:.2f}")
        st.write(f"**Productivity Loader:** {Productivity_Loader:.2f} Bcm/Jam")
        st.write(f"**Productivity Hauler:** {Productivity_Hauler:.2f} Bcm/Jam")
        st.write(f"**Ritasi Should Be:** {Ach_Ritasi:.2f} Rit/Jam")

        # Notifikasi target produktivitas
        if Productivity_Loader >= target_loader:
            st.success(f"✅ Produktivitas Loader ({Productivity_Loader:.2f} Bcm/Jam) telah mencapai atau melebihi target {target_loader} Bcm/Jam.")
        else:
            st.warning(f"⚠️ Produktivitas Loader ({Productivity_Loader:.2f} Bcm/Jam) belum mencapai target {target_loader} Bcm/Jam.")

        if Productivity_Hauler >= target_hauler:
            st.success(f"✅ Produktivitas Hauler setelah konversi ({Productivity_Hauler:.2f} Bcm/Jam) telah mencapai target {target_hauler} Bcm/Jam.")
        else:
            st.warning(f"⚠️ Produktivitas Hauler setelah konversi ({Productivity_Hauler:.2f} Bcm/Jam) belum mencapai target {target_hauler} Bcm/Jam.")
        if jumlah_hd < Kebutuhan_HD:
            st.warning(f"Rekomendasi: Tambahkan **{Kebutuhan_HD - jumlah_hd:.2f} unit HD785**. Untuk mendapatkan jumlah ideal")
        elif jumlah_hd > Kebutuhan_HD + 1:
            st.warning(f"⚠️ Jumlah HD785 telah melebihi jumlah ideal **{Kebutuhan_HD:.2f} unit**. Kurangi jika memungkinkan untuk efisiensi.")
        else:
            st.success("✅ Jumlah HD785 saat ini sudah optimal.")
    else:
        st.error("Harap isi semua parameter dengan nilai lebih dari 0 untuk melakukan perhitungan.")

# Tabel Target
st.markdown("### 📌 Target Fleet Performance")
data = {
    "EGI Unit": ["PC2000-11R", "PC2000-8", "PC1250 Series", "HD785-7"],
    "Prodty (Bcm/Jam)": [950, 800, 525, 231],
    "CT Mat OB (detik)": ["27 - 30", "27 - 30", "24 - 28", "-"],
    "Loading Time (menit)": ["2,5", "2,8", "3", "-"]
}
st.table(data)
