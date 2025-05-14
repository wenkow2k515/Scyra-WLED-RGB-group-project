# Scyra-WLED-RGB-Group-Project

## 1. Introduction – What is Scyra? 

**Scyra** is a beginner-friendly extension of the open-source LED control software **WLED**.
- WLED is powerful, but its complex interface and reliance on programming knowledge make it tough for newcomers.
- Scyra solves this by offering a **visual interface**, allowing users to create custom LED presets without coding.
- These presets are converted into JSON and work seamlessly with WLED.

## 2. Features 

- **Intuitive Visual Editor**: Create LED presets with a user-friendly RGB controller
- **Login System**: Save and manage your custom presets
- **Presets Library**: Store locally or in the cloud, with upcoming community sharing
- **Real-time LED Strip Simulation**: Test your designs without hardware
- **Privacy-Focused**: Local storage by default, no mandatory account creation
- **Responsive Design**: Works across desktop and mobile devices
- **Easy Setup**: Simple connection to your WLED-compatible devices
- **AI Mood Feedback**: Receive personalized lighting recommendations based on your mood

## 3. Usage 

### Prerequisites

- Python 3.x installed
- Flask framework
- WLED-compatible LED controller (optional for simulation mode)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Scyra-WLED-RGB-group-project.git
cd Scyra-WLED-RGB-group-project
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables (copy example file and modify as needed):
```bash
cp env_example .env
```

4. Initialize the database:
```bash
flask db upgrade
```

5. Run the application:
```bash
flask run
```

6. Open your browser and navigate to:
```
http://127.0.0.1:5000/
```

### AI Mood Feedback Feature

Our app includes a mood analysis feature that can provide personalized lighting recommendations based on your emotional state. This feature works in two ways:

#### Option 1: Using OpenAI API (Enhanced Experience)

For the best experience with advanced personalized feedback:

1. Sign up for an OpenAI API key at [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Add your API key to the `.env` file:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
3. Restart the application if it's already running

The app will use GPT-3.5-turbo to generate highly personalized feedback and color recommendations based on your mood metrics and journal entries.

#### Option 2: Without API Key (Works Out of the Box)

The app works perfectly without an API key, using a built-in rule-based system:

1. Simply leave the `OPENAI_API_KEY` field blank or remove it from your `.env` file
2. The app will automatically use our rule-based system to generate good quality feedback

This option requires no setup and provides solid recommendations based on psychological color principles.

#### Testing the Mood Feature

To test both modes of the mood feedback system:
```bash
python test_mood_utils.py
```

For more details, see the full documentation in `docs/ai_feedback.md`.

### Connecting to WLED

[Getting Started - WLED](https://kno.wled.ge/basics/getting-started/)

## 4. Project Structure 

- `/app` - Main application directory
  - `/static` - CSS, JavaScript, and images
  - `/templates` - HTML templates
    - `/mood` - Mood analysis and survey templates
    - `/auth` - Authentication related templates
    - `/user` - User profile and settings templates
  - `/database` - SQLite database and related files
  - `__init__.py` - Flask application initialization
  - `models.py` - Database models and schema definitions
  - `forms.py` - Form definitions using Flask-WTF
  - `mood_routes.py` - Routes for mood analysis features
  - `mood_utils.py` - AI mood analysis utilities with OpenAI integration and fallback system
  - `color_recommendation.py` - Color recommendation algorithm based on mood data
  - `config.py` - Application configuration settings
- `/migrations` - Database migration files
  - `/versions` - Individual migration scripts including AI feedback column addition
- `/docs` - Documentation files
  - `ai_feedback.md` - Detailed information about the mood analysis feature
- `/tests` - Test files and utilities
  - `test_mood_utils.py` - Tests for the mood analysis with and without API
  - `test_without_api.py` - Specific tests for the fallback system
- `requirements.txt` - Python package dependencies
- `env_example` - Example environment variables file showing API key configuration
- `.env` - Your local environment variables (not in repository)
- `README.md` - This documentation

## 5. Our Group Members 

| UWA ID    | Name           | GitHub Username |
|-----------|----------------|----------------|
| 24168584  | Qihang Sun     | wenkow2k515    |
| 23905527  | MannoorKaur    | MannoorKaur    |
| 23625197  | Richard Lin    | SagoCs         |

## 6. Future Development 

- Community preset sharing platform
- Mobile app
- Cloud storage for your presets
- Enhanced mood analysis algorithms

## 7. Acknowledgements 

This project builds upon the amazing [WLED project](https://github.com/Aircoookie/WLED), an open-source solution for controlling many addressable and non-addressable LED strips.

We also use the OpenAI API for our AI-powered mood feedback feature, with a fallback system for users without API access.
