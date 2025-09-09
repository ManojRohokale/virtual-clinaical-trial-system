# 🏥 Clinical Trial Eligibility Prediction System

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.0.1-green.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A sophisticated web-based application that streamlines the clinical trial screening process using machine learning. This system efficiently evaluates patient eligibility across multiple medical conditions, providing instant predictions to accelerate clinical research workflows.

## 🚀 Demo

[Live Demo](#) • [Video Walkthrough](#)

## ✨ Key Features

- **Multi-Role Authentication System**
  - Secure login for both patients and administrators
  - Role-based access control
  - Session management and security

- **Intelligent Form System**
  - Dynamic form generation for different medical conditions
  - Real-time validation and error handling
  - Progress tracking for multi-step forms

- **Machine Learning Integration**
  - Pre-trained models for various medical conditions
  - Real-time eligibility prediction
  - Confidence scoring for predictions

- **Admin Dashboard**
  - Comprehensive patient data management
  - Analytics and reporting tools
  - User management interface

- **Responsive Design**
  - Mobile-friendly interface
  - Accessible design principles
  - Cross-browser compatibility

## 🛠️ Tech Stack

- **Backend**: Python, Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: MySQL
- **Machine Learning**: scikit-learn, joblib
- **Authentication**: Flask-Bcrypt
- **Deployment**: (Add your deployment method here, e.g., Heroku, AWS, etc.)

## 🏗️ Project Structure

```
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── data/                  # Data files and ML models
├── static/                # Static assets
│   ├── css/
│   └── js/
└── templates/             # HTML templates
    ├── admin/             # Admin-specific templates
    └── patient/           # Patient-specific templates
```

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- MySQL Server 8.0+
- pip (Python package manager)
- Git

### 🛠 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ManojRohokale/clinical-trial-app1.git
   cd clinical-trial-app1
   ```

2. **Set up virtual environment**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure database**
   - Install MySQL if not already installed
   - Create a new database:
     ```sql
     CREATE DATABASE clinical_trial;
     ```
   - Update database credentials in `app.py`

5. **Initialize the database**
   ```bash
   # The application will create necessary tables on first run
   python app.py
   ```

## 🖥️ Running the Application

1. **Start the development server**
   ```bash
   # Make sure your virtual environment is activated
   python app.py
   ```

2. **Access the application**
   - Open your browser and go to: `http://localhost:5000`
   - Default admin credentials (change after first login):
     - Username: admin@example.com
     - Password: admin123

## 📱 Usage

### Patient Flow
1. Register a new account or log in
2. Access personalized dashboard
3. Complete the appropriate medical form
4. Receive instant eligibility results
5. View submission history

### Admin Features
- Monitor all patient submissions
- Manage clinical trial criteria
- Generate reports and analytics
- User management
- System configuration

## 🧪 Testing

Run the test suite with:
```bash
python -m pytest tests/
```

## 🤝 Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request






