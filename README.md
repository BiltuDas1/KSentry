# KSentry

KSentry is a lightweight, serverless security and workflow orchestrator. It acts as a final line of defense for your main branch by intercepting Pull Requests to perform two critical tasks:

1. Zero-Trust Secret Scanning: Uses Gitleaks to identify and redact leaked credentials before they merge.
2. Round Robin Reviewer Logic: Fairly distributes workload by rotating assignments among established contributors, ensuring no single developer becomes a bottleneck.
