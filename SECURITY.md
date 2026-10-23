# Security policy

Security fixes are maintained on the default branch on a best-effort basis. No response SLA is promised.

## Reporting

Use GitHub's **Report a vulnerability** option in this repository's Security tab when
available. For private repositories, report through an existing private maintainer
channel. If no private channel is available, request one without disclosing the issue.
Never post credentials, exploit details, personal records or production data in public issues.
For inherited upstream code, coordinate privately with the upstream maintainers as appropriate.

## Safe operation

- Keep credentials in environment variables or a secret manager, never tracked files or browser code.
- Use minimal API permissions, bounded execution and synthetic test inputs.
- Treat web content, agent prompts, external tools and pull requests as untrusted input.
- Review dependency updates and CI results before merging. Do not run untrusted PR code with write tokens or production secrets.
- Repository visibility is not application authorization. Internet-facing services need their own authentication, TLS and request limits.
- If a credential is exposed, revoke or rotate it at its provider. Deleting a file does not remove it from Git history or invalidate the credential.

Automated scanning and this policy do not constitute a penetration test or a guarantee
that all vulnerabilities have been found. Existing licenses and upstream notices remain authoritative.
