from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import pandas as pd
import os
from collections import Counter, defaultdict

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, 'career_dataset.csv')

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

df = pd.read_csv(DATASET_PATH)
df.columns = [c.strip().lower() for c in df.columns]

recommendation_cols = ['top1', 'top2', 'top3']
categorical_cols = ['subject_preference']
numeric_cols = [
    'coding_interest', 'writing_interest', 'design_interest', 'law_interest',
    'medical_interest', 'math_comfort', 'empathy', 'public_speaking',
    'problem_solving', 'creativity', 'biology_interest',
    'portfolio_preference', 'work_environment'
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

DEGREE_MAP = {
    'Software Engineer': ['B.Tech in Computer Science', 'BCA', 'B.Sc Computer Science'],
    'Web Developer': ['BCA', 'B.Tech in IT', 'B.Sc Computer Science'],
    'AI Engineer': ['B.Tech in AI/ML', 'B.Tech in CSE', 'B.Sc Data Science'],
    'Cloud Engineer': ['B.Tech in CSE', 'B.Tech in IT', 'BCA'],
    'Cybersecurity Analyst': ['B.Tech in Cyber Security', 'BCA', 'B.Tech in CSE'],
    'Data Scientist': ['B.Sc Data Science', 'B.Tech in CSE', 'B.Sc Statistics'],
    'UIUX Designer': ['B.Des in UX/UI', 'B.Des in Interaction Design', 'Bachelor of Fine Arts'],
    'Graphic Designer': ['B.Des in Graphic Design', 'BFA', 'B.Voc in Graphic Design'],
    'Product Designer': ['B.Des in Product Design', 'Bachelor of Design', 'B.Des in Industrial Design'],
    'Animator': ['B.Sc Animation', 'B.Des in Animation', 'BFA'],
    'Fashion Designer': ['B.Des in Fashion Design', 'B.Sc Fashion Design', 'Bachelor of Design'],
    'Content Writer': ['BA English', 'BA Journalism', 'BA Mass Communication'],
    'Copywriter': ['BA English', 'BA Advertising', 'BA Mass Communication'],
    'Author': ['BA English Literature', 'BA English', 'BA Journalism'],
    'Journalist': ['BJMC', 'BA Journalism', 'BA Mass Communication'],
    'Editor': ['BA English', 'BA Journalism', 'BA Mass Communication'],
    'Lawyer': ['BA LLB', 'BBA LLB', 'B.Com LLB'],
    'Judge': ['BA LLB', 'LLB', 'BBA LLB'],
    'Corporate Lawyer': ['BBA LLB', 'BA LLB', 'B.Com LLB'],
    'Legal Advisor': ['BA LLB', 'BBA LLB', 'LLB'],
    'Public Prosecutor': ['BA LLB', 'LLB', 'BA Political Science + LLB'],
    'Doctor': ['MBBS', 'BAMS', 'BHMS'],
    'Surgeon': ['MBBS', 'MBBS + MS', 'BDS'],
    'Cardiologist': ['MBBS', 'MD Medicine', 'DM Cardiology'],
    'Neurologist': ['MBBS', 'MD Medicine', 'DM Neurology'],
    'Radiologist': ['MBBS', 'MD Radiology', 'B.Sc Radiology'],
    'Dentist': ['BDS', 'Bachelor of Dental Surgery', 'BDS + specialization'],
    'Pharmacist': ['B.Pharm', 'Pharm.D', 'D.Pharm'],
    'Nurse': ['B.Sc Nursing', 'GNM', 'Post Basic B.Sc Nursing'],
    'Physiotherapist': ['BPT', 'Bachelor of Physiotherapy', 'B.Sc Rehabilitation'],
    'Psychiatrist': ['MBBS', 'MD Psychiatry', 'B.Sc Psychology'],
    'Accountant': ['B.Com', 'BBA Finance', 'Bachelor in Accounting'],
    'Business Analyst': ['BBA', 'B.Com', 'BBA Business Analytics'],
    'Marketing Manager': ['BBA Marketing', 'B.Com', 'BA Mass Communication'],
    'Manager': ['BBA', 'BMS', 'B.Com'],
    'Entrepreneur': ['BBA', 'B.Com', 'Any bachelor degree + entrepreneurship training']
}

LABELS = {
    'coding_interest': 'coding strength',
    'writing_interest': 'writing strength',
    'design_interest': 'design strength',
    'law_interest': 'law interest',
    'medical_interest': 'medical interest',
    'biology_interest': 'biology comfort',
    'math_comfort': 'math comfort',
    'empathy': 'empathy',
    'public_speaking': 'communication ability',
    'problem_solving': 'problem solving',
    'creativity': 'creativity',
    'subject_preference': 'subject preference',
    'work_environment': 'work environment preference',
    'portfolio_preference': 'portfolio preference'
}

def mode(values):
    values = [v for v in values if pd.notna(v)]
    return Counter(values).most_common(1)[0][0] if values else ''

def build_profiles(frame):
    grouped = defaultdict(list)
    for _, row in frame.iterrows():
        for col in recommendation_cols:
            career = row.get(col)
            if pd.notna(career) and str(career).strip():
                grouped[str(career).strip()].append(row)
    profiles = {}
    for career, rows in grouped.items():
        part = pd.DataFrame(rows)
        profiles[career] = {
            'career': career,
            'numeric': {col: float(pd.to_numeric(part[col], errors='coerce').fillna(0).mean()) for col in numeric_cols},
            'categorical': {col: mode(part[col].tolist()) for col in categorical_cols},
            'samples': len(part),
            'degrees': DEGREE_MAP.get(career, ['Relevant bachelor degree', 'Foundation degree in this field', 'Specialized undergraduate program'])
        }
    return profiles

profiles = build_profiles(df)

def score_profile(student, profile):
    score = 0
    matched = []
    for col in numeric_cols:
        student_val = float(student.get(col, 0) or 0)
        profile_val = float(profile['numeric'].get(col, 0) or 0)
        closeness = max(0, 10 - abs(student_val - profile_val))
        score += closeness
        if closeness >= 8:
            matched.append(col)
    for col in categorical_cols:
        if str(student.get(col, '')).strip().lower() == str(profile['categorical'].get(col, '')).strip().lower() and student.get(col):
            score += 12
            matched.append(col)
    return round(score, 2), matched[:6]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/meta')
def meta():
    return jsonify({'numeric_cols': numeric_cols, 'categorical_cols': categorical_cols, 'careers': sorted(list(profiles.keys()))})

@app.route('/api/recommend', methods=['POST'])
def recommend():
    student = request.get_json(force=True)
    for col in numeric_cols:
        student[col] = float(student.get(col, 0) or 0)
    results = []
    for career, profile in profiles.items():
        score, matched = score_profile(student, profile)
        reasons = ', '.join(LABELS.get(m, m) for m in matched[:5])
        results.append({
            'career': career,
            'score': score,
            'matched_traits': matched,
            'explanation': f"{career} is a strong match based on {reasons}." if reasons else f"{career} fits the overall profile pattern.",
            'degrees': profile['degrees'],
            'sample_size': profile['samples']
        })
    results = sorted(results, key=lambda x: x['score'], reverse=True)[:6]
    return jsonify({'recommendations': results, 'careers_considered': len(profiles)})

if __name__ == '__main__':
    app.run(debug=True)
