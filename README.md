# 🧩 Rubix – AI-Powered Rubik’s Cube Solver

An intelligent Rubik’s Cube Solver built using **Python**, **OpenCV**, and the **Kociemba solving algorithm**. The project scans a real Rubik’s Cube using a webcam, detects cube colors in real time, validates the cube state, and generates an optimal solving sequence.

---

# 🚀 Features

* 🎥 Real-time Rubik’s Cube scanning using webcam
* 🎨 Automatic color detection with OpenCV
* 🧠 Cube state validation before solving
* ⚡ Fast solving using Kociemba Algorithm
* 🖥 Interactive step-by-step move display
* 📦 Modular project structure for easy extension
* 🔧 YAML-based configuration support

---

# 🛠 Tech Stack

* **Python**
* **OpenCV**
* **NumPy**
* **PyYAML**
* **Matplotlib**
* **Kociemba Solver Logic**

---

# 📂 Project Structure

```bash
rubix/
│
├── backend/              # Backend APIs and solver logic
├── scanner/              # Camera + cube face scanning modules
├── solver/               # Kociemba solving implementation
├── cube/                 # Cube modeling and validation
├── ui/                   # Solution display and overlays
├── utils/                # Helper utilities
├── config/               # YAML configuration files
├── frontend/             # Frontend assets (if applicable)
├── run.py                # Main entry point
└── requirements.txt      # Python dependencies
```

---

# ⚙️ Installation

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/rubix.git
cd rubix
```

## 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Mac/Linux

```bash
source venv/bin/activate
```

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Running the Project

```bash
python run.py
```

---

# 📸 How It Works

1. Launch the application.
2. The webcam opens for cube scanning.
3. Scan all 6 faces in the required order:

```text
F → R → B → L → U → D
```

4. Press `SPACE` to capture each face.
5. The system validates the cube configuration.
6. The solver generates optimized solving moves.
7. Follow the displayed instructions to solve the cube.

---

# 🧠 Core Workflow

```text
Webcam Input
      ↓
Face Detection
      ↓
Color Recognition
      ↓
Cube State Generation
      ↓
Validation
      ↓
Kociemba Solver
      ↓
Solution Visualization
```

---

# 📦 Requirements

Install all required dependencies:

```bash
pip install -r requirements.txt
```

Main libraries used:

* opencv-python
* numpy
* pyyaml
* imutils
* matplotlib

---

# 💡 Future Improvements

* 🌐 Web-based interface
* 📱 Mobile support
* 🤖 AI-assisted cube recognition improvements
* 🎙 Voice-guided solving instructions
* 📊 Solve-time analytics
* 🧩 3D cube visualization

---

# 🤝 Contributing

Contributions, ideas, and improvements are welcome.

```bash
Fork the repository
Create a new branch
Commit your changes
Open a Pull Request
```

---

