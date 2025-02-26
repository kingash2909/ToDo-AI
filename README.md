# Todo List Application

A simple and efficient Todo List web application built with Flask. This application helps users manage their daily tasks with features like adding, editing, and tracking todo items.


https://github.com/user-attachments/assets/cca8bbbf-19b2-4615-a634-a4687e9f597e



## Live link 
- https://todo-ai-ijat.onrender.com/



## Features

- Create new todo items
- Edit existing todos
- Mark todos as complete
- Delete todos
- Analytics dashboard
- User settings
- Responsive design

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:
- git clone <repository-url>
  cd todo-list-app

2. Create a virtual environment:
- bash
    python -m venv venv


3. Activate the virtual environment:
- On Windows:
  ```bash
  venv\Scripts\activate
  ```
- On macOS/Linux:
  ```bash
  source venv/bin/activate
  ```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

1. Create a `.env` file in the root directory
2. Add the following configuration:
```
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your_secret_key_here
```

## Running the Application

1. Make sure your virtual environment is activated
2. Run the Flask application:
```bash
flask run
```
3. Open your browser and navigate to `http://localhost:5000`

## Project Structure

```
todo-list-app/
├── app.py              # Main application file
├── templates/          # HTML templates
│   ├── layout.html     # Base template
│   ├── index.html      # Home page
│   ├── add.html       # Add todo page
│   ├── edit.html      # Edit todo page
│   ├── settings.html  # User settings
│   └── analytics.html # Analytics dashboard
├── static/            # Static files (CSS, JS)
├── todos.json         # Todo data storage
├── requirements.txt   # Python dependencies
└── README.md         # Project documentation
```

## Usage

1. **Adding a Todo**
   - Click on the "Add Todo" button
   - Fill in the todo details
   - Click "Save"

2. **Editing a Todo**
   - Click on the edit icon next to the todo
   - Modify the details
   - Click "Save Changes"

3. **Completing a Todo**
   - Click the checkbox next to the todo
   - The todo will be marked as complete

4. **Viewing Analytics**
   - Navigate to the Analytics page
   - View statistics about your todos

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
