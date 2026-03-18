# Deployment Information for App Store Clone

## Server Choice
**Target Provider:** DigitalOcean
**Droplet Configuration:**
- Shared CPU (Basic)
- 2 GB RAM / 1 vCPU
- Ubuntu 22.04 LTS

## Environment Configuration
- **Python Version:** 3.12
- **Web Framework:** Flask
- **Database:** SQLite (local file `app_store/app_store.db`)
- **Required Libraries:**
  - `flask`
  - `werkzeug`

## Storage Structure
- `app_store/uploads/`: Stores the APK files.
- `app_store/static/icons/`: Stores app icons.
- `app_store/static/screenshots/`: Stores app screenshots.

## Security Considerations
- Use `werkzeug.utils.secure_filename` for all file uploads.
- Serve APKs through a dedicated Flask route with `send_from_directory`.
- Implementation of further access controls (e.g., JWT) is planned for the future.

## Run Instructions
1. Install dependencies: `pip install -r requirements.txt`
2. Run the application: `python app_store/app.py`
