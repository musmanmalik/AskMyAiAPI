import os
import openai

openai.api_key = os.environ.get("OPENAI_API_KEY")


def openai_api(text):
    prompt = "Answer the question as truthfully as possible using the Context, and if the answer is not " \
             "contained within the text below, say 'Sorry, can't " \
             "answer right now.' Use date of birth or born date while telling age."
    # prompt = "Answer the question from provided Context otherwise say " \
    #          "'Sorry, can't answer right now.'.\n\n"
    response = openai.Completion.create(
      engine="text-davinci-003",
      prompt=prompt + text,
      temperature=0.40,
      max_tokens=1000,
      top_p=1.0,
      frequency_penalty=0,
      presence_penalty=0
    )
    return response['choices'][0]['text'], response['usage']['total_tokens']
