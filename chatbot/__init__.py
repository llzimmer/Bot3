
import openai
import os
import logging
import azure.functions as func

openai.api_key = os.getenv("OPENAI_API_KEY")

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Recebendo requisição do Twilio.')

    user_msg = req.form.get('Body')
    phone_number = req.form.get('From')

    if not user_msg:
        return func.HttpResponse("Mensagem vazia.", status_code=400)

    try:
        # Enviar para OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um assistente educado e útil."},
                {"role": "user", "content": user_msg}
            ]
        )

        reply = response['choices'][0]['message']['content']

        return func.HttpResponse(f"<Response><Message>{reply}</Message></Response>",
                                 mimetype="application/xml")
    except Exception as e:
        logging.error(f"Erro ao processar: {str(e)}")
        return func.HttpResponse("Erro interno.", status_code=500)
