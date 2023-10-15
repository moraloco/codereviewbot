import os
import openai
import logging

# Ensure logger is configured.
logger = logging.getLogger(__name__)
logger.propagate = True

class Reviewer:
    def __init__(self, api_key, api_type, model_type, max_tokens):
        self.api_key = api_key
        self.api_type = api_type
        self.model_type = model_type
        self.max_tokens = max_tokens
        openai.api_key = self.api_key
        
        # Set up API details based on the type
        if self.api_type == "azure":
            openai.api_type = self.api_type
            openai.api_base = os.getenv("API_BASE")
            openai.api_version = os.getenv("API_VERSION", "2023-07-01-preview")  # Default version  

    def generate_prompt(self, patch):
        prompt_template = (
            "Below is a code patch, please help me do a brief code review on it. "
            "Any bug risks and/or improvement suggestions are welcome:\n\n{}"
        )
        return prompt_template.format(patch)

    def compile_review(self, reviews):
        prompt = "Compile the following code review comments into a comprehensive and cohesive review:\n\n"
        for i, review in enumerate(reviews):
            prompt += f"Comment {i+1}: {review}\n\n"
        prompt += "End of comments. Please provide a summarized review."

        try:
            response = openai.ChatCompletion.create(
                model=self.model_type,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant, that is an expert in compiling code review comments into a easily understandable and structured way."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens
            )
            compiled_review = response['choices'][0]['message']['content'].strip()
        except openai.error.OpenAIError as e:
            logger.error(f"OpenAI API error: {str(e)}")
            compiled_review = "\n".join(reviews)  # Fallback to concatenating original reviews
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            compiled_review = "\n".join(reviews)  # Fallback
        
        return compiled_review

    def generate_review(self, patch):
        reviews = []
        for i in range(0, len(patch), self.max_tokens):
            chunk = patch[i:i + self.max_tokens]
            prompt = self.generate_prompt(chunk)
            
            try:
                response = openai.ChatCompletion.create(
                    model=self.model_type,
                    messages=[
                        {"role": "system", "content": "You are a Senior Developer with many years of experience. You are always concise and constructive in your code reviews."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=self.max_tokens
                )
                reviews.append(response['choices'][0]['message']['content'].strip())
            except openai.error.OpenAIError as e:
                logger.error(f"OpenAI API error: {str(e)}")
            except Exception as e:
                logger.error(f"Unexpected error: {str(e)}")
        
        # Compile the individual reviews into a comprehensive review
        final_review = self.compile_review(reviews)
        return final_review