# Jaya Jaya Maju – Employee Attrition Analysis

## Project Overview
PT Jaya Jaya Maju, perusahaan multinasional yang berdiri sejak tahun 2000, memiliki lebih dari 1000 karyawan di seluruh Indonesia. Namun, perusahaan menghadapi masalah tingginya tingkat attrition (rasio karyawan keluar) yang mencapai lebih dari 10%. Hal ini mengindikasikan adanya masalah dalam pengelolaan sumber daya manusia yang perlu segera diatasi.

## Business Understanding
- **Problem**: Tingginya attrition rate (>10%) mengindikasikan banyak karyawan keluar, yang berpotensi meningkatkan biaya rekrutmen, menurunkan produktivitas, dan mengganggu stabilitas organisasi. Perusahaan belum memahami faktor utama yang mendorong keputusan karyawan untuk resign.
- **Objective**: 
- Mengidentifikasi karakteristik karyawan yang berisiko tinggi keluar (demografi, jabatan, kepuasan kerja, dll).
- Menganalisis faktor-faktor yang berpengaruh terhadap attrition.
- Menyediakan dashboard interaktif untuk memantau indikator utama attrition.
- Mengembangkan model prediksi untuk mengidentifikasi potensi attrition lebih awal.

- **Success Criteria**: 
- Dashboard interaktif, informatif, dan mudah digunakan oleh tim HR.
- Insight dan rekomendasi yang actionable untuk menekan attrition.
- Model prediksi dengan akurasi minimal ≥80%

## Data Understanding
- **Source**: [Dicoding Dataset](https://github.com/dicodingacademy/dicoding_dataset/blob/main/employee/employee_data.csv)
- **Shape**: 1,470 rows, 35 columns (after cleaning)
- **Target**: `Attrition` (Yes/No)
- **Attrition Rate**: ~12% (dari 1058 data non-null)

## Data Preparation
- Removed irrelevant columns: `EmployeeCount`, `Over18`, `StandardHours`.
- Encoded categorical features using `LabelEncoder`.
- Split data into training (80%) and testing (20%) sets.

## Modeling & Evaluation
- **Algorithm**: Random Forest Classifier (HyperParameter Tuning).
- **Performance**: Accuracy: 85%
- **Top Features**:
  1. Monthly Income
  2. Age
  3. Overtime
  4. Monthly Rate
  5. Daily Rate

## Business Dashboard (Looker Studio)
A dashboard was created in Looker Studio to monitor attrition trends and key factors. It includes:
- Attrition rate over time (if date available) or overall summary.
- Breakdown by department, job role, overtime, and monthly income.
- Filters for managers to drill down into specific segments.

**Dashboard Access**: [dicoding-dt-hr-attrition-rate-evpt5vdvqkkd6qzxpnie5g
.streamlit.app]  

## Action Items (Recommendations)
1. **Monthly Income**: Lakukan benchmarking gaji; sesuaikan untuk posisi yang dibayar di bawah standar; buat jalur karier yang transparan.
2. **Age**: Terapkan program retensi berdasarkan segmen usia (pengembangan karier untuk karyawan muda, work-life balance untuk usia menengah, program pra-pensiun untuk karyawan senior)
3. **Overtime**: Kurangi lembur berlebihan dengan menambah staf; terapkan kebijakan keseimbangan kerja dan kehidupan.
4. **Monthly Rate**: Tinjau struktur kompensasi variabel; pastikan kompetitif; kaitkan dengan target kinerja yang realistis.
5. **Daily Rate**: Evaluasi kesetaraan upah per jam; sesuaikan untuk posisi dengan tingkat attrition tinggi.

## Deployment Notes
- The model (`model_employee.pkl`) and label encoders (`label_encoders_employee.pkl`) are included in the `model/` folder.
- A simple prediction script (`prediction.py`) is provided to score new employee data.
- to use prediction.py 
	- (optional but recommended) create venv by run this command python -m venv venv 
	- Run venv\Scripts\activate atau source venv/bin/Activate
	- then pip install -r requirements.txt
	- then python prediction.py employee_data.csv --output predictions.csv