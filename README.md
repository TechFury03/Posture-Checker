# Posture Checker

## Install
We make use of Python, `pip` and Git in order to install Posture Checker. 
We assume this has already been setup on the system.
Posture Checker has been developed for Windows.
It might also work on Linux/macOS with some adaption, however these are out of the scope of this project.
To install Posture Checker, follow the steps below:

### 1. Clone 
First, clone the repository onto your system:
```bash
git clone https://github.com/TechFury03/Posture-Checker.git
```

### 2. Virtual Environment
Next, create a virtual environment so the dependencies do not potentionally conflict with global dependencies on your system:
```bash
python -m venv post_venv
```
Here we call our virtual environment `pc_venv`, short for Posture Checker Virtual Environment. 
Now we need to start our virtual environment:

#### Windows
```bash
pc_venv\Scripts\activate
```

#### Linux/macOS
```bash
source pc_venv/bin/activate
```

### 3. Install Dependencies
Next, install the dependencies using `pip`:
``` bash
pip install -r requirements.txt
```

### 4. Run Posture Checker
We can now start Posture Checker:
``` bash
python main.py
```

### 5. Disable venv
To shut down the virtual environment:
``` bash
deactivate
```
