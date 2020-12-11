


import tkinter as tk
import time
import os
from keras.models import load_model
from time import sleep
from keras.preprocessing.image import img_to_array 
from keras.preprocessing import image
import cv2
import numpy as np 
from tkinter import ttk
import os
import pygame
import time


start_pause_var = 0
music_quee = 0
songs = os.listdir()
res = [x for x in songs if ".mp3" in x]
index = songs.index(res[music_quee])
counter = 0
labels = []
def open_camera():
    global name
    global final_emotion
    # name = tk.simpledialog.askstring('Name', "Let's start with your name")
    face_classifier = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')
    classifier =load_model('./Emotion_Detection.h5')
    
    class_labels = ['Angry','Happy','Neutral','Sad','Shocked']
    
    cap = cv2.VideoCapture(0)   
    while True:
        ret, frame = cap.read()
        
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray,1.3,5)
        for (x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h,x:x+w]
            roi_gray = cv2.resize(roi_gray,(48,48),interpolation=cv2.INTER_AREA)
            if np.sum([roi_gray])!=0:
                roi = roi_gray.astype('float')/255.0
                roi = img_to_array(roi)
                roi = np.expand_dims(roi,axis=0)   
                preds = classifier.predict(roi)[0]
                label=class_labels[preds.argmax()]
                label_position = (x,y)
                cv2.putText(frame,label,label_position,cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,0),3)
                labels.append(label)
                print(labels)
               
            
            else:
                cv2.putText(frame,'No Face Found',(20,60),cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,0),3)
            print("\n\n")       
        cv2.imshow('Emotion Detector',frame)
        if cv2.waitKey(1) & 0xFF == ord(' '):
            break
            
           
    final_emotion=max(set(labels), key=labels.count)
   
    cap.release()
    cv2.destroyAllWindows()
    print(choosing_song())
    music_player()
    
def music_player():
    music_root = tk.Tk()
    music_root.geometry("500x500")
    global music_quee
    music_quee = 1
    
    frameCnt =4
    frames = [tk.PhotoImage(file='D:/Profile/Desktop/Programming in general/ML/wavess.gif',format = 'gif -index %i' %(i)) for i in range(frameCnt)]
    def update(ind):
        frame = frames[ind]
        ind += 1
        if ind == frameCnt:
            ind = 0
        label.configure(image=frame)
        music_root.after(90, update, ind)
    
    
    lower_frame=tk.Text(music_root,bg="#000000")
    lower_frame.place(relx=0.5,rely=0.4,relwidth=0.3,relheight=0.3,anchor="n")
    
    label = ttk.Label(music_root)
    label.place(relx=0.5,rely=0.4,relwidth=0.3,relheight=0.3,anchor="n")
    music_root.after(0, update, 0)
    
    style = ttk.Style(music_root)
    music_root.tk.eval("""
    set base_theme_dir D:/Profile/Desktop/awthemes-9.5.0
    
    package ifneeded awthemes 9.5.0 \
        [list source [file join $base_theme_dir awthemes.tcl]]
    package ifneeded colorutils 4.8 \
        [list source [file join $base_theme_dir colorutils.tcl]]
    package ifneeded awdark 7.9 \
        [list source [file join $base_theme_dir awdark.tcl]]
    package ifneeded awlight 7.6 \
        [list source [file join $base_theme_dir awlight.tcl]]
    """)
    music_root.tk.call("package", "require", 'awdark')
    music_root.tk.call("package", "require", 'awlight')
    style.theme_use('awdark')
    pygame.mixer.init()
        
    def start_and_stop_the_music ():
        global start_pause_var
        global music_label
        global final_list
        songs = os.listdir()
        final_list= []
        indexes = []
        res = [x for x in songs if ".mp3" in x]
        recommended_songs = choosing_song()
        for x in recommended_songs:
            if x in res:
                final_list.append(x)
        for ele in final_list:
            index = songs.index(ele)
            indexes.append(index)
        start_pause_var+=1
        if start_pause_var == 1:
            music_label = ttk.Label(music_root,text= songs[indexes[0]])
            music_label.pack()
            pygame.mixer.music.load(songs[indexes[0]])
            pygame.mixer.music.play(0)
            print("music started")
        elif start_pause_var % 2 !=0:
            pygame.mixer.music.unpause()
            print("countinue")
    def stop_music():
        global start_pause_var 
        start_pause_var+=1
        if start_pause_var %2 == 0:
            pygame.mixer.music.pause()
    def next_song ():
        global music_quee
        global music_label
        global final_list 
        songs = os.listdir()
        music_root.after(0,music_label.destroy)
        res = [x for x in songs if ".mp3" in x]
        indexes= []
        recommended_songs = choosing_song()
        for x in recommended_songs:
            if x in res:
                final_list.append(x)
        for ele in final_list:
            index = songs.index(ele)
            indexes.append(index)
        
        if music_quee == 0: 
            music_label = ttk.Label(music_root,text= songs[index])
            music_label.pack()
            music_root.after(0,music_label.destroy) 
            print(index)
            music_quee+=1
            index = songs.index(final_list[music_quee])
            music_label = ttk.Label(music_root,text= songs[index])
            music_label.pack()
            pygame.mixer.music.load(songs[index])
            pygame.mixer.music.play(0)  
        else:
            try:
                music_quee+=1
                music_root.after(0,music_label.destroy) 
                index = songs.index(final_list[music_quee])
                music_label = ttk.Label(music_root,text= songs[index])
                music_label.pack()
                print(index)
                pygame.mixer.music.load(songs[index])
                pygame.mixer.music.play(0)
            except IndexError:
                error_label = ttk.Label(music_root,text='Sorry it looks like this is the last song buy you can still listen the previous ones')
                error_label.pack()
                music_root.after(10000,error_label.destroy)
    def previous_song ():
        global music_quee
        global music_label
        music_root.after(0,music_label.destroy)
        songs = os.listdir()
        res = [x for x in songs if ".mp3" in x] 
        indexes= []
        recommended_songs = choosing_song()
        for x in recommended_songs:
            if x in res:
                final_list.append(x)
        for ele in final_list:
            index = songs.index(ele)
            indexes.append(index)
        index = songs.index(final_list[music_quee-1])
        music_label = ttk.Label(music_root,text= songs[index])
        music_label.pack()
        pygame.mixer.music.load(songs[index])
        pygame.mixer.music.play(0)
        music_quee-=1
    
    
    
    
          
    l1=ttk.Label(music_root,text="MUSIC PLAYER",font="times 20")
    l1.pack()
    
    button_start=ttk.Button(music_root,text="Play",command=start_and_stop_the_music)
    button_start.place(x=1,y=7,relx=0.32,rely=0.12)
    
    button_stop = ttk.Button(music_root,text="Pause",command = stop_music).place(x=1,y=7,relx=0.5,rely=0.12)
    
    button_next = ttk.Button(music_root,text="Next Song",command = next_song).place(x=1,y=7,relx=0.7,rely=0.12)
    button_previous = ttk.Button(music_root,text="Previous Song",command = previous_song).place(x=1,y=7,relx=0.1,rely=0.12)
    
    
    
    
    style = ttk.Style()
    style.configure("BW.TLabel", foreground="black", background="white")
    music_root.configure(bg=style.lookup('TFrame', 'background'))
    
    
        
    
    
    
    
    
    music_root.mainloop()
def choosing_song():
    global final_emotion
    status_happy= ["Marie Laforêt - Je suis folle de vous (1968).mp3","Tim Mcmorris - Its a beautiful day.mp3","American Authors - Best Day Of My Life (Official Video).mp3"]
    status_sad = ["Marie Laforet - Viens Viens.mp3","Alec Benjamin - Let Me Down Slowly [Official Music Video].mp3"]
    status_neutral = ["Sting - Englishman In New York (Official Music Video).mp3","The Kooks - Sofa Song.mp3"]
    if final_emotion == 'Happy':
        return status_happy
    elif final_emotion == 'Sad':
        return status_sad
    elif final_emotion == 'Neutral':
        return status_neutral
    
    
    
    
    
    
    
    
    
def main():
    root = tk.Tk()
    root.wm_title('Music Program')
    root.geometry("900x500")
    style = ttk.Style(root)
    root.tk.eval("""
set base_theme_dir D:/Profile/Desktop/awthemes-9.5.0

package ifneeded awthemes 9.5.0 \
    [list source [file join $base_theme_dir awthemes.tcl]]
package ifneeded colorutils 4.8 \
    [list source [file join $base_theme_dir colorutils.tcl]]
package ifneeded awdark 7.9 \
    [list source [file join $base_theme_dir awdark.tcl]]
package ifneeded awlight 7.6 \
    [list source [file join $base_theme_dir awlight.tcl]]
""")
    root.tk.call("package", "require", 'awdark')
    root.tk.call("package", "require", 'awlight')
    style.theme_use('awdark')
    frameCnt = 12
    frames = [tk.PhotoImage(file='tenor.gif',format = 'gif -index %i' %(i)) for i in range(frameCnt)]
    def update(ind):
        frame = frames[ind]
        ind += 1
        if ind == frameCnt:
            ind = 0
        label.configure(image=frame)
        root.after(90, update, ind)
    start_button = ttk.Button(text="Let's Start",command=open_camera)
    start_button.pack()
    upper_frame=tk.Text(root,bg="#ECECF2",bd=5)
    upper_frame.place(relx=0.5,rely=0.1,relwidth=0.5,relheight=0.5,anchor="n")
    label_main = tk.Label(upper_frame,text="This program detecs your current mood \n via your webcam and recommends you a playlist \n based on your facial expression\n besides that you can see your predicted emotions via your webcam")
    label_main.pack()
    lower_frame=tk.Text(root,bg="#ECECF2")
    lower_frame.place(relx=0.5,rely=0.4,relwidth=0.5,relheight=0.5,anchor="n")
    
    label = ttk.Label(lower_frame)
    label.pack()
    root.after(0, update, 0)
    style = ttk.Style()
    style.configure("BW.TLabel", foreground="black", background="white")
    root.configure(bg=style.lookup('TFrame', 'background'))
    root.mainloop()
    
    
    
main()
