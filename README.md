
# Code Review Bot using OpenAI and Bitbucket Webhooks with OAuth 2.0

A Python bot that performs code reviews by integrating Bitbucket pull request webhooks and OpenAI's ChatGPT, capable of working with both Bitbucket Cloud and Data Center.

## Overview

- **Webhook Listener**: Listens for Bitbucket pull request webhooks.
- **OpenAI API Interaction**: Sends code diffs to OpenAI API and retrieves generated reviews.
- **Bitbucket API Interaction**: Uses OAuth 2.0 to securely post the generated reviews as comments on Bitbucket pull requests.

## Prerequisites

- Docker
- Bitbucket repository and admin access to set up webhooks
- OpenAI API key
- Bitbucket OAuth Consumer Key and Secret

## Setup and Configuration

### 1. Bitbucket OAuth Consumer
Create an OAuth consumer in Bitbucket using OAuth 2.0 with Grant Type Credentials.

- Navigate to Bitbucket settings.
- Under "Access Management", select "OAuth".
- Click "Add consumer" and set the permissions (ensure write access to pull requests).
- **Callback URL**: Set a callback URL even though it is not used in this application, for instance, `https://localhost/`.
- Note down the key and secret.

### 2. OpenAI API Key
Obtain an API key from OpenAI. Visit [OpenAI's platform](https://beta.openai.com/signup/).

### 3. Set Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key.
- `BITBUCKET_KEY`: Bitbucket OAuth consumer key.
- `BITBUCKET_SECRET`: Bitbucket OAuth consumer secret.
- `BITBUCKET_API_URL`: API Base URL (e.g., `https://api.bitbucket.org/2.0` for Cloud or your Bitbucket Data Center API Base URL).
- `BITBUCKET_WORKSPACE`: (For Cloud) Your Bitbucket workspace.

### SSL Configuration

The application can be configured to use different modes of SSL, controlled by the `SSL_MODE` environment variable:

- **None**: No SSL (for development environments).
- **Ad-hoc**: Uses Flask's built-in ad-hoc SSL for development purposes.
- **Custom**: Uses your custom SSL certificate and key.

Set the `SSL_MODE` environment variable according to your use-case:
- `SSL_MODE=none`: No SSL.
- `SSL_MODE=adhoc`: Ad-hoc SSL.
- `SSL_MODE=custom`: Custom SSL certificate.

For custom SSL, set the paths to your SSL certificate and key as environment variables:
- `SSL_CERT_PATH`: Path to your SSL certificate.
- `SSL_KEY_PATH`: Path to your SSL key.

### Using Azure OpenAI API

To utilize Azure OpenAI API instead of the standard OpenAI API, follow the steps below:

1. Ensure that your Azure OpenAI API is set up and note down the API key.
2. Set the following environment variables:
   - `API_TYPE=azure`: This tells the application to use the Azure OpenAI API settings.
   - `API_BASE`: The base URL of your Azure OpenAI API. Default is "https://{Company}openai.openai.azure.com/".
   - `API_VERSION`: The version of your Azure OpenAI API. Default is "2023-07-01-preview".
   
If you wish to switch back to the standard OpenAI API, you can simply change or remove the `API_TYPE` environment variable.

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

- **Security**: Ensure to use HTTPS for production deployment and validate webhook requests using secret verifications.
- **Handling Larger Diffs**: The bot sends code diffs in chunks to the OpenAI API and concatenates responses.
- **Rate Limiting**: Be aware of OpenAI API rate limits and configure the bot to handle them gracefully.
- **API Interaction**: Adjust API interaction and payload handling according to Bitbucket Cloud or Data Center requirements.
- **Error Handling**: Consider enhancing error handling and logging as per your deployment scenario.
- **SSL/TLS**: Ensure to use the appropriate SSL mode for your deployment scenario. Avoid using ad-hoc SSL for production. When deploying with Docker, map ports accordingly and ensure the SSL certificate and key files are accessible within the container.

This readme is made with the help of ChatGPT.

## Usage and Modification

- Adjust webhook payload handling as per Bitbucket Cloud or Data Center.
- Modify OpenAI API interaction and response handling as per requirements.
- Ensure to handle API rate limits and responses gracefully.

## License

MIT License. See [LICENSE.md](LICENSE.md) for details.

## Contribution

Feel free to fork, modify, and contribute to enhance functionality or adapt to specific use-cases. Contributions, issues, and feature requests are welcome!
