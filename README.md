# Somesh Kumar | Personal Portfolio

A responsive personal portfolio for Somesh Kumar, a second-year B.Tech Computer Science and Engineering student at SRKR Engineering College. The site presents an introduction, skills, education, projects, certifications, a downloadable starter resume, and a contact form powered by Flask and SQLite.

## Features

- Responsive dark portfolio layout with mobile navigation
- Projects, skills, education, and certification sections
- Downloadable PDF resume, generated on first run if no resume exists
- Contact form with server-side validation and SQLite storage
- Flask static assets and environment-based port for Render
- Accessible labels, skip link, reduced-motion support, and a spam honeypot

## Technologies

Python, Flask, SQLite, ReportLab, HTML5, CSS3, JavaScript, Git/GitHub, Gunicorn, and Render.

## Project structure

```text
portfolio/
├── app.py
├── requirements.txt
├── Procfile
├── .gitignore
├── README.md
├── templates/
│   └── index.html
├── static/
│   ├── css/style.css
│   ├── js/script.js
│   └── images/profile.svg
└── resume/
    └── resume.pdf       # Generated on first run; replace with your final resume
```

The contact database is created at `instance/contact_messages.db` and is excluded from Git.

## Run locally in VS Code

1. Open this project folder in VS Code and open a terminal in the folder.
2. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   On macOS/Linux, activate it with `source .venv/bin/activate`.
3. Install the dependencies:

   ```shell
   python -m pip install -r requirements.txt
   ```
4. Run Flask:

   ```shell
   python app.py
   ```

5. Open `http://127.0.0.1:5000` in your browser. The app binds to `0.0.0.0` and reads its port from `PORT` (default `5000`).

## Personalize before publishing

- Replace `somesh.kumar@example.com`, `your-username`, and `your-profile` in `templates/index.html` and the starter resume content in `app.py`.
- Replace the example GitHub and demo URLs in `PROJECTS` in `app.py` with real project links.
- Replace `static/images/profile.svg` with a profile image you have the rights to use. Update its `url_for` path in `templates/index.html` if you choose a different filename.
- Replace the generated `resume/resume.pdf` with your final resume PDF. Existing PDFs are not overwritten.
- Set a unique `SECRET_KEY` in your local environment and in Render. Contact messages are stored in SQLite; Render's default filesystem is ephemeral, so use a persistent disk or external database if messages must survive redeploys.

## GitHub setup and push

Create an empty repository on GitHub (do not initialize it with a README if you already have this one). In the VS Code terminal, from the project folder:

```shell
git init
git add .
git commit -m "Build personal portfolio website"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

Replace the remote URL with your repository URL. Later updates use `git add .`, `git commit -m "Describe your update"`, and `git push`.

## Deploy on Render

1. Push the project to GitHub using the steps above.
2. Sign in at [Render](https://render.com/) and choose **New +** then **Web Service**.
3. Connect GitHub, select this repository, and choose the `main` branch.
4. Choose **Python** as the runtime and set:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT`
5. Choose an instance plan, then add an environment variable named `SECRET_KEY` with a long, unique random value. Render provides `PORT` to the running service; the start command binds Gunicorn to that assigned port.
6. Select **Create Web Service**. Render installs dependencies, starts Gunicorn, and provides a public `onrender.com` URL when deployment finishes.
7. Open the URL and test navigation, the resume download, and the contact form.

## Common deployment errors

- **Build fails or a module is missing:** Confirm `requirements.txt` is committed and the build command is `pip install -r requirements.txt`.
- **Application fails to start:** Use `gunicorn app:app --bind 0.0.0.0:$PORT`; `app` before the colon is `app.py`, and the second `app` is the Flask application object.
- **Service does not bind to the assigned port:** Do not hard-code a Render port. Gunicorn detects Render's port in the Render environment; `python app.py` uses `PORT` for local/direct runs.
- **Resume download returns an error:** Check the service logs for dependency errors and confirm `reportlab` is in `requirements.txt`. The starter PDF is generated on application startup if the file is missing.
- **Contact messages disappear after redeploy:** Render's default filesystem is temporary. Attach a persistent disk for the SQLite file or move message storage to a managed database.
- **Changes do not appear online:** Confirm the intended branch was pushed and check the latest deployment logs in Render.

## Repository and live demo

- GitHub repository: `https://github.com/YOUR-USERNAME/YOUR-REPOSITORY`
- Live demo: `https://YOUR-SERVICE-NAME.onrender.com` (replace with the URL Render assigns)