# `templates/` README — HTML Templates for Flask Application

This folder contains the **HTML templates** used by the **Smart Manufacturing — Efficiency Prediction** Flask application. These templates define the **structure, layout, and content** of the web interface and are dynamically rendered with Flask’s **Jinja2** templating engine.

## 📁 Folder Overview

```text
templates/
└── index.html     # 🧩 Main user interface for the prediction app
```

## 🧠 `index.html` — Main Prediction Interface

### Purpose

Serves as the **front-end interface** where users can enter machine and contextual parameters to predict efficiency status. It dynamically updates based on server responses and uses Flask’s `render_template()` to inject variables such as `defaults`, `op_modes`, and `prediction`.

### Core Features

| Section              | Description                                                                  |
| -------------------- | ---------------------------------------------------------------------------- |
| **Header**           | Displays the glowing title and subtitle prompting user input.                |
| **Form (Main Card)** | Collects all relevant numeric and categorical machine parameters.            |
| **Result Panel**     | Displays prediction output (High, Medium, Low) after submission.             |
| **Footer**           | Contains project credit and the current year, passed dynamically from Flask. |

### Key Template Variables

| Variable     | Type        | Description                                                           |
| ------------ | ----------- | --------------------------------------------------------------------- |
| `features`   | `list[str]` | List of model features expected by the backend.                       |
| `defaults`   | `dict`      | Default form values (loaded from feature means or sensible defaults). |
| `op_modes`   | `list[str]` | Available operation modes for the dropdown selector.                  |
| `prediction` | `str`       | The output label returned by the trained model.                       |

### Layout Overview

1. **Header** — Large glowing title and subtitle
2. **Form Grid** — Two-column layout with labels, hints, and numeric validation
3. **Submit Button** — Gradient-styled “Predict Efficiency” call-to-action
4. **Prediction Section** — Displays the result dynamically with green accent and badge
5. **Footer** — Simple copyright and project label

### Example Code Snippet

```html
<header class="header">
  <h1 class="title">Smart Manufacturing — Efficiency Prediction</h1>
  <p class="subtitle">Enter machine and context parameters below to estimate efficiency status.</p>
</header>

<main class="card">
  <form method="post" class="form-grid">
    <div class="form-field">
      <label for="Temperature_C">Temperature (°C)</label>
      <input type="number" id="Temperature_C" name="Temperature_C"
             step="0.1" min="-20" max="200" value="{{ defaults['Temperature_C'] }}">
    </div>
    <div class="actions">
      <button type="submit">Predict Efficiency</button>
    </div>
  </form>

  {% if prediction %}
    <div class="result">
      <span class="badge">Prediction</span>
      <h2 class="prediction">{{ prediction }}</h2>
    </div>
  {% endif %}
</main>
```

### Rendering Flow

1. The Flask backend (`app.py`) calls `render_template("index.html", ...)`.
2. The Jinja engine replaces variables like `{{ defaults[...] }}` and `{{ prediction }}`.
3. User inputs are POSTed back to the same route (`"/"`), triggering model inference.
4. The template re-renders with updated results.

## 🧩 Integration with Flask

The `index.html` file is rendered from `app.py` as follows:

```python
return render_template(
    "index.html",
    prediction=prediction,
    features=FEATURES,
    defaults=form_values,
    op_modes=OPERATION_MODE_CHOICES,
)
```

Flask automatically locates templates in the `templates/` directory, so no additional path configuration is needed.

## ✅ In summary

* **`index.html`** defines the complete prediction interface for the app.
* The template dynamically displays data and results from Flask through **Jinja2** variables.
* It integrates seamlessly with assets in `static/` (CSS, images) to provide a **polished, responsive, and user-friendly** experience for the **MLOps Machine Maintenance** system.
