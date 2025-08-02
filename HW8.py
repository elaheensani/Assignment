
from openai import OpenAI


OPENAI_API_KEY = "aa-VIYcdCWFZTHh6GlKSVnyDRmOEjiJWfhDGb6HtCOSTEdQDGVP"


AVALAI_BASE_URL = "https://api.avalai.ir/v1"


client = OpenAI(api_key=OPENAI_API_KEY, base_url=AVALAI_BASE_URL)


tone = input("Enter the tone for the conversation (e.g., sarcastically, cheerfully, angrily): ")


if not tone.strip():
    print("Error: Tone cannot be empty.")
    exit()


prompts = [
    {
        'role': 'system',
        'content': [
            {'type': 'text', 'text': f"Respond {tone}!"}
        ]
    }
]


EXIT_WORDS = {"quit", "exit", "stop"}


while True:
    user_message = input("\nEnter your message (or 'quit', 'exit', or 'stop' to end): ")

 
    if user_message.lower() in EXIT_WORDS:
        print("Ending conversation.")
        break

   
    if not user_message.strip():
        print("Error: Message cannot be empty.")
        continue

   
    prompts.append({
        'role': 'user',
        'content': [
            {'type': 'text', 'text': user_message}
        ]
    })

    try:
       
        response_obj = client.chat.completions.create(
            model="GPT-4.1-nano",
            messages=prompts
        )

        
        response = response_obj.choices[0].message.content[0].text

        print(f"\nAI Response ({tone}): {response}")

       
        prompts.append({
            'role': 'assistant',
            'content': [
                {'type': 'text', 'text': response}
            ]
        })

        
        print("\n--- Conversation History ---")
        for message in prompts:
            role = message['role'].capitalize()
            for part in message['content']:
                if part['type'] == 'text':
                    print(f"{role}: {part['text']}")
        print("----------------------------")

    except Exception as e:
        print(f"An error occurred: {e}")
