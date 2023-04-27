from flask import Flask, render_template, request, redirect, url_for, jsonify
import pandas as pd
import numpy as np
from selenium import webdriver
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from firebase_admin import credentials, storage
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import pandas as pd
from tqdm import tqdm
import string
import random
import os
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from threading import Thread
import cv2
from datetime import datetime
from moviepy.editor import *


package_dir = os.path.dirname(
    os.path.abspath(__file__)
)
static = os.path.join(
    package_dir, "static"
)

cred = credentials.Certificate('firebase.json')
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': "Your DB URL",
    'storageBucket': 'Your Storage URL'
})

# Define the scope and credentials to access the Google Sheet API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(
    'service.json', scope)
client = gspread.authorize(creds)

finished = False
df = pd.DataFrame()
th = Thread()
availa = 0

def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""

def gif_gen(url, key):
    chrome = webdriver.ChromeOptions()
    chrome.add_argument('--headless')
    chrome.add_argument('--no-sandbox')
    chrome.add_argument('--disable-dev-shm-usage')
    chrome.add_argument('--disable-gpu')
    chrome.add_argument('---window-size=1920,980')
    dr = webdriver.Chrome(
        executable_path="/usr/bin/chromedriver", options=chrome)
    """dr = webdriver.Chrome(
        executable_path="chromedriver.exe", options=chrome)"""
    # Set the dimensions of the webpage
    width = 1920
    height = 980
    fsize = (width, height)
    # Navigate to the webpage
    wait = WebDriverWait(dr, 30)
    dr.get(url)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(5)
    # Set up the file path for the video file
    video_path = f'.{key}_vid.avi'
    
    # Set up the codec and frames per second for the video
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    fps = 7
    
    # Create a new video writer object
    out = cv2.VideoWriter(video_path, fourcc, fps, fsize)
    
    # Set up the time limit for the recording
    time_limit = 10  # in seconds
    
    # Start the recording
    start_time = time.time()
    while (time.time() - start_time) < time_limit:
        # Take a screenshot of the webpage
        dr.find_element_by_tag_name('body').screenshot(f'.{key}_out.png')
        img = cv2.imread(f'.{key}_out.png')
        img = cv2.resize(img, fsize)
        # Write the frame to the video
        out.write(img)
    
    # Release the video writer and the driver
    out.release()
    
    # Load the video file
    video = VideoFileClip(video_path)
    
    # Set the path of the output GIF file
    gif_path = f'.{key}_gif.gif'
    
    # Create the GIF file
    video.write_gif(gif_path)

    fileName = f'.{key}_gif.gif'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)
    blob.make_public()
    gif_url = blob.public_url
    return gif_url

def S(X): return driver.execute_script(
    'return document.body.parentNode.scroll' + X)


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(
    executable_path="/usr/bin/chromedriver", options=chrome_options)

"""driver = webdriver.Chrome(
    executable_path="chromedriver.exe", options=chrome_options)"""

app = Flask(__name__)

def task():
    global df
    global client
    # Open the Google Sheet by its name
    sheet_name = 'Store Sheet ID'
    sheet = client.open_by_key(sheet_name).worksheet('Sheet1')
    dfx = df.copy()
    # create a new column with timestamps
    dfx.insert(0, 'Timestamp', str(datetime.now().date()))
    # Append the data to the Google Sheet
    data = dfx.values.tolist()
    sheet.append_rows(data)

    url1 = df['URL_1'].tolist()
    url2 = df['URL_2'].tolist()
    url3 = df['URL_3'].tolist()
    url4 = df['URL_4'].tolist()
    url5 = df['URL_5'].tolist()
    link = df['G_Video'].tolist()
    fn = df['First_Name'].tolist()
    ln = df['Last_Name'].tolist()
    temp = df['template_id'].tolist()
    links = []
    embed = []
    gif = []
    for i in tqdm(range(len(url1))):
        vid_link1 = ""
        vid_link2 = ""
        vid_link3 = ""
        vid_link4 = ""
        vid_link5 = ""
        key = np.nan
        try:
           driver.get(url1[i])
           time.sleep(2)
           driver.set_window_size(S('Width'), S('Height'))
           key = ''.join(random.choices(string.ascii_uppercase +
                                        string.digits, k=16))
           driver.find_element_by_tag_name('body').screenshot(f'.{key}.png')
           fileName = f'.{key}.png'
           bucket = storage.bucket()
           blob = bucket.blob(fileName)
           blob.upload_from_filename(fileName)
           blob.make_public()
           vid_link1 = blob.public_url
        except:
            pass
        if url2[i] != 'None':
            try:
                driver.get(url2[i])
                time.sleep(2)

                driver.set_window_size(S('Width'), S('Height'))
                driver.find_element_by_tag_name(
                    'body').screenshot(f'.{key}_1.png')
                fileName = f'.{key}_1.png'
                bucket = storage.bucket()
                blob1 = bucket.blob(fileName)
                blob1.upload_from_filename(fileName)
                blob1.make_public()
                vid_link2 = blob1.public_url
            except:
                pass
        if url3[i] != 'None':
            try:
                driver.get(url3[i])
                time.sleep(2)

                driver.set_window_size(S('Width'), S('Height'))
                driver.find_element_by_tag_name(
                    'body').screenshot(f'.{key}_2.png')
                fileName = f'.{key}_2.png'
                bucket = storage.bucket()
                blob2 = bucket.blob(fileName)
                blob2.upload_from_filename(fileName)
                blob2.make_public()
                vid_link3 = blob2.public_url
            except:
                pass

        if url4[i] != 'None':
            try:
               driver.get(url4[i])
               time.sleep(2)

               driver.set_window_size(S('Width'), S('Height'))
               driver.find_element_by_tag_name(
                   'body').screenshot(f'.{key}_3.png')
               fileName = f'.{key}_3.png'
               bucket = storage.bucket()
               blob3 = bucket.blob(fileName)
               blob3.upload_from_filename(fileName)
               blob3.make_public()
               vid_link4 = blob3.public_url
            except:
                pass

        if url5[i] != 'None':
            try:
                driver.get(url5[i])
                time.sleep(2)
                driver.set_window_size(S('Width'), S('Height'))
                driver.find_element_by_tag_name(
                    'body').screenshot(f'.{key}_4.png')
                fileName = f'.{key}_4.png'
                bucket = storage.bucket()
                blob4 = bucket.blob(fileName)
                blob4.upload_from_filename(fileName)
                blob4.make_public()
                vid_link5 = blob4.public_url
            except:
                pass

        nlink = f'https://drive.google.com/uc?export=download&id={find_between( link[i], "/file/d/", "/view" )}'
        json = {
            'vid1': vid_link1,
            'vid2': vid_link2,
            'vid3': vid_link3,
            'vid4': vid_link4,
            'vid5': vid_link5,
            'corner': nlink,
            'fname': fn[i],
            'lname': ln[i]
        }
        ref = db.reference(f"/video/{temp[0]}/{key}")
        ref.set(json)
        links.append(
            f'https://opentotalk.org/video?name={fn[i]}_{ln[i]}&video={key}&template={temp[0]}/')
        gif.append(gif_gen(
            f'https://opentotalk.org/iframe/?name={fn[i]}_{ln[i]}&video={key}&template={temp[0]}', f'{key}'))
        embed.append(
            f'<iframe src="https://opentotalk.org/iframe/?name={fn[i]}_{ln[i]}&video={key}&template={temp[0]}/" style="border:0px #ffffff none;" name="VidServer" scrolling="no" frameborder="1" marginheight="0px" marginwidth="0px" height="200px" width="300px" allowfullscreen></iframe>')
    df['uplink'] = links
    df['gif'] = gif
    df['embed'] = embed
    my_dir = './'
    for fname in os.listdir(my_dir):
        if fname.endswith(".png") or fname.endswith(".avi") or fname.endswith(".gif") and fname.startswith(".dist") == False:
            os.remove(os.path.join(my_dir, fname))
    df = df[['from', 'name', 'First_Name', 'Last_Name', 'Mobile', 'Email', 'uplink', 'gif', 'embed']]
    df['Done'] = 0
    # Open the Google Sheet by its name
    sheet_name = 'Resutl Sheet ID'
    sheet = client.open_by_key(sheet_name).worksheet('Sheet1')
    dfx = df.copy()
    # create a new column with timestamps
    dfx.insert(0, 'Timestamp', str(datetime.now().date()))
    # Append the data to the Google Sheet
    data = dfx.values.tolist()
    sheet.append_rows(data)
    global availa
    ref = db.reference(f"/credit/{temp[0]}/used")
    data = availa + len(df)
    ref.set(data)
    global finished
    finished = True
    

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/result')
def result():
    global df
    return render_template('upload.html', data=df.to_html(render_links=True, escape=False))


@app.route('/status')
def thread_status():
    """ Return the status of the worker thread """
    return jsonify(dict(status=('finished' if finished else 'running')))


@app.route('/upload', methods=['GET'])
def upload():
    file = request.args.get('file')
    token = request.args.get('token')
    avail = request.args.get('avil')
    sentMail = request.args.get('email')
    temp = request.args.get('temp')
    nam = request.args.get('Name')
    used = int(request.args.get('utok')) / 9988770
    avail = int(avail)/887656678
    acurl = f'{file}&token={token}'
    acurl = acurl.replace('Excels/', 'Excels%2F')
    print(acurl)
    global df
    try:
        df = pd.read_excel(acurl)
        df['template_id'] = temp
        df['from'] = sentMail
        df['name'] = nam
    except:
        pass
    if len(df) > avail or acurl.find('https://firebasestorage.googleapis.com/v0/b/vidshare-1.appspot.com/o/Excels') == -1:
        message = ''
        return render_template('alert.html', message=message)
    else:   
        global th
        global finished
        global availa
        availa = used
        finished = False
        th = Thread(target=task, args=())
        th.start()
        return render_template('numba.html')
    

if __name__ == '__main__':
    app.run(debug=False, port=5001, host="0.0.0.0")
