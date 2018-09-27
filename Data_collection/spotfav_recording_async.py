
# This file runs a pipline command for a windows(!!!) command line using subprocess module. The aim of this command is to capture
# video files from the webcams streaming video to the internet. The video clips of duration 30 sec are captured every 5 min (300sec)
# from 5 different webcams and are saved into newly created directory (name_of_directory=location_name). The video clips are only recorded
# between 10am and 7pm. To run this script you need a presence of AdobeHDS.php file in the same directory and PHP installed on your system


import subprocess
import datetime
import time

def record(location,duration=10):

    #Create filename in format 'year-month-day-hour-minute' easy to parse later
    
    directory='../Data_samples/train data/'+location
    
    filename = '"{}-{}-{}"'.format(datetime.datetime.today().date(),datetime.datetime.today().hour,
                                     datetime.datetime.today().minute)
    # creates windows cmd command to start video parser AdobeHDS, that will save video into file in derectory 'location'
    command = (r'php AdobeHDS.php --manifest "https://flus0.spotfav.com/'+ location +'/manifest.f4m" --delete'
            ' --outdir "' + directory + '" --outfile ' + filename + ' --duration '+ str(duration))

    #send the comand for execution, wait 2 second for the response. If there is no response in 5 sec recording is probably started

    try:
        out=subprocess.Popen(command,stdout=subprocess.PIPE).communicate(timeout=5)
    except:
        out=0

    #handels the output messages of Popen (if any) and prints what's going on

    try:
        if out[0].splitlines()[-1]==b'Unable to download the manifest':
            print('webcam on {} is down'.format(location))
        else:
            print(out)
    except:
        if out==0:
            print('recording on {}'.format(location))
        else:
            print(out)



#list of locations
locations=['valdevaqueros-tangana','ion-club-valdevaqueros']#,'zahara-atunes','balneario' 'arte-vida',


#the loop through locations to record video in all of them with duration of video in seconds (10second by default)
step=300 #how many seconds to wait between the cycles of recordings
while True:
    if datetime.datetime.today().hour>=10 and datetime.datetime.today().hour<19:
        try:
            for loc in locations:
                record(loc,duration=30)
        except KeyboardInterrupt:
            break
    else:
        hour=datetime.datetime.today().hour
        time_to_start=(hour>10)*24+10-hour
        print('paused for {} hours'.format(time_to_start))
        time.sleep(time_to_start*3600)
    print('paused for {} seconds'.format(step))
    time.sleep(step)
