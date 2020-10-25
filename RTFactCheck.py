import json
import requests
from pocketsphinx import LiveSpeech
from gtts import gTTS 
from playsound import playsound


def SpeakTerms(phrase): 
    # Language in which you want to convert 
    language = 'en'
    myobj = gTTS(text=phrase, lang=language, slow=False) 
    myobj.save("response.mp3") 
    playsound("response.mp3")

def FactCheck(query):
    payload = {
    'key': 'your_key_goes_here',
    'query':query
    }
    url ='https://factchecktools.googleapis.com/v1alpha1/claims:search'
    response = requests.get(url,params=payload)
    if response.status_code == 200:
        result = json.loads(response.text)
        # Arbitrarily select 1
        try:
            topRating = result["claims"][0]
            # arbitrarily select top 1
            claimReview = topRating["claimReview"][0]["textualRating"]
            claimVal = "According to " + str(topRating["claimReview"][0]['publisher']['name'])+ " that claim is " + str(claimReview)
            return claimVal           
        except:
            print("No claim review field found.")
            return 0
    else:
        return 0
def EavesDrop():
    # Reading Microphone as source
    print("Listening...")
    review = 0
    for phrase in LiveSpeech(): 
        phrase = str(phrase)
        try:
            if len(phrase) > 12:
                print("Fact checking: " + phrase)
                review = FactCheck(phrase)
                
            # Arbitrarily short sentence
            if review != 0:
                review = review.lower()
                print(review)
                if phrase.find("the earth is flat") != -1:
                    SpeakTerms("Everyone in this room is now dumber for having listened to your claim. I award you no points, and may God have mercy on your soul.")
                else:
                    SpeakTerms(review)
                review = 0
        except Exception as e:
            print(e)
# Some confirmed behaviors
def TestFactCheck():
    # Peculiarites
    FactCheck("Trump is making money off covid coins.")
    FactCheck("The earth is flat.")
    # More authentic sounding falsities
    FactCheck("An AP photograph shows Senate Majority Leader Mitch McConnell's hands looking bruised and discolored.")
    FactCheck("Telugu has now been recognised as an official language in the United States.")
EavesDrop()
