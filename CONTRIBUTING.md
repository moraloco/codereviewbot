# Contributing to codereviewbot

We love your input! We want to make contributing to this project as easy and transparent as possible, whether it's:
- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features

## Develop with Github

We use Github to host code, to track issues and feature requests, as well as accept pull requests.

## Verified Commits using GPG

In the interest of ensuring the integrity of our code and protecting it from malicious actors, we require contributors to sign their commits with a verified GPG key. This provides an additional layer of security and ensures that the commits were indeed created by a trusted individual.

### How to Configure GPG Key Signatures

1. **Generate a GPG key pair**: If you do not have a GPG key pair, you can generate one by following [GitHub's detailed guide on generating a new GPG key](https://docs.github.com/en/github/authenticating-to-github/generating-a-new-gpg-key).

2. **Add the GPG key to your GitHub account**: Once you have a GPG key pair, make sure to add it to your GitHub account. Instructions can be found in [GitHub’s documentation for adding a new GPG key to your GitHub account](https://docs.github.com/en/github/authenticating-to-github/adding-a-new-gpg-key-to-your-github-account).

3. **Sign your commits**: Ensure that your commits are signed. You can do this on a per-commit basis with `git commit -S` or configure Git to [sign all of your commits by default](https://docs.github.com/en/github/authenticating-to-github/signing-commits).

### Why Verified Commits?

- **Security**: Verifying commits and tags verifies that the commits in the project are from a trusted source.
- **Integrity**: The GPG signature ensures that the commit is integral and hasn’t been tampered with.

## Pull Requests

We actively welcome your pull requests:
1. Fork the repo and create your branch from `master`.
2. If you've added code that should be tested, add tests.
3. Ensure the test suite passes.
4. Make sure your code lints.
5. Ensure that your commits are signed with the GPG key.
6. Issue that pull request!

## License

By contributing, you agree that your contributions will be licensed under its MIT License.
