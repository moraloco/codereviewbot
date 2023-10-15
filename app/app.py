import logging
from utils.logging_config import configure_logging

# Setup logging
configure_logging()
logger = logging.getLogger(__name__)

import threading
from flask import Flask, request, jsonify
from reviewers.generic_reviewer import Reviewer
from utils.config import configurations
from utils.handler_utils import HandlerUtils
import os

# Setup Flask app
app = Flask(__name__)

# Fetch platform type from environment variables
PLATFORM_TYPE = os.getenv("PLATFORM_TYPE", "bitbucket_cloud")  # Default to 'bitbucket_cloud' if not set

# Fetch SSL Mode
SSL_MODE = os.getenv('SSL_MODE', 'none')  # Default to 'none' if SSL_MODE is not set

# Fetch API details from environment variables
API_TYPE = os.getenv("API_TYPE", "openai")
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
BITBUCKET_WORKSPACE = os.getenv('BITBUCKET_WORKSPACE', None)

# Select the configuration based on the platform type
provider_config = configurations.get(PLATFORM_TYPE.lower())
if provider_config is None:
    raise ValueError(f"Invalid platform: {PLATFORM_TYPE}")

# Model configuration for OpenAI
MODEL_TYPE = os.getenv("MODEL_TYPE", "gpt-3.5-turbo-16k")
MAX_TOKENS = os.getenv("MAX_TOKENS", 4096)

# Initialize classes
oauth_handler = HandlerUtils.load_oauth_handler(PLATFORM_TYPE, provider_config, BITBUCKET_WORKSPACE)
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

    # Initialize WebhookHandler dynamically
    logger.debug("Attempting to create WebhookHandler instance...")
    handler = HandlerUtils.load_webhook_handler(data, oauth_handler, reviewer, PLATFORM_TYPE)
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
    if SSL_MODE == 'none':
        ssl_context = None
    elif SSL_MODE == 'adhoc':
        ssl_context = 'adhoc'
    elif SSL_MODE == 'custom':
        ssl_context = (os.getenv('SSL_CERT_PATH'), os.getenv('SSL_KEY_PATH'))
    else:
        raise ValueError(f'Invalid SSL_MODE: {SSL_MODE}')


    app.run(host='0.0.0.0', port=5000, debug=False, ssl_context=ssl_context)
