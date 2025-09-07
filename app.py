# app.py (Final Corrected Version)

from flask import Flask, render_template, request, redirect, session, url_for, flash
import joblib
import numpy as np
import pandas as pd  # <-- STEP 1: Import pandas
import mysql.connector
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = "averysecretkeyforflashing"
bcrypt = Bcrypt(app)

# --- MODEL LOADING ---
try:
    general_model = joblib.load("general_model.pkl")
    ra_model = joblib.load("Rheumatoid_Arthritis_model.pkl")
    hypertension_model = joblib.load("Hypertension.pkl")
except FileNotFoundError:
    print("Error: One or more model files not found!")
    general_model, ra_model, hypertension_model = None, None, None

# --- DATABASE CONNECTION ---
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Manoj#3401", # Your password
    database="clinical_trial"
)
cursor = db.cursor(dictionary=True)

# --- GENERAL & AUTH ROUTES ---
@app.route('/')
def home():
    return render_template("index.html")

# In app.py, replace your old register function with this one

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        # 1. Check if user already exists
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        existing_user = cursor.fetchone()

        # 2. If user exists, show an error
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
            return redirect(url_for('register'))

        # 3. If username is available, proceed with registration
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                       (username, hashed_password, role))
        db.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template("register.html")

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()
        if user and bcrypt.check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['role'] = user['role']
            session['username'] = user['username']
            if user['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('patient_dashboard'))
        else:
            flash('Login failed. Please check your credentials.', 'danger')
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# --- PATIENT WORKFLOW ---
@app.route('/patient_dashboard')
def patient_dashboard():
    if 'role' not in session or session['role'] != 'patient':
        return redirect(url_for('login'))
    return render_template("patient_dashboard.html")

@app.route('/general_form', methods=['GET','POST'])
def general_form():
    if 'role' not in session or session['role'] != 'patient':
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Collect data for saving to the database
        data_tuple = (
            session['user_id'],
            request.form['Age'], request.form['Sex'], request.form['Weight_kg'],
            request.form['Height_cm'], request.form['BMI'], request.form['Cohort'],
            request.form['ALT'], request.form['Creatinine'], request.form['SBP'],
            request.form['DBP'], request.form['HR'], request.form['Temp_C'],
            request.form['AdverseEvent']
        )
        cursor.execute("""
            INSERT INTO patient_forms 
            (user_id, Age, Sex, Weight_kg, Height_cm, BMI, Cohort, ALT, Creatinine, SBP, DBP, HR, Temp_C, AdverseEvent) 
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, data_tuple)
        db.commit()
        patient_form_id = cursor.lastrowid

        # FIX: Create a DataFrame for the prediction
        input_data_general = {
            'Age': [float(request.form['Age'])], 'Sex': [float(request.form['Sex'])],
            'Weight_kg': [float(request.form['Weight_kg'])], 'Height_cm': [float(request.form['Height_cm'])],
            'BMI': [float(request.form['BMI'])], 'Cohort': [float(request.form['Cohort'])],
            'ALT': [float(request.form['ALT'])], 'Creatinine': [float(request.form['Creatinine'])],
            'SBP': [float(request.form['SBP'])], 'DBP': [float(request.form['DBP'])],
            'HR': [float(request.form['HR'])], 'Temp_C': [float(request.form['Temp_C'])],
            'AdverseEvent': [float(request.form['AdverseEvent'])]
        }
        input_df_general = pd.DataFrame(input_data_general)
        
        prediction = general_model.predict(input_df_general)[0]
        result = "Accepted" if prediction == 1 else "Rejected"
        
        cursor.execute("UPDATE patient_forms SET eligibility=%s WHERE id=%s", (result, patient_form_id))
        db.commit()

        return redirect(url_for('general_eligibility_result', result=result, form_id=patient_form_id))
        
    return render_template("patient_form.html")

@app.route('/general_eligibility_result')
def general_eligibility_result():
    if 'role' not in session or session['role'] != 'patient':
        return redirect(url_for('login'))
    
    result = request.args.get('result')
    form_id = request.args.get('form_id')
    return render_template("general_result.html", result=result, form_id=form_id)

@app.route('/ra_form/<int:form_id>', methods=['GET', 'POST'])
def ra_form(form_id):
    if 'role' not in session or session['role'] != 'patient':
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Collect data from the CORRECTED form
        data_tuple = (
            session['user_id'],
            form_id,
            request.form['Age'],
            request.form['Years_Since_Diagnosis'],
            request.form['Tender_Joint_Count'],
            request.form['Swollen_Joint_Count'],
            request.form['CRP_Level'],
            request.form['Patient_Pain_Score'],
            request.form['eGFR'],
            request.form['On_Biologic_DMARDs'],
            request.form['Has_Hepatitis']
        )
        
        # Insert data into the CORRECTED table
        cursor.execute("""
            INSERT INTO rheumatoid_arthritis_forms (user_id, patient_form_id, Age, Years_Since_Diagnosis, 
            Tender_Joint_Count, Swollen_Joint_Count, CRP_Level, Patient_Pain_Score, eGFR, 
            On_Biologic_DMARDs, Has_Hepatitis)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, data_tuple)
        db.commit()
        flash('Rheumatoid Arthritis trial application submitted!', 'success')
        return redirect(url_for('patient_dashboard'))
        
    return render_template("ra_form.html", form_id=form_id)

@app.route('/hypertension_form/<int:form_id>', methods=['GET', 'POST'])
def hypertension_form(form_id):
    if 'role' not in session or session['role'] != 'patient':
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        data_tuple = (
            session['user_id'],
            form_id,
            request.form['Age'],
            request.form['Gender'],
            request.form['BMI'],
            request.form['Glucose'],
            request.form['Lifestyle_Risk'],
            request.form['Stress_Level'],
            request.form['Systolic_BP'],
            request.form['Diastolic_BP'],
            request.form['Cholesterol_Total'],
            request.form['Comorbidities'],
            request.form['Consent']
        )

        cursor.execute("""
            INSERT INTO hypertension_forms (user_id, patient_form_id, Age, Gender, BMI, Glucose, 
            Lifestyle_Risk, Stress_Level, Systolic_BP, Diastolic_BP, Cholesterol_Total, 
            Comorbidities, Consent)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, data_tuple)
        db.commit()
        flash('Hypertension trial application submitted!', 'success')
        return redirect(url_for('patient_dashboard'))
        
    return render_template("hypertension_form.html", form_id=form_id)

# --- ADMIN WORKFLOW ---
@app.route('/admin_dashboard')
def admin_dashboard():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
        
    cursor.execute("""
        SELECT u.username, ra.* FROM rheumatoid_arthritis_forms ra 
        JOIN users u ON ra.user_id = u.id 
        ORDER BY ra.submission_date DESC
    """)
    ra_patients = cursor.fetchall()
    
    cursor.execute("""
        SELECT u.username, ht.* FROM hypertension_forms ht 
        JOIN users u ON ht.user_id = u.id 
        ORDER BY ht.submission_date DESC
    """)
    hypertension_patients = cursor.fetchall()
    
    return render_template("admin_dashboard.html", ra_patients=ra_patients, hypertension_patients=hypertension_patients)

@app.route('/check_ra/<int:form_id>')
def check_ra(form_id):
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
        
    cursor.execute("SELECT * FROM rheumatoid_arthritis_forms WHERE id=%s", (form_id,))
    patient_data = cursor.fetchone()

    # Create a DataFrame with the CORRECT columns the model expects
    input_data = {
        'Age': [patient_data['Age']],
        'Years_Since_Diagnosis': [patient_data['Years_Since_Diagnosis']],
        'Tender_Joint_Count': [patient_data['Tender_Joint_Count']],
        'Swollen_Joint_Count': [patient_data['Swollen_Joint_Count']],
        'CRP_Level': [patient_data['CRP_Level']],
        'Patient_Pain_Score': [patient_data['Patient_Pain_Score']],
        'eGFR': [patient_data['eGFR']],
        'On_Biologic_DMARDs': [patient_data['On_Biologic_DMARDs']],
        'Has_Hepatitis': [patient_data['Has_Hepatitis']]
    }
    input_df = pd.DataFrame(input_data)

    prediction = ra_model.predict(input_df)[0]
    result = "Accepted" if prediction == 1 else "Rejected"

    cursor.execute("UPDATE rheumatoid_arthritis_forms SET eligibility=%s WHERE id=%s", (result, form_id))
    db.commit()

    flash(f"Patient (RA Form ID: {form_id}) has been {result}.", 'info')
    return redirect(url_for('admin_dashboard'))

@app.route('/check_hypertension/<int:form_id>')
def check_hypertension(form_id):
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
        
    cursor.execute("SELECT * FROM hypertension_forms WHERE id=%s", (form_id,))
    patient_data = cursor.fetchone()

    # FIX: Create a pandas DataFrame with the correct column names
    input_data = {
        'Age': [patient_data['Age']],
        'Gender': [patient_data['Gender']],
        'BMI': [patient_data['BMI']],
        'Glucose': [patient_data['Glucose']],
        'Lifestyle_Risk': [patient_data['Lifestyle_Risk']],
        'Stress_Level': [patient_data['Stress_Level']],
        'Systolic_BP': [patient_data['Systolic_BP']],
        'Diastolic_BP': [patient_data['Diastolic_BP']],
        'Cholesterol_Total': [patient_data['Cholesterol_Total']],
        'Comorbidities': [patient_data['Comorbidities']],
        'Consent': [patient_data['Consent']]
    }
    input_df = pd.DataFrame(input_data)

    prediction = hypertension_model.predict(input_df)[0]
    result = "Accepted" if prediction == 1 else "Rejected"

    cursor.execute("UPDATE hypertension_forms SET eligibility=%s WHERE id=%s", (result, form_id))
    db.commit()

    flash(f"Patient (Hypertension Form ID: {form_id}) has been {result}.", 'info')
    return redirect(url_for('admin_dashboard'))

if __name__ == "__main__":
    app.run(debug=True)