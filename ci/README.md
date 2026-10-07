# CI workflow (pending activation)

`github-workflow-ci.yml` is a ready GitHub Actions workflow: it compiles every
Python file, runs the smoke tests in `v45_beta/tests`, and starts the Streamlit
app headless to confirm it answers its health check, on Python 3.11 and 3.13.

It could not be committed under `.github/workflows/` from the session that
wrote it because that token lacked the `workflow` scope. To activate it:

```bash
mkdir -p .github/workflows
git mv ci/github-workflow-ci.yml .github/workflows/ci.yml
git commit -m "ci: enable GitHub Actions workflow"
git push
```
