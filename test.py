from google import genai

client = genai.Client(api_key="AIzaSyD2LjQz6nPpm0So3TDWtnwRDwf7TlafLZk")

for m in client.models.list():
    print(m.name)