# Contributing to KSentry

Thank you for your interest in contributing! To ensure a smooth process for everyone, please follow these guidelines for local setup, bug reporting, and feature suggestions.

## Local Development Setup

To get a local copy of the project up and running on your machine, follow these steps:

### Prerequisites

- Python 3.12+ and Node.js 24+
- Git, Poetry and Npm

### Installation

1. Clone the repository:

   ```bash
   git clone git@github.com:BiltuDas1/KSentry.git
   cd KSentry
   ```

2. Install Packages

   ```bash
   poetry install
   ```

3. Install `smee-client`

   ```bash
   npm install --global smee-client
   ```

### Configure the Project

#### Create a New Smee Channel

1. Go go https://smee.io/
2. Press Start a New channel
3. Copy the Webhook Proxy URL

#### Create a Github App

1. Go to https://github.com/settings/apps
2. Press the `New Github App` button
3. Fill all the required details
4. Mark the Webhook as Active
5. Set the Webhook URL as the Smee Webhook Proxy URL
6. Input a password in the secret field
7. Select `Where can this GitHub App be installed?` to `Only on this Account`
8. Press Create Github App

#### Setup Environments

1. Rename [.env.example](./.env.example) to `.env`
2. Select your app in https://github.com/settings/apps and press `edit`
3. Scroll down and then press `Generate Private Key`, and save the private key to your computer
4. Open the Private Key in a text editor and then copy the whole contents and set it in `.env` `APP_PRIVATE_KEY`
5. Write down the Webhook secret to the `APP_SECRET`
6. Copy the `APP_ID` from the same page and fill it in `.env`
7. Setup Redis Database and Set the connection URI to `REDIS_URL`

### Run the Project

1. Establish `smee` client

   ```bash
   smee -u <smee_webhook_url> -t http://localhost:5001
   ```

2. Start the Python Server

   ```bash
   poetry run python main.py
   ```

3. Now Install the Github App to your account and then start using it

> Note: To avoid permission issues during development, feel free to grant your development app broad Read & Write access to 'Pull Requests', 'Issues', and 'Content', then narrow them down once your feature is complete.

## Contribution Workflow

To keep the project history clean and manageable, please follow these steps when contributing:

### Fork the repository

- Click on the Fork button to fork it in your account
- Clone the repository using SSH in your computer

### Create a branch

Always create a new branch for your work. Avoid committing directly to `main`.

```bash
# Get the latest changes from main
git checkout main
git pull origin main

# Create a new branch (use a descriptive name)
git checkout -b feature/your-feature-name
# OR
git checkout -b bugfix/issue-description
```

### Make Your Changes

- Write your code and follow the existing style of the project.
- If you added a new feature, consider adding a basic test to verify it.
- Keep commits focused: Try to make one commit per logical change.
- If you installed any new package using poetry then consider running the following command to generate respective `requirements.txt`

  ```bash
  poetry export --without-hashes -f requirements.txt --output requirements.txt
  ```

### Format, Commit and Push

```bash
poetry run ruff format .
git add .
git commit -m "feat: describe your change in one sentence"
git push origin feature/your-feature-name
```

### Open a Pull Request

- Go to the KSentry Repository.
- You will see a prompt to "Compare & pull request."
- Describe what your PR does and link any related issues (e.g., Closes #12).
