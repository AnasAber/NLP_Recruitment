"""
Initialization of all project's models

"""

import os

from groq import Groq

client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)


def groq_query(prompt):

    chat_completion = client.chat.completions.create(
        #
        # Required parameters
        #
        messages=[{"role": "user", "content": prompt}],
        # The language model which will generate the completion.
        model="llama3-70b-8192",
        #
        # Optional parameters
        #
        # Controls randomness: lowering results in less random completions.
        # As the temperature approaches zero, the model will become deterministic
        # and repetitive.
        temperature=0,
        # The maximum number of tokens to generate. Requests can use up to
        # 2048 tokens shared between prompt and completion.
        max_tokens=1024,
        # Controls diversity via nucleus sampling: 0.5 means half of all
        # likelihood-weighted options are considered.
        top_p=1,
        # A stop sequence is a predefined or user-specified text string that
        # signals an AI to stop generating content, ensuring its responses
        # remain focused and concise. Examples include punctuation marks and
        # markers like "[end]".
        stop=None,
        # If set, partial message deltas will be sent.
        stream=False,
    )

    response = chat_completion.choices[0].message.content
    return response


def llama_query():
    pass
