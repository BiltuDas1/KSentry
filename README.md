# KSentry

KSentry is a lightweight, serverless security and workflow orchestrator. It acts as a final line of defense for your main branch by intercepting Pull Requests to perform two critical tasks:

1. Zero-Trust Secret Scanning: Uses Gitleaks to identify and redact leaked credentials before they merge.
2. Round Robin Reviewer Logic: Fairly distributes workload by rotating assignments among established contributors, ensuring no single developer becomes a bottleneck.

## Generate `requirements.txt`

1. Use the following command to convert the `pyproject.toml` to `requirements.txt`

   ```sh
   poetry export --without-hashes -f requirements.txt --output requirements.txt
   ```

2. Now use the following command to install the `requirements.txt`

   ```sh
   pip install --no-deps -r requirements.txt
   ```

## Deploy

### Deploy in Vercel

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/BiltuDas1/KSentry&template=fastapi)
