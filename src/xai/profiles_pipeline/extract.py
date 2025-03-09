from src.file_operations.file_operations import filter_x_handles_with_score
from src.xai.json_formating import clean_json_text
from src.xai.xai_client import XAIClient

tweet_handles = filter_x_handles_with_score('../../../data/ranked/tweets_Wed02251523_ranked.csv', 3)
print(tweet_handles)


def extract_profile_info(x_handle: str, xai_client: XAIClient) -> dict:
    prompt = f"""
                    Analyze the posts from the X handle "@{x_handle}" and return a structured JSON object with the following details:

                    Check for Grants or Funding Won:
                    - If an amount is mentioned, return it. If no amount is found, return 0.
                    - Identify the type of funding (e.g., grant, funding, hackathon prize, angel investment, etc.).
                    - Provide the exact sentence from the post that mentions funding or grants won.
                    - Include the URL of the post where the funding information was found.

                    Strictly return the output in this JSON format:

                    {{
                      "amount": amount_in_USD,
                      "type": "Type of funding (e.g., grant, funding, hackathon, angel investment)",
                      "evidence": {{
                        "sentence": "Sentence mentioning funding or grants won.",
                        "post_URL": "URL of the post containing the funding information."
                      }}
                    }}

                    If no funding information is found, return:
                    {{
                      "amount": 0,
                      "type": null,
                      "evidence": {{
                        "sentence": null,
                        "post_URL": null
                      }}
                    }}

                    Do not fabricate data—only return funding details if explicitly mentioned.
                    No additional explanations—only return the JSON object.
    """

    system_message = f"""
                    You are an intelligent startup funding analyzer. Your task is to extract and verify information about grants or funding won from an X (formerly Twitter) handle.

                    Follow these steps to ensure accuracy:

                    - Scan posts to detect explicit mentions of grants or funding.
                    - Extract the amount mentioned . If no amount is found, return 0.
                    - Identify the type of funding (e.g., grant, funding, hackathon, angel investment).
                    - Provide the exact sentence that mentions the funding or grant.
                    - Include the URL of the post where the funding information was found.

                    **Output Format (Strictly Follow This JSON Format)**

                    {{
                      "amount": amount_in_USD,
                      "type": "Type of funding (e.g., grant, funding, hackathon, angel investment)",
                      "evidence": {{
                        "sentence": "Sentence mentioning funding or grants won.",
                        "post_URL": "URL of the post containing the funding information."
                      }}
                    }}

                    **If no funding information is found, return:**
                    {{
                      "amount": 0,
                      "type": null,
                      "evidence": {{
                        "sentence": null,
                        "post_URL": null
                      }}
                    }}

                    **Rules:**
                    - Do not fabricate any data. Only include information explicitly mentioned in posts.
                    - Convert currency to USD if necessary.
                    - If the type of funding cannot be determined, return null for the "type" field.
                    - Do not add explanations—return only the structured JSON response.
    """

    try:
        response_text = xai_client.ask(system_message, prompt, model="grok-2-latest")
        result = clean_json_text(response_text)
        print(f"Response for {x_handle}: {result}")
        return result
    except Exception as e:
        print(f"Error parsing response for {x_handle}: {e}")
        return {}
