# CI/CD Setup

This repository has automated CI/CD workflows set up using GitHub Actions.

## Workflows

### CI (Continuous Integration)

**File**: `.github/workflows/ci.yml`

**Triggers**:
- Push to `main` branch
- Pull requests to `main` branch

**Jobs**:
- **Test**: Runs tests on Python 3.11, 3.12, and 3.13
  - Installs dependencies
  - Runs ruff linter
  - Runs ruff formatter check
  - Runs pytest

- **Lint**: Separate linting job
  - Runs ruff linter
  - Runs ruff formatter check

### CD (Continuous Deployment)

**File**: `.github/workflows/cd.yml`

**Triggers**:
- Push to `main` branch (only runs if version changes)

**Jobs**:
1. **check-version**: Detects if the version in `pyproject.toml` has changed
2. **create-tag**: Creates a git tag (e.g., `v0.2.0`) when version changes
3. **publish**: Builds and publishes the package to PyPI
4. **create-release**: Creates a GitHub release with changelog notes

## Setup Requirements

### 1. PyPI API Token

To publish to PyPI, you need to set up a PyPI API token:

1. Go to https://pypi.org/manage/account/token/
2. Create a new API token (you can scope it to this project)
3. Add the token to your GitHub repository secrets:
   - Go to your repository on GitHub
   - Navigate to Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Name: `PYPI_API_TOKEN`
   - Value: Your PyPI API token

### 2. Repository Permissions

The workflows require certain permissions:

- The CD workflow needs `contents: write` permission to create tags and releases
- The CD workflow needs `id-token: write` for trusted publishing (optional, but recommended)

These are already configured in the workflow files.

### 3. Publishing Workflow

To publish a new version:

1. Update the version in `pyproject.toml`:
   ```toml
   version = "0.3.0"  # Increment from current version
   ```

2. Update `CHANGELOG.md` with the changes for this version:
   ```markdown
   ## [0.3.0] - 2024-11-01

   ### Added
   - New feature description

   ### Fixed
   - Bug fix description
   ```

3. Commit and push to `main`:
   ```bash
   git add pyproject.toml CHANGELOG.md
   git commit -m "Bump version to 0.3.0"
   git push origin main
   ```

4. The CD workflow will automatically:
   - Detect the version change
   - Create a git tag `v0.3.0`
   - Build the package
   - Publish to PyPI
   - Create a GitHub release with changelog notes

## Testing the Workflows

### Testing CI Locally

You can run the checks locally before pushing:

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run linter
ruff check .

# Run formatter check
ruff format --check .

# Run tests
pytest -v
```

### Testing CD (Version Detection)

The version detection only triggers when the version in `pyproject.toml` changes between commits. To test:

1. Make a test branch
2. Change the version in `pyproject.toml`
3. Commit and push
4. The workflow will detect the change but only on `main` branch

## Troubleshooting

### PyPI Publishing Fails

- Check that `PYPI_API_TOKEN` secret is set correctly
- Ensure the version number is higher than any existing version on PyPI
- Verify that the package name is available on PyPI

### Tag Creation Fails

- Check that GitHub Actions has write permissions to your repository
- Ensure the tag doesn't already exist

### Tests Fail

- Run tests locally to debug: `pytest -v`
- Check the GitHub Actions logs for detailed error messages

## Alternative: Trusted Publishing

Instead of using an API token, you can set up PyPI Trusted Publishing:

1. Go to https://pypi.org/manage/project/vimkeys-input/settings/publishing/
2. Add a new publisher with:
   - Repository owner: jasoncronquist
   - Repository name: vimkeys-input
   - Workflow name: cd.yml
   - Environment: pypi

3. Remove the `password` line from the publish step in `cd.yml` (trusted publishing uses OIDC)

This is more secure as it doesn't require storing tokens.
