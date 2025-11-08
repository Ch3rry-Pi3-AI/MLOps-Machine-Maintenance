# 🌐 **Flask Web Application — MLOps Machine Maintenance**

This branch advances the **MLOps Machine Maintenance** project by introducing a **Flask-based web interface** for real-time machine efficiency prediction. It represents the **fourth major stage** of the project, transitioning from backend model training to a fully interactive **frontend deployment**.

The Flask app integrates all artefacts produced in previous stages — **scaler**, **trained model**, and **preprocessed defaults** — and serves them through a clean, user-friendly web UI.

<p align="center">
  <img src="img/flask/flask_app.png" alt="Deployed Flask Machine Efficiency Prediction App" style="width:100%; height:auto;" />
</p>

## 🧩 **Overview**

The Flask application allows users to input **machine and contextual parameters** (e.g. temperature, vibration, power consumption, network latency) and instantly receive a **predicted efficiency status** from the trained model.

It consists of three main components:

1️⃣ **`app.py`** — Flask backend handling user requests, prediction logic, and result rendering
2️⃣ **`templates/index.html`** — Jinja2-based HTML template for the main web interface
3️⃣ **`static/`** — Styling and design assets, including CSS and background images

Together, they deliver an end-to-end web solution for **predictive maintenance inference**.

## 🔧 **Core Responsibilities**

| Component              | Operation                                                                                          | Description |
| ---------------------- | -------------------------------------------------------------------------------------------------- | ----------- |
| 🧠 **Model Inference** | Loads pre-trained model and scaler, scales inputs, and predicts machine efficiency class.          |             |
| 💻 **Web Interface**   | Accepts user input through a responsive web form and displays prediction results dynamically.      |             |
| 🎨 **Frontend Design** | Implements a modern, glowing UI with transparency, gradients, and adaptive layout for all devices. |             |

## 🗂️ **Updated Project Structure**

```text
mlops_machine_maintenance/
├── artifacts/
│   ├── raw/
│   │   └── data.csv                  # ⚙️ Raw machine sensor dataset
│   ├── processed/
│   │   ├── X_train.pkl
│   │   ├── X_test.pkl
│   │   ├── y_train.pkl
│   │   ├── y_test.pkl
│   │   ├── scaler.pkl
│   │   └── feature_means.json        # Optional: saved mean defaults for UI prefill
│   └── models/
│       └── model.pkl                 # 🧠 Trained machine efficiency model
├── pipeline/
│   └── training_pipeline.py          # 🚀 End-to-end pipeline (preprocessing → training)
├── src/
│   ├── custom_exception.py           # Unified and detailed exception handling
│   ├── logger.py                     # Centralised logging configuration
│   ├── data_processing.py            # 🧩 Data preprocessing and scaling
│   └── model_training.py             # ⚙️ Model training and evaluation
├── static/
│   ├── style.css                     # 🎨 Core application styling
│   └── img/
│       └── app_background.jpg        # 🖼️ Background image for the web app
├── templates/
│   └── index.html                    # 🧠 Flask interface for efficiency prediction
├── img/
│   └── flask/
│       └── flask_app.png             # 📸 Screenshot of the deployed Flask web app
├── app.py                            # 🌐 Flask backend for web application
├── requirements.txt                  # 📦 Python dependencies
├── pyproject.toml                    # ⚙️ Project metadata and uv configuration
├── setup.py                          # 🔧 Editable install support
└── uv.lock                           # 🔒 Locked dependency versions
```

## ⚙️ **How to Run the Flask Application**

Once the model has been trained and artefacts are available under `artifacts/processed/` and `artifacts/models/`, launch the web app using:

```bash
python app.py
```

The application will start a local development server, typically accessible at:

🔗 **[http://0.0.0.0:5000](http://0.0.0.0:5000)** or **[http://localhost:5000](http://localhost:5000)**

### ✅ **Expected Successful Output**

```console
 * Running on http://127.0.0.1:5000 (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
```

When opened in a browser, the interface will display:

* A **glowing blue title** and descriptive subtitle
* A **two-column input form** for machine and contextual parameters
* A **“Predict Efficiency”** button
* A dynamically rendered prediction result (e.g., “High Efficiency” or “Low Efficiency”)

## 🧠 **Implementation Highlights**

* **Dynamic Form Population**
  The app preloads sensible defaults (e.g., average temperature, vibration frequency, maintenance score) using `feature_means.json` if available.

* **Integrated Preprocessing**
  Automatically encodes the selected `Operation_Mode`, scales numeric inputs using the saved `StandardScaler`, and ensures strict feature ordering.

* **Human-Readable Predictions**
  Translates model output indices (0, 1, 2) into intuitive labels: `High`, `Medium`, `Low`.

* **Polished UI Design**
  Transparent glass-like card layout, glowing blue text, and responsive grid form built for clarity and usability.

* **Full Flask–Jinja2 Integration**
  Combines backend inference with dynamic HTML rendering, providing seamless feedback and state persistence.

## 🧩 **Integration Guidelines**

| File                            | Purpose                                                         |
| ------------------------------- | --------------------------------------------------------------- |
| `app.py`                        | Flask backend serving predictions using trained ML artefacts.   |
| `templates/index.html`          | Main HTML template for user interaction and prediction display. |
| `static/style.css`              | Defines the overall UI layout, styling, and glow effects.       |
| `static/img/app_background.jpg` | Visual background for the prediction interface.                 |
| `img/flask/flask_app.png`       | Image preview of the deployed web application.                  |
| `artifacts/`                    | Contains all preprocessed data, trained models, and scalers.    |

## ✅ **In Summary**

This stage transforms the **MLOps Machine Maintenance** project into a **fully interactive predictive web application**.
The Flask app integrates the trained model with a polished, responsive frontend that allows users to perform real-time efficiency predictions from any browser.

It marks the transition from **model training and automation** to **interactive deployment and inference**, laying the foundation for upcoming stages such as **Docker containerisation**, **Kubernetes hosting**, and **CI/CD-based web deployments** to cloud platforms.
