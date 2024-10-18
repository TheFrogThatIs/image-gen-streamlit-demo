from typing import Dict
import requests

hive_task_endpoint = 'https://api.thehive.ai/api/v2/task/sync'

def generate_image_response(
        text_input: str,
        hiveai_key: str,
        negated_input: str = "",
        images_count: int = 1,
) -> Dict | None:
    # https://docs.thehive.ai/docs/image-generation
    # Example Output: https://docs.thehive.ai/reference/image-generation-1
    request_body = {
        "options": {
            "neg_text": negated_input,
            "num_images": images_count,
        },
        "text_data": text_input,
        # "callback_url": "example_url"
    }
    headers = {
        "Authorization": f"Token {hiveai_key}",
        "Content-Type": "application/json",
    }
    response = requests.post(url=hive_task_endpoint, headers=headers, json=request_body)
    return response.json()
