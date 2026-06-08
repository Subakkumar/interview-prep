import os
import json
from flask import Flask, render_template, request, jsonify
from models import db, Problem, Attempt
from runner import run_solution
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']        = 'sqlite:///interview_prep.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY']                     = 'interviewprepsecret'

db.init_app(app)
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

with app.app_context():
    db.create_all()

# ── Groq helper ────────────────────────────────────────
def ask_groq(prompt: str, max_tokens: int = 512) -> str:
    response = client.chat.completions.create(
        model='llama-3.3-70b-versatile',
        messages=[{'role': 'user', 'content': prompt}],
        max_tokens=max_tokens,
        temperature=0.4
    )
    return response.choices[0].message.content

# ── Routes ─────────────────────────────────────────────
@app.route('/')
def index():
    problems = Problem.query.order_by(Problem.difficulty, Problem.category).all()
    by_diff  = {'easy': [], 'medium': [], 'hard': []}
    for p in problems:
        by_diff.setdefault(p.difficulty, []).append(p)
    return render_template('index.html', problems=problems, by_diff=by_diff)

@app.route('/problem/<int:problem_id>')
def problem(problem_id):
    prob = Problem.query.get_or_404(problem_id)
    attempts = Attempt.query.filter_by(problem_id=problem_id)\
                            .order_by(Attempt.created_at.desc())\
                            .limit(5).all()
    return render_template('problem.html', problem=prob, attempts=attempts)

@app.route('/api/hint', methods=['POST'])
def get_hint():
    data         = request.get_json() or {}
    problem_id   = data.get('problem_id')
    attempt_num  = int(data.get('attempt_num', 0))

    prob = Problem.query.get(problem_id)
    if not prob:
        return jsonify({'error': 'Problem not found'}), 404

    if attempt_num == 0:
        level   = 'very gentle — one sentence, no code, just a nudge'
    elif attempt_num == 1:
        level   = 'mention the key data structure or algorithm family without giving away the solution'
    else:
        level   = 'explain the algorithm approach clearly with pseudocode only, no actual implementation'

    prompt = f"""You are a coding mentor helping a student solve this problem.

Problem: {prob.title}
{prob.description}

Give a hint at this level: {level}

Do NOT give the full solution. Be encouraging and concise."""

    hint = ask_groq(prompt, 256)
    return jsonify({'hint': hint, 'level': attempt_num})

@app.route('/api/run', methods=['POST'])
def run_code():
    data       = request.get_json() or {}
    problem_id = data.get('problem_id')
    code       = data.get('code', '')

    prob = Problem.query.get(problem_id)
    if not prob:
        return jsonify({'error': 'Problem not found'}), 404

    test_cases = json.loads(prob.test_cases) if prob.test_cases else []
    results    = run_solution(code, prob.title, test_cases)
    passed_all = all(r['passed'] for r in results)
    pass_count = sum(1 for r in results if r['passed'])

    return jsonify({
        'results':    results,
        'passed_all': passed_all,
        'pass_count': pass_count,
        'total':      len(results)
    })

@app.route('/api/evaluate', methods=['POST'])
def evaluate():
    data       = request.get_json() or {}
    problem_id = data.get('problem_id')
    code       = data.get('code', '')
    hints_used = int(data.get('hints_used', 0))

    prob = Problem.query.get(problem_id)
    if not prob:
        return jsonify({'error': 'Problem not found'}), 404

    # Run tests first
    test_cases = json.loads(prob.test_cases) if prob.test_cases else []
    results    = run_solution(code, prob.title, test_cases)
    passed_all = all(r['passed'] for r in results)
    pass_count = sum(1 for r in results if r['passed'])
    total      = len(results)

    test_summary = f'{pass_count}/{total} test cases passed'

    # Groq feedback
    prompt = f"""You are a senior software engineer reviewing a coding solution.

Problem: {prob.title} ({prob.difficulty})
{prob.description}

Student's Solution:
```python
{code}
```

Test Results: {test_summary}
Hints used: {hints_used}

Provide:
1. **Correctness** — does it solve the problem correctly?
2. **Time Complexity** — Big O analysis
3. **Space Complexity** — Big O analysis
4. **One improvement** — the most important thing to change
5. **Score** — rate the solution 0-100

Format the Score as: Score: XX/100
Be constructive and specific."""

    feedback = ask_groq(prompt, 600)

    # Parse score from feedback
    score = 0
    for line in feedback.split('\n'):
        if 'Score:' in line or 'score:' in line:
            import re
            nums = re.findall(r'\d+', line)
            if nums:
                score = min(int(nums[0]), 100)
                break
    if score == 0:
        score = int((pass_count / total * 70) + (30 if hints_used == 0 else 15)) if total else 50

    # Save attempt
    attempt = Attempt(
        problem_id = problem_id,
        code       = code,
        passed     = passed_all,
        score      = score,
        feedback   = feedback,
        hints_used = hints_used
    )
    db.session.add(attempt)
    db.session.commit()

    return jsonify({
        'passed':     passed_all,
        'pass_count': pass_count,
        'total':      total,
        'score':      score,
        'feedback':   feedback,
        'attempt_id': attempt.id
    })

@app.route('/api/problems')
def list_problems():
    diff     = request.args.get('difficulty')
    category = request.args.get('category')
    q        = Problem.query
    if diff:     q = q.filter_by(difficulty=diff)
    if category: q = q.filter_by(category=category)
    return jsonify([p.to_dict() for p in q.all()])

if __name__ == '__main__':
    app.run(debug=True, port=5009)