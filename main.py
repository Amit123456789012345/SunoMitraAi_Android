import os
import openai
import speech_recognition as sr
from gtts import gTTS
import requests
import datetime
import time

# ✅ OPENAI API KEY (पहले से डाली गई है)
openai.api_key = "sk-..."

# ✅ News API Key
news_api_key = "your_news_api_key"

# ✅ Weather API Key
weather_api_key = "your_openweather_api_key"

# ✅ Hindi में बोलने का function
def speak_hindi(text):
    print("सुनो मित्र:", text)
    tts = gTTS(text=text, lang='hi')
    tts.save("output.mp3")
    os.system("termux-media-player play output.mp3")

# ✅ Hindi में सुनने का function
def listen_hindi():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("आप बोलें...")
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language="hi-IN")
            print("आपने कहा:", query)
            return query.lower()
        except sr.UnknownValueError:
            speak_hindi("माफ कीजिए, मैं समझ नहीं पाया।")
            return ""
        except sr.RequestError:
            speak_hindi("नेटवर्क में दिक्कत है।")
            return ""

# ✅ ChatGPT से जवाब
def ask_chatgpt(question):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": question}]
    )
    answer = response['choices'][0]['message']['content']
    return answer

# ✅ Weather
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric&lang=hi"
    res = requests.get(url)
    data = res.json()
    if data.get("weather"):
        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        return f"{city} में अभी {weather} है और तापमान {temp}°C है।"
    else:
        return "मौसम जानकारी नहीं मिल पाई।"

# ✅ News
def get_news():
    url = f"https://newsapi.org/v2/top-headlines?country=in&language=hi&apiKey={news_api_key}"
    res = requests.get(url)
    articles = res.json().get("articles", [])[:3]
    headlines = [article["title"] for article in articles]
    return "आज की प्रमुख खबरें:\n" + "\n".join(headlines)

# ✅ रिमाइंडर सेट
reminders = []
def set_reminder(text):
    speak_hindi(f"रिमाइंडर सेट कर दिया गया: {text}")
    reminders.append(text)

# ✅ Placeholder features
def future_whatsapp():
    return "भविष्य में WhatsApp से जुड़ने का विकल्प होगा।"

def future_location():
    return "भविष्य में स्थान आधारित सुझाव दिए जाएंगे।"

# ✅ मुख्य function
def suno_mitra_ai():
    speak_hindi("नमस्ते! मैं सुनो मित्र, मैं एआई हूँ। कैसे मदद कर सकता हूँ?")
    while True:
        query = listen_hindi()

        if "बंद हो जाओ" in query:
            speak_hindi("ठीक है, अलविदा!")
            break
        elif "मौसम" in query:
            speak_hindi("किस शहर का मौसम जानना है?")
            city = listen_hindi()
            info = get_weather(city)
            speak_hindi(info)
        elif "खबर" in query:
            news = get_news()
            speak_hindi(news)
        elif "रिमाइंडर" in query:
            speak_hindi("किस चीज़ का रिमाइंडर सेट करना है?")
            note = listen_hindi()
            set_reminder(note)
        elif "व्हाट्सएप" in query:
            speak_hindi(future_whatsapp())
        elif "जगह" in query or "लोकेशन" in query:
            speak_hindi(future_location())
        else:
            answer = ask_chatgpt(query)
            speak_hindi(answer)

# ✅ प्रोग्राम शुरू करें
suno_mitra_ai()