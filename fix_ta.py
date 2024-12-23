# -*- coding: utf-8 -*-
"""fix ta.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1dyCnHlnPvD5Md-sMqJKtNQzeceNEv1fD

**Load dataset dan import library**
"""


"""**Menangani missing values**"""

# Mengisi missing values dengan rata-rata
df['Weighted Frequency'] = df['Weighted Frequency'].fillna(df['Weighted Frequency'].mean())

"""**Scatter plot**"""

import matplotlib.pyplot as plt

plt.scatter(df['Percent'], df['Weighted Frequency'])
plt.xlabel('Percent')
plt.ylabel('Weighted Frequency')
plt.title('Scatter Plot: Percent vs Weighted Frequency')
plt.show()

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

x = df.iloc[:, [3, 4]].values

wcss = []
for i in range(1, 10):
    km = KMeans(n_clusters = i, init = 'k-means++', max_iter = 300,
                n_init = 10, random_state = 0)
    km.fit(x)
    wcss.append(km.inertia_)

fig, ax = plt.subplots(figsize=(7,4))
fig.text(0.105, .98, 'Metode Elbow', fontsize=15, fontweight='bold',
         fontfamily='serif')
fig.text(0.105, .93, 'Klaster 2D: Percent dan Weighted Frequency',
         fontsize = 12, fontweight = 'light', fontfamily = 'serif')

plt.plot(range(1, 10), wcss, '#114a31')
#plt.title('Metode Elbow', fontsize = 20)
plt.xlabel('Jumlah Klaster (K)')
plt.ylabel('wcss')
plt.show()

# kolom yang di scale
selected_cols = ['Percent', 'Weighted Frequency']

# objek scaler
scaler = StandardScaler()

# fit scaler pada kolom yang dipilih
df_scaled = scaler.fit_transform(df[selected_cols])

# 4. Clustering dengan k optimal
optimal_k = 3  # Misal hasil dari elbow method
kmeans = KMeans(n_clusters=optimal_k, random_state=42)

# gunakan scaler untuk klastering data
clusters = kmeans.fit_predict(df_scaled)

# 5. Tambahkan hasil clustering ke dataset
df['Cluster'] = clusters

# 6. Visualisasi cluster
plt.figure(figsize=(8, 6))
plt.scatter(df['Percent'], df['Weighted Frequency'], c=clusters, cmap='viridis', s=50)
plt.title('Clustering: Percent vs Weighted Frequency')
plt.xlabel('Percent')
plt.ylabel('Weighted Frequency')
plt.show()

from sklearn.metrics import silhouette_score

range_n_clusters = [3, 4, 5, 6]

for n_clusters in range_n_clusters:
    clusterer = KMeans(n_clusters = n_clusters, init = 'k-means++',
                      max_iter = 300, n_init = 10, random_state = 0)
    y_means = clusterer.fit_predict(x)
    silhouette_avg = silhouette_score(x, y_means)

    print("Jumlah klaster = ", n_clusters,
         "nilai rata-rata silhouette = ", silhouette_avg)

selected_cols = ['Percent', 'Weighted Frequency']
cluster_data = df.loc[:, selected_cols]

kmeans_sel = KMeans(n_clusters = 6, random_state = 0).fit(x)
labels = pd.DataFrame(kmeans_sel.labels_)
clustered_data = cluster_data.assign(Cluster = labels)
clustered_data

grouped_km = clustered_data.groupby(['Cluster']).mean().round(1)
grouped_km2 = clustered_data.groupby(['Cluster']).mean().round(1).reset_index()
grouped_km2['Cluster'] = grouped_km2['Cluster'].map(str)
grouped_km2

# Ganti nama kolom Cluster menjadi lebih deskriptif
df.rename(columns={"Cluster": "Prioritas Intervensi"}, inplace=True)

# Membuat peta label untuk mengganti angka klaster
priority_labels = {
    0: "Prioritas Sangat Rendah",
    1: "Prioritas Rendah",
    2: "Prioritas Sedang",
    3: "Prioritas Tinggi",
    4: "Prioritas Sangat Tinggi",
    5: "Prioritas Ekstrem",
}

# Ganti angka klaster dengan label prioritas
df["Prioritas Intervensi"].map(priority_labels)

fig, ax = plt.subplots(figsize=(12, 6))
fig.text(0.105, .98, '2D Visualisasi Klaster', fontsize=12,
         fontweight='bold', fontfamily='serif')
fig.text(0.105, .93, 'Klaster 2D: Weighted Frequency dan Percent',
         fontsize=11, fontweight='light', fontfamily='serif')

# Nama klaster sesuai dengan prioritas intervensi
priority_labels = {
    0: "Prioritas Sangat Rendah",
    1: "Prioritas Rendah",
    2: "Prioritas Sedang",
    3: "Prioritas Tinggi",
    4: "Prioritas Sangat Tinggi"
}

# Fit k-means clustering
km = KMeans(n_clusters=5, init='k-means++', max_iter=300,
            n_init=10, random_state=0)
y_means = km.fit_predict(x)

# Warna dan label klaster sesuai prioritas
colors = ['purple', 'salmon', 'teal', 'darkgreen', 'orangered']
for cluster_id in range(5):
    plt.scatter(x[y_means == cluster_id, 0], x[y_means == cluster_id, 1],
                s=100, c=colors[cluster_id], label=priority_labels[cluster_id])

# Centroid klaster
plt.scatter(km.cluster_centers_[:, 0], km.cluster_centers_[:, 1],
            s=200, c='navy', marker='*', label='Centroid')

# Label sumbu
plt.xlabel('Percent', fontfamily='serif')
plt.ylabel('Weighted Frequency', fontfamily='serif')

# Legenda dan grid
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()

# Mapping prioritas intervensi
priority_labels = {
    0: "Prioritas Sangat Rendah",
    1: "Prioritas Rendah",
    2: "Prioritas Sedang",
    3: "Prioritas Tinggi",
    4: "Prioritas Sangat Tinggi"
}

# Mengganti angka klaster dengan nama prioritas
df['Prioritas Intervensi'] = df['Prioritas Intervensi'].map(priority_labels)

# Ringkasan data berdasarkan prioritas intervensi
cluster_summary = df.groupby('Prioritas Intervensi').agg({
    'Percent': 'mean',
    'Weighted Frequency': 'mean'
})

print(cluster_summary)

import seaborn as sns
sns.boxplot(x='Prioritas Intervensi', y='Percent', data=df) # Changed 'Cluster' to 'Prioritas Intervensi'
plt.title('Distribusi Percent per Klaster')
plt.show()

cluster_demographic = df.groupby(['Prioritas Intervensi', 'Strata Name']).size()
print(cluster_demographic)

from sklearn.metrics import silhouette_score
score = silhouette_score(x, y_means)
print("Silhouette Score:", score)


# Commented out IPython magic to ensure Python compatibility.
# %%writefile app.py
# import streamlit as st
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from sklearn.cluster import KMeans
# from sklearn.preprocessing import StandardScaler
# from sklearn.metrics import silhouette_score
# 
# # Judul aplikasi
# st.title("Clustering Depresi: Visualisasi dan Insight")
# 
# # Sidebar untuk upload dataset
# st.sidebar.header("Upload Dataset")
# uploaded_file = st.sidebar.file_uploader("Unggah file CSV", type=["csv"])
# 
# if uploaded_file is not None:
#     # Membaca dataset
#     df = pd.read_csv(uploaded_file)
#     st.subheader("Data yang Diunggah")
#     st.write(df.head())
# 
#     # Menampilkan informasi awal
#     st.write("Statistik Dataset")
#     st.write(df.describe())
# 
#     # Preprocessing (mengatasi missing value)
#     if df.isnull().sum().sum() > 0:
#         st.warning("Dataset mengandung missing value. Missing value akan diimputasi dengan rata-rata.")
#         df.fillna(df.mean(), inplace=True)
# 
#     # Kolom yang akan digunakan untuk clustering
#     cols = st.sidebar.multiselect("Pilih kolom untuk clustering", df.columns, default=["Weighted Frequency", "Percent"])
# 
#     if len(cols) < 2:
#         st.warning("Pilih minimal 2 kolom untuk clustering.")
#     else:
#         # Standardisasi data
#         scaler = StandardScaler()
#         data_scaled = scaler.fit_transform(df[cols])
# 
#         # Elbow Method
#         st.subheader("Metode Elbow")
#         inertia = []
#         k_values = range(1, 11)
#         for k in k_values:
#             kmeans = KMeans(n_clusters=k, random_state=42)
#             kmeans.fit(data_scaled)
#             inertia.append(kmeans.inertia_)
# 
#         # Plot elbow method
#         fig, ax = plt.subplots()
#         ax.plot(k_values, inertia, marker="o", linestyle="--")
#         ax.set_title("Metode Elbow untuk Menentukan Jumlah Klaster")
#         ax.set_xlabel("Jumlah Klaster (k)")
#         ax.set_ylabel("Inertia")
#         st.pyplot(fig)
# 
#         # Input jumlah klaster
#         k_optimal = st.sidebar.slider("Pilih jumlah klaster", min_value=2, max_value=10, value=3)
# 
#         # K-Means Clustering
#         kmeans = KMeans(n_clusters=k_optimal, random_state=42)
#         clusters = kmeans.fit_predict(data_scaled)
# 
#         # Menambahkan kolom klaster ke dataset
#         df["Cluster"] = clusters
# 
#         # Menampilkan data dengan label klaster
#         st.subheader("Hasil Clustering")
#         st.write(df.head())
# 
#         # Visualisasi 2D Klaster
#         st.subheader("Visualisasi 2D Klaster")
#         fig, ax = plt.subplots()
#         for i in range(k_optimal):
#             cluster_data = data_scaled[clusters == i]
#             ax.scatter(cluster_data[:, 0], cluster_data[:, 1], label=f"Klaster {i}")
#         ax.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s=200, c="red", label="Centroid")
#         ax.set_title("Visualisasi Klaster")
#         ax.set_xlabel(cols[0])
#         ax.set_ylabel(cols[1])
#         ax.legend()
#         st.pyplot(fig)
# 
#         # Insight
#         st.subheader("Insight dan Rekomendasi")
#         st.write("**Insight**")
#         for i in range(k_optimal):
#             cluster_summary = df[df["Cluster"] == i][cols].mean()
#             st.write(f"Klaster {i}:")
#             st.write(cluster_summary)
# 
#         st.write("**Rekomendasi:**")
#         st.write("""
#         - Fokus pada klaster dengan persentase depresi tinggi untuk intervensi segera.
#         - Promosikan pendekatan holistik seperti mindfulness, pola makan sehat, dan aktivitas fisik di klaster dengan risiko tinggi.
#         - Lakukan edukasi khusus untuk populasi kecil dengan prevalensi tinggi untuk mencegah peningkatan risiko.
#         """)
# 
# else:
#     st.info("Silakan unggah file CSV untuk memulai analisis.")
#
