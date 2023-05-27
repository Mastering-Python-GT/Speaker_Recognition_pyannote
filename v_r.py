from tkinter import filedialog
from scipy.spatial.distance import pdist
from pyannote.audio import Inference
from pyannote.audio import Model
import customtkinter

# create your own database in my case i used this records for testing the speaker recognition application

dataset = {"1": "elon musk", "2": "sam altman", "3": "kanye west", "4": "stephen wolfram", "5": "liv boeree",
           "6": "anna frebel", "7": "simone giertz", "8": "shannon curry", "9": "ginni rometty",
           "10": "manolis kellis", "11": "paul rosolie", "12": "robert playter", "13": "Guido van Rossum"}

model = Model.from_pretrained(
    "pyannote/embedding", use_auth_token="PAST_THE_ACCESS_TOKEN_HERE")

vec = Inference(model, window='whole')

def select():
    try:
        global test, distance, name
        distance = 0.7
        name = "unkown"
        textbox.delete(0.0, 'end')
        textbox1.delete(0.0, 'end')
        label3.configure(text="0%")
        progressbar.set(0)
        app.filename = filedialog.askopenfilename(initialdir="C:/Users/mohamed/Desktop/projects_python/voice_recognition/audios",
                                                  title="select a file", filetypes=(("mp3 files", "*.mp3"), ("wav files", "*.wav")))
        textbox.insert(0.0, app.filename)
        test = vec(app.filename)
    except:
        textbox.insert(0.0, "please select an audio")


def search():
    global distance, name
    num = len(dataset)
    for i in range(num):
        percent = (i+1) / num
        a = vec(f"actors/{i+1}.mp3")
        x = [test, a]
        y = pdist(x, metric='cosine')
        if round(y[0], 4) <= distance:
            distance = round(y[0], 4)
            name = dataset[f"{i+1}"]
        progressbar.set(percent)
        label3.configure(text=f"{int(percent*100)}%")
        label3.update()

    textbox1.insert('end', "\n the speake is : " + name)


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("780x580")
app.title('Speaker Recognition / Verification')


frame = customtkinter.CTkFrame(app, width=760, height=100, corner_radius=15)
frame.place(x=10, y=20)

label = customtkinter.CTkLabel(
    frame, text="File Name :", font=customtkinter.CTkFont(family='calibre', size=15, weight="bold"))
label.place(x=30, y=5)

textbox = customtkinter.CTkTextbox(
    frame, width=630, height=40, font=customtkinter.CTkFont(family='calibre', size=17))
textbox.place(x=15, y=40)

button = customtkinter.CTkButton(frame, corner_radius=5, width=60, height=40, command=select, text="Select File",
                                 font=customtkinter.CTkFont(size=15, weight="bold"))
button.place(x=655, y=40)

frame1 = customtkinter.CTkFrame(app, width=760, height=200, corner_radius=15)
frame1.place(x=10, y=140)

label1 = customtkinter.CTkLabel(
    frame1, text="Progress Bar :", font=customtkinter.CTkFont(family='calibre', size=15, weight="bold"))
label1.place(x=30, y=5)

label3 = customtkinter.CTkLabel(
    frame1, text="0%", width=40, font=customtkinter.CTkFont(family='arial', size=20))
label3.place(x=690, y=5)

progressbar = customtkinter.CTkProgressBar(
    frame1, width=740, height=10, corner_radius=15)
progressbar.set(0)
progressbar.place(x=10, y=40)

label2 = customtkinter.CTkLabel(
    frame1, text="The Speaker :", font=customtkinter.CTkFont(family='calibre', size=15, weight="bold"))
label2.place(x=30, y=70)


textbox1 = customtkinter.CTkTextbox(
    frame1, width=530, height=90, font=customtkinter.CTkFont(size=20, weight="bold"))
textbox1.place(x=10, y=100)

button1 = customtkinter.CTkButton(frame1, corner_radius=5, width=200, height=90, command=search,
                                  text="Search For The Speaker", font=customtkinter.CTkFont(size=15, weight="bold"))
button1.place(x=550, y=100)
app.mainloop()
