
# Code Review Bot using OpenAI and Bitbucket Webhooks

A Python bot that performs code reviews by integrating Bitbucket pull request webhooks and OpenAI's ChatGPT, capable of working with both Bitbucket Cloud and Data Center.

## Overview

- **Webhook Listener**: Listens for Bitbucket pull request webhooks.
- **OpenAI API Interaction**: Sends code diffs to OpenAI API and retrieves generated reviews.
- **Bitbucket API Interaction**: Posts the generated reviews as comments on Bitbucket pull requests.

## Prerequisites

- Docker
- Bitbucket repository and admin access to set up webhooks
- OpenAI API key
- Bitbucket OAuth Consumer Key and Secret

## Setup and Configuration

### 1. Bitbucket OAuth Consumer
Create an OAuth consumer in Bitbucket.

- Navigate to Bitbucket settings.
- Under "Access Management", select "OAuth".
- Click "Add consumer" and set the permissions (ensure write access to pull requests).
- Note down the key and secret.

### 2. OpenAI API Key
Obtain an API key from OpenAI. Visit [OpenAI's platform](https://beta.openai.com/signup/).

### 3. Set Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key.
- `BITBUCKET_KEY`: Bitbucket OAuth consumer key.
- `BITBUCKET_SECRET`: Bitbucket OAuth consumer secret.
- `BITBUCKET_API_URL`: API Base URL (e.g., `https://api.bitbucket.org/2.0` for Cloud or your Bitbucket Data Center API Base URL).
- `BITBUCKET_WORKSPACE`: (For Cloud) Your Bitbucket workspace.

### 4. Docker Build and Run
```sh
docker build -t code_review_bot .
docker run -p 5000:5000 -e OPENAI_API_KEY='your-openai-api-key' -e BITBUCKET_KEY='your-bitbucket-key' -e BITBUCKET_SECRET='your-bitbucket-secret' -e BITBUCKET_API_URL='your-bitbucket-api-url' -e BITBUCKET_WORKSPACE='your-bitbucket-workspace' code_review_bot
```
Replace placeholders with actual keys and URLs.

### 5. Bitbucket Webhook Setup
- Navigate to your Bitbucket repository settings.
- Under "Workflow", find "Webhooks" and click "Add webhook".
- Set:
  - **Title**: CodeReviewBot
  - **URL**: `http://[your_docker_host_ip]:5000/webhook`
  - **Triggers**: Choose "Pull Request".

### 6. Testing
Create a pull request on your Bitbucket repository and observe the bot posting a review comment.

## Note

- **Security**: Use HTTPS for production deployment and validate webhook requests.
- **Handling Larger Diffs**: The bot sends code diffs in chunks to the OpenAI API and concatenates responses.
- **Rate Limiting**: Be mindful of OpenAI API rate limits and configure the bot accordingly.
- **API Interaction**: Adjust API interaction and payload handling according to Bitbucket Cloud or Data Center requirements.
- **Error Handling**: Consider enhancing error handling and logging as per your deployment scenario.

## Usage and Modification

- Adjust webhook payload handling as per Bitbucket Cloud or Data Center.
- Modify OpenAI API interaction and response handling as per requirements.
- Ensure to handle API rate limits and responses gracefully.

## License

MIT License. See [LICENSE.md](LICENSE.md) for details.

## Contribution

Fork, modify, and contribute to enhance functionality or adapt to specific use-cases.
