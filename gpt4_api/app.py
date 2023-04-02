from flask import Flask, request, jsonify
import openai
import sqlite3

# Function that calls the GPT-4 API
def ask_gpt4(system_intel:str, prompt:str): 
  """
  > `ask_gpt4` takes in a system intel and a prompt, and returns the response from GPT-4
  
  :param system_intel: This is the system's intelligence. It's the information that the system has
  about the user
  :param prompt: the prompt to ask the model
  :return: A string of text.
  """
  result = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
      {"role": "system", "content": system_intel},
      {"role": "user", "content": prompt}
    ]
  )

  # print the result
  print(result['choices'][0]['message']['content'])

  return result['choices'][0]['message']['content']

app = Flask(__name__)

# define a constant for 'responses.db'
DB_NAME = 'responses.db'

system_intel = "You are GPT-4, answer my questions as if you were an expert in the field."

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS responses (id INTEGER PRIMARY KEY, prompt TEXT, response TEXT)''')
    conn.commit()
    conn.close()

@app.route('/prompt', methods=['POST'])
def prompt():
    data = request.json
    # print the data
    print(data)

    prompt_text:str = data['prompt']
    # print the prompt
    print(prompt_text)

    gpt4_response = ask_gpt4(system_intel, prompt_text)

    # print the response
    print(gpt4_response)

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO responses (prompt, response) VALUES (?, ?)", (prompt_text, gpt4_response))
    conn.commit()
    conn.close()
    # connection closed
    print('connection closed')

    return jsonify({'response': gpt4_response})

@app.route('/responses', methods=['GET'])
def responses():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM responses")
    data = [{'id': row[0], 'prompt': row[1], 'response': row[2]} for row in c.fetchall()]
    conn.close()

    return jsonify(data)

if __name__ == '__main__':
    init_db()
    app.run(host='localhost', port=8181)