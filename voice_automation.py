from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import speech_recognition as sr
import pyttsx3
# works only for english language


def get_google_result(browser, query):
    query.replace(' ','+')
    browser.get(url + query)
    data = browser.find_element_by_id('rhs_block').find_elements_by_tag_name('span')[6].text
    with open('result.txt', 'wb') as handle:
        handle.write(data.encode("UTF-8"))
    return data

def play_youtube(browser, video_name):
    browser.get('https://www.youtube.com/results?search_query='+video_name)
    time.sleep(1)
    browser.find_element_by_tag_name("ytd-video-renderer").click()


browser = webdriver.Chrome("./chromedriver")
browser.implicitly_wait(10)
url = 'https://www.google.com/search?q='
browser.get('https://www.google.com')
# change googles default search results language to english.
browser.find_element_by_xpath("//*[text()[contains(., 'English')]]").click() # to get english results
# initialize the text to speach object
engine = pyttsx3.init()
# initialize the speach recognizer
rec = sr.Recognizer()
listen = True
'''
say 'google', and search value.
the program will read loud the default result and save a text file of it.
say 'youtube', the program will ask you what video to search and play the first output.
say 'stop', and the program will close itself, and stop listening
'''
with sr.Microphone() as source:
    while listen:
        print("Speak Command")
        audio = rec.listen(source)
        try:
            type = rec.recognize_google(audio)
            if 'google' in type.lower():
                engine.say("how can I help you")
                engine.runAndWait()
                audio = rec.listen(source)
                query = rec.recognize_google(audio)
                print(f"Searching for {query}")
                data = get_google_result(browser, query)
                engine.say(data)
                engine.runAndWait()
            elif 'youtube' in type.lower():
                engine.say("what video to search")
                engine.runAndWait()
                audio = rec.listen(source)
                query = rec.recognize_google(audio)
                print(query)
                play_youtube(browser, query)
            elif 'stop' in type.lower():
                listen = False
                print("Stopped listening")
        except:
            print("couldn't recognize your voice")
#########################


browser.close()
