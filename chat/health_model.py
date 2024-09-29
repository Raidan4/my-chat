import google.generativeai as genai

# Google Generative AI Setup
genai.configure(api_key="AIzaSyA7XR0xvaEQpoug-79ri773lCYXNcR2WlI")

# Generation Configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Initialize the Model
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    system_instruction=(
        "انت نموذج ذكاء اصطناعي يهتم فقط بالجانب الطبي واعطاء المعلومات والاجابة "
        "عن الاسئلة التي في الجانب الطبي وعن الشخصيات المتعلقة بالمجال الطبي واي معلومة تختص بنفس المجال "
        "اذا كان هناك سؤال خارج هذا المجال عليك ان تجيبه برسالة "
        "'انا اسف لا يمكنني التحدث في مجال اخر. هل تريد المساعدة في الجانب الطبي؟ "
        "لا تتردد في السؤال.'"
    ),
)

# Start a Chat Session
def start_chat():
    return model.start_chat(history=[])

# Function to Send Message
def send_message(chat_session, question):
    try:
        response = chat_session.send_message(question)
        return response.text
    except Exception as e:
        return f"⚠️ حدث خطأ أثناء استرجاع الإجابة: {str(e)}"