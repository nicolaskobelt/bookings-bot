# Automate Aimharder bookings using selenium

**Customize bookings:**
 - Adapt the cron job in the actions.yml
 - Set your actions secrets USERNAME and PASSWORD
 - Logs can be checked in the status.log file

   

**Reference tutorial for github actions:**

[![Alt text](https://img.youtube.com/vi/PaGp7Vi5gfM/hqdefault.jpg)](https://youtu.be/PaGp7Vi5gfM)

This example shows how to run a Python script as cron job with GitHub Actions.

- Implement your script in `main.py`
- Inspect and configure cron job in GitHub Action `.github/workflows/actions.yml`
- It can install and use third party packages from `requirements.txt`
- Secret environment variables can be used. Set secrets in Settings/Secrets/Actions -> 'New repository secret'. Use the same secret name inside `actions.yml` and `main.py`
