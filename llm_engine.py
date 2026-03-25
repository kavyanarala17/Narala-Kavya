from openai import OpenAI

client = OpenAI(
    api_key="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",
    base_url="https://openrouter.ai/api/v1"
)

def call_model(model_name, question):
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "user", "content": question}
            ]
        )
        return response.choices[0].message.content

    except Exception as e:
        return "Model not available"


def get_llm_responses(question):

    responses = {
        "GPT-3.5": call_model("openai/gpt-3.5-turbo", question),
        "GPT-4o-mini": call_model("openai/gpt-4o-mini", question),
        "DeepSeek": call_model("deepseek/deepseek-chat", question),
        "Claude": call_model("anthropic/claude-3-haiku", question),
        "Mixtral": call_model("mistralai/mixtral-8x7b-instruct", question)
    }

    return responses