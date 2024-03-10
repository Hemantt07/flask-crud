from flask import request, render_template, jsonify
from application import app
from openai import OpenAI

client = OpenAI(api_key='OPEN_AI_KEY')

@app.route( '/generate_text', methods=['POST', 'GET'] )
def generate_text_withai():
    if request.method == "POST":
        prompt = request.form.get( 'prompt' )
        response = client.chat.completions.create(
            model = "gpt-3.5-turbo",
            messages = [{"role": "user", "content": prompt}],
            max_tokens = 50
        )
        generated_text = response.choices[0]
        return jsonify({'generated_text': generated_text.message.content})
    else:
        pass
    return render_template( 'ai_form.html' )