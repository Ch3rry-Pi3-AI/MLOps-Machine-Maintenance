# `static/` README — Front-End Assets for Flask Application

This folder contains all **static front-end assets** used by the **Smart Manufacturing — Efficiency Prediction** Flask web interface. These assets define the **look, feel, and visual interactivity** of the MLOps Machine Maintenance prediction app.

## 📁 Folder Overview

```text
static/
├── style.css               # 🎨 Core styling and layout rules for the web app
└── img/
    └── app_background.jpg  # 🖼️ Background image for the app interface
```

## 🎨 `style.css` — Application Styling

### Purpose

Defines the complete visual design for the Flask app, including:

* Page background and translucent overlay
* Typography, spacing, and responsive layout
* Glowing blue header and title text
* Two-column grid form for desktop (auto-stacking on mobile)
* Interactive input fields and animated submit buttons
* Transparent form card with 15% opacity for readability
* Styled prediction results and badge components

### Key Design Features

| Feature                | Description                                                                                  |
| ---------------------- | -------------------------------------------------------------------------------------------- |
| **Background Overlay** | Adds a soft transparent layer over the background image for improved contrast.               |
| **Glowing Title Text** | The title features a neon-blue glow using layered shadows to stand out.                      |
| **Transparent Card**   | The form container (`.card`) has 15% transparency to blend subtly with the image background. |
| **Responsive Design**  | Automatically shifts to one-column layout on smaller screens (`max-width: 720px`).           |
| **Input Highlights**   | Inputs and dropdowns glow blue when focused, improving accessibility and feedback.           |
| **Gradient Buttons**   | The “Predict Efficiency” button uses a blue-to-light-blue gradient with hover animations.    |

### Example Code Snippet

```css
.title {
  font-size: 42px;
  font-weight: 900;
  text-transform: uppercase;
  color: #ffffff;
  text-shadow:
    0 0 5px #42a5f5,
    0 0 10px #42a5f5,
    0 0 15px #42a5f5,
    0 0 20px #0d47a1;
}
```

This creates the bright **neon-blue glow** for the main title.

## 🖼️ `img/app_background.jpg` — Background Image

### Purpose

Used as the **full-page visual background** for the web application.
It is fixed in place and covered by a light gradient overlay to maintain text readability.

### CSS Reference

```css
.page {
  background: linear-gradient(rgba(255,255,255,0.15), rgba(255,255,255,0.15)),
              url("/static/img/app_background.jpg") center/cover no-repeat fixed;
}
```

### Tips for Replacement

1. Place a new image file (ideally `.jpg`) into `static/img/`.
2. Rename it to `app_background.jpg`, or update the CSS path accordingly.
3. Choose an image with soft tones and good contrast to ensure text remains readable.

## 🧩 Integration with Flask

The stylesheet and background image are served automatically by Flask using `url_for()`:

```html
<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
```

Flask handles all static files under the `/static/` directory, making deployment seamless.

## ✅ In summary

* `style.css` defines the **layout, colours, and responsive styling** of the interface.
* `img/app_background.jpg` provides the **visual background** with subtle transparency.
* Together, they create a **clean, modern, and user-friendly** front-end for the **MLOps Machine Maintenance** prediction app.
