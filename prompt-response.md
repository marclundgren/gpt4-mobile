To achieve this, we'll create a simple Python Flask API backend, an SQLite database to store the prompts and responses, and a mobile-friendly HTML and JavaScript frontend.

1. First, create a new directory for your project and navigate to it:

```
mkdir gpt4_api
cd gpt4_api
```

2. Install Flask and create the `app.py` file:

```sh
pip install Flask
touch app.py
```

3. Inside `app.py`, create a simple Flask API with an SQLite database to store responses:

```python
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('responses.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS responses (id INTEGER PRIMARY KEY, prompt TEXT, response TEXT)''')
    conn.commit()
    conn.close()

@app.route('/prompt', methods=['POST'])
def prompt():
    data = request.json
    prompt_text = data['prompt']

    # Process the prompt with GPT-4 and get the response (Replace `gpt4_response` with actual GPT-4 API code)
    gpt4_response = f"Response for: {prompt_text}"

    conn = sqlite3.connect('responses.db')
    c = conn.cursor()
    c.execute("INSERT INTO responses (prompt, response) VALUES (?, ?)", (prompt_text, gpt4_response))
    conn.commit()
    conn.close()

    return jsonify({'response': gpt4_response})

@app.route('/responses', methods=['GET'])
def responses():
    conn = sqlite3.connect('responses.db')
    c = conn.cursor()
    c.execute("SELECT * FROM responses")
    data = [{'id': row[0], 'prompt': row[1], 'response': row[2]} for row in c.fetchall()]
    conn.close()

    return jsonify(data)

if __name__ == '__main__':
    init_db()
    app.run(host='localhost', port=8181)
```

4. Next, create the `index.html` and `style.css` file in a new folder called `static`:

```sh
mkdir static
touch static/index.html
touch static/style.css
```

5. Add the HTML and JS code for the frontend in `static/index.html`:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>GPT-4 API</title>
    <link rel="stylesheet" href="style.css" />
  </head>
  <body>
    <div class="container">
      <h1>GPT-4 API</h1>
      <textarea id="prompt" rows="5" placeholder="Enter your prompt"></textarea>
      <button id="submit">Submit</button>
      <div id="loader" hidden>Loading...</div>
      <div id="responses"></div>
    </div>
    <script>
      const submitButton = document.getElementById("submit");
      const promptTextArea = document.getElementById("prompt");
      const loader = document.getElementById("loader");
      const responsesDiv = document.getElementById("responses");

      async function getAllResponses() {
        const response = await fetch("/responses");
        if (!response.ok) {
          alert("Error getting responses");
          return;
        }
        const data = await response.json();
        data.forEach((d) => {
          addResponseToPage(d.prompt, d.response);
        });
      }

      function addResponseToPage(prompt, response) {
        const el = document.createElement("div");
        el.innerHTML = `<p>Prompt: ${prompt}</p><p>Response: ${response}</p>`;
        responsesDiv.appendChild(el);
        promptTextArea.value = "";
      }

      submitButton.addEventListener("click", async () => {
        const promptText = promptTextArea.value.trim();
        if (!promptText) {
          alert("Please enter a prompt");
          return;
        }
        submitButton.disabled = true;
        loader.hidden = false;

        const data = { prompt: promptText };
        const response = await fetch("/prompt", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(data),
        });

        if (!response.ok) {
          alert("Error submitting prompt");
          return;
        }

        const result = await response.json();
        addResponseToPage(promptText, result.response);
        loader.hidden = true;
        submitButton.disabled = false;
      });

      getAllResponses();
    </script>
  </body>
</html>
```

6. Add some basic styles for mobile-friendly design in `static/style.css`:

```css
body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
}

.container {
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
  padding: 15px;
}

h1 {
  text-align: center;
}

textarea {
  display: block;
  width: 100%;
  margin-bottom: 20px;
}

button {
  display: block;
  width: 100%;
  background-color: #007bff;
  color: white;
  font-size: 16px;
  padding: 10px;
  border: none;
  text-align: center;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}

button:disabled {
  background-color: #ccc;
}

#loader {
  display: block;
  width: 100%;
  text-align: center;
}
```

7. Finally, run the server:

```sh
python app.py
```

8. Visit `http://localhost:8181/static/index.html` to see the frontend and interact with the GPT-4 API.

With this setup, you can now enter prompts, send them to the Python Flask API, process the requests with GPT-4, and store the responses in an SQLite database. Visitors can see previous prompts and their responses.
