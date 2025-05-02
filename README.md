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

3. Run the application:
```bash
flask run
```

4. Open your browser and navigate to:
```
http://127.0.0.1:5000/
```

### Connecting to WLED

[Getting Started - WLED](https://kno.wled.ge/basics/getting-started/)

## 4. Project Structure 

- `/app` - Main application directory
  - `/static` - CSS, JavaScript, and images
  - `/templates` - HTML templates
  - `__init__.py` - Flask application initialization
- `/docs` - Documentation files

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

## 7. Acknowledgements 

This project builds upon the amazing [WLED project](https://github.com/Aircoookie/WLED), an open-source solution for controlling many addressable and non-addressable LED strips.
