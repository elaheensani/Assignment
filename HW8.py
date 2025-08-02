# openai library must be installed already
from openai import OpenAI

# WARNING: Never hardcode your API key in production code
OPENAI_API_KEY = "aa-VIYcdCWFZTHh6GlKSVnyDRmOEjiJWfhDGb6HtCOSTEdQDGVP"

# AvalAI base URL
AVALAI_BASE_URL = "https://api.avalai.ir/v1"

# Create OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY, base_url=AVALAI_BASE_URL)

# Get user-defined tone
tone = input("Enter the tone for the conversation (e.g., sarcastically, cheerfully, angrily): ")

# Validate tone input
if not tone.strip():
    print("Error: Tone cannot be empty.")
    exit()

# Initialize conversation history with system prompt
prompts = [
    {
        'role': 'system',
        'content': [
            {'type': 'text', 'text': f"Respond {tone}!"}
        ]
    }
]

# Words that end the conversation
EXIT_WORDS = {"quit", "exit", "stop"}

# Main conversation loop
while True:
    user_message = input("\nEnter your message (or 'quit', 'exit', or 'stop' to end): ")

    # Exit condition
    if user_message.lower() in EXIT_WORDS:
        print("Ending conversation.")
        break

    # Validate message
    if not user_message.strip():
        print("Error: Message cannot be empty.")
        continue

    # Append user message to prompt history
    prompts.append({
        'role': 'user',
        'content': [
            {'type': 'text', 'text': user_message}
        ]
    })

    try:
        # Send request to AvalAI API
        response_obj = client.chat.completions.create(
            model="GPT-4.1-nano",
            messages=prompts
        )

        # Extract AI response
        response = response_obj.choices[0].message.content[0].text

        print(f"\nAI Response ({tone}): {response}")

        # Append AI response to conversation history
        prompts.append({
            'role': 'assistant',
            'content': [
                {'type': 'text', 'text': response}
            ]
        })

        # Print the full conversation history
        print("\n--- Conversation History ---")
        for message in prompts:
            role = message['role'].capitalize()
            for part in message['content']:
                if part['type'] == 'text':
                    print(f"{role}: {part['text']}")
        print("----------------------------")

    except Exception as e:
        print(f"An error occurred: {e}")
