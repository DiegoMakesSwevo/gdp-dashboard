# 📐 Riemann Sum Practice Studio

An interactive Streamlit app for practicing upper and lower sums, trapezoidal estimates, and midpoint rules with preset examples, a custom sandbox, and randomized drills.

### How to run locally

1. Install dependencies

   ```bash
   pip install -r requirements.txt
   ```

2. Start the app

   ```bash
   streamlit run streamlit_app.py
   ```

3. Open the provided local URL (usually http://localhost:8501) in your browser to see the website.

### What you can do
- Browse ready-to-use practice cards for common functions and intervals.
- Build custom problems by choosing a function, interval `[a,b]`, and subinterval count `n`.
- Generate repeatable random drills with an optional seed to compare your hand calculations against computed upper/lower sums, trapezoids, and midpoint approximations.
