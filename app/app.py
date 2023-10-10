import logging
from logging_config import configure_logging

# Setup logging
configure_logging()
logger = logging.getLogger(__name__)

import threading
from flask import Flask, request, jsonify
from bitbucket_oauth import BitbucketOAuth
from reviewer import Reviewer
from webhook_handler import WebhookHandler
from config import configurations
import os

# Setup Flask app
app = Flask(__name__)

# Fetch API details from environment variables
API_TYPE = os.getenv("API_TYPE", "openai")
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
BITBUCKET_WORKSPACE = os.getenv('BITBUCKET_WORKSPACE', None)
is_cloud = bool(BITBUCKET_WORKSPACE)

# Select the configuration based on the type of Bitbucket instance
if is_cloud:
    provider_config = configurations['bitbucket_cloud']
else:
    provider_config = configurations['bitbucket_data_center']

# Model configuration for OpenAI
MODEL_TYPE = os.getenv("MODEL_TYPE", "gpt-3.5-turbo-16k")
MAX_TOKENS = os.getenv("MAX_TOKENS", 4096)

# Initialize classes
oauth_handler = BitbucketOAuth(provider_config, BITBUCKET_WORKSPACE)
reviewer = Reviewer(OPENAI_API_KEY, API_TYPE, MODEL_TYPE, MAX_TOKENS)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    logger.debug("Webhook endpoint hit. Processing...")

    try:
        data = request.get_json()
    except Exception as e:
        logger.exception("Failed to parse JSON data: %s", str(e))
        return jsonify({"message": "Bad Request: Failed to parse JSON"}), 400

    if not data:
        logger.error("No JSON data received in webhook.")
        return jsonify({"message": "Bad Request: No data received"}), 400
    
    logger.debug("Webhook data received: %s", data)

    # Initialize WebhookHandler
    logger.debug("Attempting to create WebhookHandler instance...")
    handler = WebhookHandler(data, is_cloud, oauth_handler, reviewer)
    logger.debug("WebhookHandler instance created successfully.")
    
    # Use threading to process webhook in the background
    threading.Thread(target=process_webhook_in_thread, args=(handler,)).start()

    logger.info("Webhook acknowledged and will be processed in the background.")
    return jsonify({"message": "Webhook received"}), 200

def process_webhook_in_thread(handler):
    try:
        handler.process_webhook()
        logger.info("Webhook processed successfully")
    except Exception as e:
        logger.exception("Error processing webhook: %s", str(e))

if __name__ == "__main__":
    logger.debug("Starting the app...")
    app.run(host='0.0.0.0', port=5000, debug=False)
