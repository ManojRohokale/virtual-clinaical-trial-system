# Clinical Trial Eligibility Prediction System

A web-based application that helps determine patient eligibility for clinical trials using machine learning models. The system includes different forms for various medical conditions and provides instant eligibility predictions.

## Features

- **Multi-User Authentication**: Separate dashboards for patients and administrators
- **Condition-Specific Forms**: Dedicated forms for different medical conditions (General, Rheumatoid Arthritis, Hypertension)
- **Machine Learning Integration**: Pre-trained models for eligibility prediction
- **Database Management**: MySQL database for storing user information and form submissions
- **Responsive Design**: User-friendly interface accessible on various devices

## Prerequisites

- Python 3.7+
- MySQL Server
- pip (Python package manager)
- Virtual Environment (recommended)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd clinical-trial-app1
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**
   - Create a MySQL database named `clinical_trial`
   - Update the database credentials in `app.py` if necessary
   - The application will create the required tables on first run

5. **Download the pre-trained models**
   - Place the following model files in the project root directory:
     - `general_model.pkl`
     - `Rheumatoid_Arthritis_model.pkl`
     - `Hypertension.pkl`

## Running the Application

1. **Start the Flask development server**
   ```bash
   python app.py
   ```

2. **Access the application**
   Open a web browser and navigate to `http://localhost:5000`

## Usage

### For Patients
1. Register for an account or log in if you already have one
2. Access your dashboard
3. Fill out the appropriate medical form
4. View your eligibility results

### For Administrators
1. Log in with admin credentials
2. Access the admin dashboard
3. Review patient submissions
4. Manage clinical trial eligibility criteria

## Project Structure

```
clinical-trial-app1/
├── data/                    # Data files
├── static/                  # Static files (CSS, JavaScript)
│   ├── script.js
│   └── style.css
├── templates/               # HTML templates
│   ├── admin_dashboard.html
│   ├── general_result.html
│   ├── hypertension_form.html
│   ├── index.html
│   └── ...
├── venv/                   # Virtual environment
├── .gitignore
├── app.py                  # Main application file
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Dependencies

- Flask
- scikit-learn
- joblib
- numpy
- pandas
- mysql-connector-python
- Flask-Bcrypt

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, please open an issue in the GitHub repository or contact the project maintainers.

## Acknowledgments

- The development team
- Open-source contributors
- Medical professionals who provided domain expertise
