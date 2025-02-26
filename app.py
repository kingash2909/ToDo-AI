from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import json
import os
import openai
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'ai_todo_secret_key'  # Required for flashing messages

# Configure OpenAI API - in production, use environment variables
openai.api_key = "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"  # Replace with your actual API key

# File to store todos
TODO_FILE = 'todos.json'

def load_todos():
    """Load todos from JSON file"""
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, 'r') as f:
            return json.load(f)
    return []

def save_todos(todos):
    """Save todos to JSON file"""
    with open(TODO_FILE, 'w') as f:
        json.dump(todos, f, indent=2)

def generate_ai_suggestions(task_description):
    """Generate AI suggestions for task prioritization and scheduling"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI assistant that helps prioritize and schedule tasks."},
                {"role": "user", "content": f"Based on this task: '{task_description}', suggest a priority level (High, Medium, Low) and a reasonable deadline. Respond with ONLY a JSON object with 'priority' and 'suggested_deadline' fields."}
            ],
            temperature=0.7,
            max_tokens=150
        )
        
        # Extract the AI response and parse the JSON
        ai_response = response.choices[0].message.content.strip()
        try:
            suggestion = json.loads(ai_response)
            return suggestion
        except json.JSONDecodeError:
            # Fallback if AI doesn't return valid JSON
            return {"priority": "Medium", "suggested_deadline": datetime.now().strftime("%Y-%m-%d")}
            
    except Exception as e:
        print(f"Error generating AI suggestions: {e}")
        return {"priority": "Medium", "suggested_deadline": datetime.now().strftime("%Y-%m-%d")}

@app.route('/')
def index():
    """Home page - display all todos"""
    todos = load_todos()
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['GET', 'POST'])
def add_todo():
    """Add a new todo"""
    if request.method == 'POST':
        task = request.form.get('task', '').strip()
        
        if not task:
            flash('Task cannot be empty!')
            return redirect(url_for('add_todo'))
        
        # Generate AI suggestions
        suggestions = generate_ai_suggestions(task)
        
        new_todo = {
            'id': len(load_todos()) + 1,
            'task': task,
            'priority': suggestions.get('priority', 'Medium'),
            'deadline': suggestions.get('suggested_deadline', datetime.now().strftime("%Y-%m-%d")),
            'completed': False,
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        todos = load_todos()
        todos.append(new_todo)
        save_todos(todos)
        
        flash('Todo added successfully with AI suggestions!')
        return redirect(url_for('index'))
    
    return render_template('add.html')

@app.route('/edit/<int:todo_id>', methods=['GET', 'POST'])
def edit_todo(todo_id):
    """Edit an existing todo"""
    todos = load_todos()
    todo = next((t for t in todos if t['id'] == todo_id), None)
    
    if not todo:
        flash('Todo not found!')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        task = request.form.get('task', '').strip()
        priority = request.form.get('priority')
        deadline = request.form.get('deadline')
        
        if not task:
            flash('Task cannot be empty!')
            return redirect(url_for('edit_todo', todo_id=todo_id))
        
        todo['task'] = task
        todo['priority'] = priority
        todo['deadline'] = deadline
        save_todos(todos)
        
        flash('Todo updated successfully!')
        return redirect(url_for('index'))
    
    return render_template('edit.html', todo=todo)

@app.route('/complete/<int:todo_id>')
def complete_todo(todo_id):
    """Mark a todo as completed"""
    todos = load_todos()
    todo = next((t for t in todos if t['id'] == todo_id), None)
    
    if todo:
        todo['completed'] = not todo['completed']  # Toggle completed status
        save_todos(todos)
        flash('Todo status updated!')
    else:
        flash('Todo not found!')
    
    return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>')
def delete_todo(todo_id):
    """Delete a todo"""
    todos = load_todos()
    todos = [t for t in todos if t['id'] != todo_id]
    save_todos(todos)
    flash('Todo deleted successfully!')
    return redirect(url_for('index'))

@app.route('/analyze')
def analyze_todos():
    """Analyze todos and provide insights"""
    todos = load_todos()
    
    # Simple analytics
    total_todos = len(todos)
    completed_todos = sum(1 for t in todos if t['completed'])
    completion_rate = (completed_todos / total_todos * 100) if total_todos > 0 else 0
    
    high_priority = sum(1 for t in todos if t['priority'] == 'High' and not t['completed'])
    overdue_todos = []  # We would calculate overdue todos here
    
    return render_template('analytics.html', 
                          total=total_todos,
                          completed=completed_todos,
                          completion_rate=completion_rate,
                          high_priority=high_priority,
                          overdue=overdue_todos)

@app.route('/ai/reanalyze/<int:todo_id>')
def reanalyze_todo(todo_id):
    """Re-analyze a task with AI to update suggestions"""
    todos = load_todos()
    todo = next((t for t in todos if t['id'] == todo_id), None)
    
    if not todo:
        return jsonify({"error": "Todo not found"}), 404
    
    # Generate new AI suggestions
    suggestions = generate_ai_suggestions(todo['task'])
    
    # Update todo with new suggestions
    todo['priority'] = suggestions.get('priority', todo['priority'])
    todo['deadline'] = suggestions.get('suggested_deadline', todo['deadline'])
    save_todos(todos)
    
    return jsonify({"success": True, "todo": todo})

if __name__ == '__main__':
    app.run(debug=True)