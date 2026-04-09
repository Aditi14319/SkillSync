🚀 SkillSync – Career Recommendation System

SkillSync is an intelligent career recommendation web application that helps students and professionals discover suitable career paths based on their interests, skills, and preferences.

It not only suggests top career options but also recommends relevant bachelor’s degree programs, making it a complete guidance tool for academic and career planning.



🌟 Key Highlights

🎯 Personalized Career Recommendations

🎓 Bachelor Degree Suggestions for Each Career

🧠 Data-driven Recommendation Logic (CSV-based)

🎛️ Interactive Slider-Based UI for Inputs

🌐 Full Stack Web Application (Frontend + Backend)

📊 Covers diverse domains:

Technology

Law

Medical

Design

Literature

Business & more

🧩 How It Works

SkillSync collects user input across multiple dimensions:

Coding Interest

Writing Interest

Design Interest

Law Interest

Medical Interest

Math Comfort

Empathy

Public Speaking

Problem-Solving Ability

Creativity

Biology Interest

Portfolio Preference

Work Environment Preference

Subject Preference


🔍 These inputs are matched against a structured dataset (career_dataset.csv) to:


Identify the closest matching career profiles

Rank and return Top Career Recommendations

Suggest relevant undergraduate degree programs

🛠️ Tech Stack

Layer	               Technology Used

Backend	                Python, Flask

API Support	               Flask-CORS

Data Handling	            Pandas

Frontend	            HTML, CSS, JavaScript

Deployment	               Gunicorn, Render


📁 Project Structure

skillsync/

│

├── app.py                 # Main Flask application

├── requirements.txt       # Dependencies

├── career_dataset.csv     # Dataset for recommendation logic

├── README.md

│

├── templates/

│   └── index.html         # Frontend UI

│

└── static/

    ├── style.css          # Styling

    └── script.js          # Client-side logic


⚙️ Installation & Setup

1️⃣ Clone the Repository
git clone https://github.com/Aditi14319/SkillSync.git
cd SkillSync

2️⃣ Create Virtual Environment (Recommended)
python -m venv venv
venv\Scripts\activate   # For Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Run the Application
python app.py

5️⃣ Open in Browser
http://127.0.0.1:5000

📦 Requirements

Flask==3.0.3

flask-cors==4.0.1

pandas==2.2.2


🔧 Configuration

Environment: Python

Build Command:

pip install -r requirements.txt


⚠️ Important Notes

Ensure career_dataset.csv is in the root directory

Always run the Flask server before accessing the app

If facing issues installing pandas on Windows, use Conda environment

🔮 Future Enhancements

🔐 User Authentication (Login/Signup)

💾 Save User Profiles & History

📊 Advanced ML-Based Recommendation Engine

🧭 Career Roadmap Visualization

🎓 University & Course Recommendations

📱 Mobile Responsive UI Improvements

📌 Use Cases

🎓 Students choosing career paths

🔁 Professionals planning career switches

📊 Educational institutions offering guidance tools

💼 Career counseling platforms


👩‍💻 Author

Aditi Pandey

📄 License

This project is intended for academic and educational purposes.

⭐ Support

If you found this project useful:

⭐ Star the repository

🍴 Fork it

🛠️ Contribute improvements