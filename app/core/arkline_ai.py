from groq import Groq
from dotenv import load_dotenv
from app.utils.extract_json import extract_clean_json
import os

load_dotenv()

class ArklineAI:

    SYSTEM_BASE_PROMPT = """
    - You are a smart classification assistant integrated into an intern request management system. 
    - Your task is to analyze the content of a submitted request and determine how urgent it is for HR to respond. 
    - Consider keywords and tones. 
    - Classify the intern requests based on urgency. 
    You must respond using this JSON format:

    Output: 
    {"urgency": ["High", "Medium", "Low", "Unknown"]}
    """

    BEHAVIOR_ONE_SHOT_MESSAGE = {
        "role": "user",
        "content": """
                Hi Ma'am/Sir,
                I hope you're doing well. I would like to request your assistance in signing my Memorandum of Agreement (MOA) as soon as possible. Our university requires it to be submitted by 3 PM today in order to process my OJT clearance and attendance.

                I've already attached the MOA document and filled out the necessary fields. Please let me know if you need anything else from my end.

                Thank you for your kind support!

                Best regards,
                Juan Dela Cruz
                BSCS Intern: 2024-2025
        """,
        "role": "assistant",
        "content": """
        {"urgency": "High"}
        """
    } 

    def __init__(self) -> None:
        self.client = Groq(
            api_key=os.environ.get("GROQ_API_KEY")
        )

    def get_response(self, prompt: str):
        response = self.client.chat.completions.create(
            # model="deepseek-r1-distill-llama-70b",
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": ArklineAI.SYSTEM_BASE_PROMPT},
                ArklineAI.BEHAVIOR_ONE_SHOT_MESSAGE, # type: ignore
                {"role": "user", "content": prompt}
            ],
        )
        raw = response.choices[0].message.content

        return extract_clean_json(raw) # type: ignore

if __name__ == "__main__":
    ai = ArklineAI()
    test_prompt = """
        Hi Ma'am/Sir,

        I hope you're doing well. I would like to request your assistance in signing my Memorandum of Agreement (MOA) as soon as possible. Our university requires it to be submitted by 3 PM today in order to process my OJT clearance and attendance.

        I've already attached the MOA document and filled out the necessary fields. Please let me know if you need anything else from my end.

        Thank you for your kind support!

        Best regards,
        Juan Dela Cruz
        BSCS Intern: 2024-2025
    """

    test_prompt1 = """
    Hello maam sir. I would like to to thank you again for your support!
    """
    response = ai.get_response(test_prompt)
    response1 = ai.get_response(test_prompt1)
    print(f"AI Response: {response}")
    print(type(response))
    print(f"AI Response 1: {response1}")