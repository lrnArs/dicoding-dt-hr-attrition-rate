# Proyek Akhir: Menyelesaikan Permasalahan Human Resources

## Business Understanding
PT Jaya Jaya Maju, perusahaan multinasional yang berdiri sejak tahun 2000, memiliki lebih dari 1000 karyawan di seluruh Indonesia. Namun, perusahaan menghadapi masalah tingginya tingkat attrition (rasio karyawan keluar) yang mencapai lebih dari 10%. Hal ini mengindikasikan adanya masalah dalam pengelolaan sumber daya manusia yang perlu segera diatasi.

## Permasalahan Bisnis
1. Tingginya attrition rate (>10%) mengindikasikan banyak karyawan keluar, yang berpotensi meningkatkan biaya rekrutmen, menurunkan produktivitas, dan mengganggu stabilitas organisasi.
2. Tidak adanya sistem monitoring yang terintegrasi untuk memantau faktor-faktor yang memengaruhi keputusan karyawan untuk keluar.
3. Kurangnya model prediktif yang dapat membantu HR mengidentifikasi karyawan yang berpotensi keluar sehingga tindakan preventif dapat dilakukan.


## Cakupan Proyek 
Proyek ini bertujuan untuk:
1. **Mengidentifikasi faktor-faktor dominan** yang memengaruhi *attrition* menggunakan analisis eksploratif dan *feature importance* dari model machine learning.
2. **Membangun model prediksi** *attrition* berbasis Random Forest yang dapat membantu HR memproyeksikan karyawan mana yang berisiko tinggi keluar.
3. **Membuat business dashboard** interaktif dengan Looker Studio untuk memonitor metrik *attrition* secara real-time, dilengkapi filter departemen, jabatan, dan faktor lainnya.

## Persiapan
**Source**: [Dicoding Dataset](https://github.com/dicodingacademy/dicoding_dataset/blob/main/employee/employee_data.csv)


Proyek ini dikerjakan menggunakan Google Colaboratory untuk notebook Run

Setup environment:

Buat virtual Environment python
```
create venv by run this command python -m venv venv 
```
Aktivasi Virtual Env
```
Run venv\Scripts\activate atau source venv/bin/Activate
```
Install Depedencies yang dibutuhkan
```
then pip install -r requirements.txt
```

### Deployment Notes
- The model (`model_employee.pkl`) and label encoders (`label_encoders_employee.pkl`) are included in the `model/` folder.
- A simple prediction script (`prediction.py`) is provided to score new employee data.

### How to to use/ Cara Pakai  prediction.py 
```
python prediction.py employee_data.csv --output predictions.csv
```



### Modeling & Evaluation
- **Algorithm**: Random Forest Classifier (HyperParameter Tuning).
- **Performance**: Accuracy: 85%
- **Top Features**:
  1. Monthly Income
  2. Age
  3. Overtime
  4. Monthly Rate
  5. Daily Rate

## Business Dashboard (Streamlit)
A dashboard was created in Streamlit to monitor attrition trends and key factors. It includes:

- Overall Attrition Summary: Displays the total attrition rate, offering a quick snapshot of workforce retention.
- Attrition Breakdown: Analyzes attrition across key dimensions such as Department, Overtime, and Gender, helping identify high-risk groups.
- Attrition Prediction: Estimates the probability of employee attrition based on survey responses and satisfaction scores, enabling proactive intervention.
- Interactive Filters: Allows managers to drill down into specific employee segments categorized by high, medium, and low attrition probability for targeted analysis.

**Dashboard Access**: [Dashboard Streamlit](https://dicoding-dt-hr-attrition-rate-evpt5vdvqkkd6qzxpnie5g.streamlit.app/) 

## Conclusion
Berdasarkan analisis dan pemodelan yang dilakukan, dapat disimpulkan bahwa:

- Faktor utama penyebab attrition adalah MonthlyIncome, Age, Overtime, Monthly Rate, dan Daily Rate. Karyawan memiliki pendapatan rendah dan yang sering lembur memiliki risiko attrition lebih tinggi.
- Model Random Forest yang dibangun memiliki akurasi sekitar 85% dan mampu mengidentifikasi karyawan berisiko dengan recall cukup baik pada kelas attrition, sehingga dapat digunakan sebagai alat bantu early warning.
- Dashboard interaktif memungkinkan manajemen memantau attrition secara real-time dan melakukan investigasi lebih mendalam berdasarkan segmen karyawan tertentu.

## Action Items (Recommendations)
1. **Monthly Income**: Lakukan benchmarking gaji; sesuaikan untuk posisi yang dibayar di bawah standar; buat jalur karier yang transparan.
2. **Age**: Terapkan program retensi berdasarkan segmen usia (pengembangan karier untuk karyawan muda, work-life balance untuk usia menengah, program pra-pensiun untuk karyawan senior)
3. **Overtime**: Kurangi lembur berlebihan dengan menambah staf; terapkan kebijakan keseimbangan kerja dan kehidupan.
4. **Monthly Rate**: Tinjau struktur kompensasi variabel; pastikan kompetitif; kaitkan dengan target kinerja yang realistis.
5. **Daily Rate**: Evaluasi kesetaraan upah per jam; sesuaikan untuk posisi dengan tingkat attrition tinggi.

