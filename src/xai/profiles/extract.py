from src.file_operations.file_operations import filter_x_handles_with_score
from src.xai.json_formating import clean_json_text
from src.xai.xai_client import XAIClient

tweet_handles = filter_x_handles_with_score('../../../data/ranked/tweets_Wed02251523_ranked.csv', 3)
print(tweet_handles)


def extract_profile_info(x_handle: str, xai_client: XAIClient) -> dict:
    prompt = f"""
                Analyze the posts from the X handle "@{x_handle}" and return a structured JSON object with the following details:
                Extract Industry Keywords & Hashtags (Identify up to 4 key terms or hashtags that represent the startup’s market focus).
                Identify the Number of Founders (If mentioned in posts).
                Extract Names of Founders (If explicitly stated).
                Check for Grants or Funding Won (If an amount is mentioned, return it in USD, otherwise return 0).
                Detect Investor & Ecosystem Engagement (Identify mentions of VC firms, angel investors, or startup accelerators).
                Provide sentences from the posts as evidence for each field.
                Strictly return the output in this JSON format:


                {{
    "Industry_Keywords_Hashtags": ["keyword1", "keyword2", "keyword3", "keyword4"],
                  "Number_of_Founders": X,
                  "Name_of_Founders": ["Founder1", "Founder2"],
                  "Grants_or_Funding_Won": amount_in_USD,
                  "Investor_Ecosystem_Engagement": ["VC1", "Angel1", "Accelerator1"],
                   "Evidence": {{
                    "Industry_Keywords_Hashtags": "Sentence from the post mentioning keywords or hashtags.",
                    "Number_of_Founders": "Sentence that indicated the number of founders.",
                    "Name_of_Founders": "Sentence explicitly mentioning the founder's name(s).",
                    "Grants_or_Funding_Won": "Sentence mentioning funding or grants won.",
                    "Investor_Ecosystem_Engagement": "Sentence mentioning VC firms, angel investors, or startup accelerators."
                  }}
                Do not fabricate data—if a field is not found, return null (except for funding, which should default to 0).
                No additional explanations—only return the JSON object.
                This ensures clear, structured output while avoiding hallucinated information.
                 """

    system_message = f"""
               You are an intelligent startup profile creator. Your task is to extract and analyze posts from an X (formerly Twitter) handle to generate a structured startup profile.

                Follow these steps to ensure accuracy:

                Extract information from posts, focusing on industry keywords, hashtags, founders, funding, and ecosystem engagement.
                Identify patterns and categorize insights to infer key details.
                Ensure accuracy by cross-referencing mentions within the posts.
                Output only the required JSON format with no additional text.
                Output Format (Strictly Follow This JSON Format)

               {{
    "Industry_Keywords_Hashtags": ["keyword1", "keyword2", "keyword3", "keyword4"],
                  "Number_of_Founders": X,
                  "Name_of_Founders": ["Founder1", "Founder2"],
                  "Grants_or_Funding_Won": amount_in_USD,
                  "Investor_Ecosystem_Engagement": ["VC1", "Angel1", "Accelerator1"],
                    "Evidence": {{
                    "Industry_Keywords_Hashtags": "Sentence from the post mentioning keywords or hashtags.",
                    "Number_of_Founders": "Sentence that indicated the number of founders.",
                    "Name_of_Founders": "Sentence explicitly mentioning the founder's name(s).",
                    "Grants_or_Funding_Won": "Sentence mentioning funding or grants won.",
                    "Investor_Ecosystem_Engagement": "Sentence mentioning VC firms, angel investors, or startup accelerators."
                  }}
                If no information is found for a field, return null instead of fabricating an answer.
                If no grants or funding are found, return "Grants_or_Funding_Won": 0.
                Ensure concise yet accurate keyword selection for industry focus (maximum 4).
                Only return names of founders if explicitly mentioned in posts.
                Provide relevant sentences from the startup’s posts as evidence for each field.
    
                Do not include any additional text, comments, or explanations. Only return the JSON object.
    """

    try:
        response_text = xai_client.ask(system_message, prompt, model="grok-2-latest")
        result = clean_json_text(response_text)
        print(f"Response for {x_handle}: {result}")
        return result
    except Exception as e:
        print(f"Error parsing response for {x_handle}: {e}")
        return {}
