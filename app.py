import sys
import openai
import os
from IPython.display import Markdown
from IPython.display import display
import config

openai.api_key = config.api_key

system_intel = "You are GPT-4, answer my questions as if you were an expert in the field."
prompt = """Three user inputs: a URL, and number of minutes and number of seconds. Write a Google Chrome extension that will open a URL, only after the provided time (minutes and seconds) has passed. The extension should be able to be used on any website

for the manifest.json file, use version 3.

If a url domain name was provided, the extension should open the url in a new tab. Automatically append https:// to the url if it is not already there.

Once the url is opened, the extension should close the tab.

Provide a start button and a cancel button.

When the countdown timer is active, Provide a countdown timer that counts down from the number of minutes and seconds provided by the user. The time should be displayed in the format: mm:ss

Once the Start button is clicked, disable the start button and all inputs.

Once the Cancel button is clicked, enable the start button and all inputs and disable the cancel button.

The start button is only enabled if a valid url and there is a valid time delay (minutes and seconds) Note minutes and seconds are both optional, but at least one of them must have a valid value for the delay to be considered valid. The domain name should be validated using a regex.

If the cancel is button is clicked, the timer should stop.

Once the timer is done, the extension should open the provided url in a new tab.
"""

# optional prompt.txt
if os.path.exists('prompt.txt'):
  with open('prompt.txt') as f:
    prompt = f.read()

# optional cli parameter
prompt = sys.argv[1] if len(sys.argv) > 1 else prompt

# Function that calls the GPT-4 API
def ask_gpt4(system_intel, prompt): 
  result = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
      {"role": "system", "content": system_intel},
      {"role": "user", "content": prompt}
    ]
  )

  # print the result
  print(result['choices'][0]['message']['content'])
  # Display the result
  # display(Markdown(result['choices'][0]['message']['content']))

  return result['choices'][0]['message']['content']

# Call the function above
ask_gpt4(system_intel, prompt)