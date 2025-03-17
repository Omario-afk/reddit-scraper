from selenium import webdriver
from selenium.webdriver.common.by import By

from redvid import Downloader

import os
from os import path
import subprocess

from time import sleep

from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb

# S => Settings Dictionary
with open("settings.txt", "r") as f:
    info = f.read().split()
    limit_of_links = int(info[0])


# Changes in Settings Tab
def edit_current_settings(value):
    with open("settings.txt", "w") as f2:
        f2.write(str(value))
    return


# updates value in gui, and settings.txt
def change_limit_of_links():
    # lol = limit_of_links
    global limit_of_links
    global limit_current
    global top
    try:
        limit_of_links = int(new_limit.get())
        limit_current.place_forget()
        limit_current = Label(canvas_Options, text='( Current: ' + str(limit_of_links) + ' )', fg='grey', bg='white',
                              font=('', 10))
        limit_current.place(x=445, y=0 + 15)
        edit_current_settings(str(limit_of_links))
    except ValueError:
        mb.showerror('  Error  ', '  New Limit Must Be A Number  ')
    return


def empty_comp_folder():
    comp_dir = 'Temp\\'
    if not os.listdir(comp_dir):
        mb.showinfo('Info', 'The File Is Already Empty')
        pass
    else:
        for i in os.listdir(comp_dir):
            os.remove(comp_dir + i)
        mb.showinfo('Info', 'The File Has Been Emptied')
    return


def link_added():
    global subreddit_link
    global downloaded_dir
    global done_txt, mid_txt, bot_txt
    done_txt.place_forget()
    mid_txt.place_forget()
    bot_txt.place_forget()

    s_link = subreddit_link.get()

    if not s_link:
        s_link = "https://www.reddit.com/r/funnyvideos/"
    if s_link.startswith('https:'):

        int_txt = Label(canvas_B, text="Step1: Getting Link ---> Completed", fg='white', bg='#191919',
                        font=('fixedsys', 7))
        int_txt.place(x=15, y=15)
    else:
        mb.showerror('Invalid Link', '     Please Enter A Valid URL         ')
        pass
    return


downloaded_dir = 'Temp//'

# =======================================================================================================================
# Reddit
# =======================================================================================================================

# Parsing the subreddit link for links of videos and Downloading them
def Start():
    chrome_options = webdriver.ChromeOptions()
    prefs = {'profile.default_content_setting_values.notifications': 2, 'download.default_directory': downloaded_dir}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument('--incognito')

    while True:
        try:
            driver = webdriver.Chrome(options=chrome_options)
            break
        except AttributeError:
            sleep(5)

    # functions only used locally:
    def remove_duplicate_videos():
        # Deleting duplicates
        # new_path to reload contents of old path
        tmp_path = os.listdir(downloaded_dir)
        sizes = []
        for np in tmp_path:
            item_path = downloaded_dir + np
            size = os.path.getsize(item_path)
            if size in sizes:
                os.remove(item_path)
            else:
                sizes.append(size)
        print('Duplicate Videos Deleted')
        sleep(1)

    def open_downloaded_dir():
        os.startfile(downloaded_dir)

    def download_videos(reddit_link):

        link_parts = [reddit_link.split('/')]
        try:
            print('Searching in : ' + link_parts[0][3] + '/' + link_parts[0][4] + '/' + link_parts[0][
                5] + ', Downloading in: ' + downloaded_dir)

        except IndexError:
            print('Downloading in: ' + downloaded_dir)

        sleep(0.5)
        driver.get(reddit_link)
        print('Driver Opened')
        sleep(3)
        print('Scrolling...')

        reached_limit = 0
        number_of_links_change = 0
        scroll_more = 1
        driver.execute_script(f"window.scrollTo(0, {100000 * scroll_more})")
        links_to_download = []
        downloaded = 1
        reddit = Downloader(max_q=True, path=downloaded_dir)
        reddit.log = False

        while True:
            sleep(2)
            elements = driver.find_elements(by=By.TAG_NAME, value="a")
            for element in elements:
                if downloaded > limit_of_links:
                    return
                link = element.get_attribute("href")
                if "comments" in link and link not in links_to_download:
                    # print(link)
                    reddit.url = link
                    reddit.overwrite = True
                    reddit.filename = str(downloaded)
                    try:
                        status = reddit.download()
                    except BaseException as e:
                        print(e)
                        continue

                    if str(status).endswith(".mp4"):  # download successful
                        print(f"{downloaded}/{limit_of_links}")
                        downloaded += 1
                        links_to_download.append(link)
                    else:
                        print(link, status)
                else:
                    pass

            if links_to_download == number_of_links_change:
                reached_limit += 1
                scroll_more += .5
            else:
                number_of_links_change = links_to_download

            # keeping number of links below limits
            if len(links_to_download) >= limit_of_links:
                links_to_download = links_to_download[:limit_of_links]
                break

            else:
                driver.execute_script(f"window.scrollTo(0, {100000 * scroll_more})")
                # print(len(links), "links...")
                sleep(5)
                pass

            if reached_limit == 5:  # if no more links after 5 scrolls
                print(f'Couldn\'t find {new_limit} videos, going with the limit: {downloaded}!')
                break

            print(f"found {len(links_to_download)}/{limit_of_links}, scrolling...")

        print('Links Fetched')

        print('Total = ' + str(len(links_to_download)))

        print('--')

    sub_link = subreddit_link.get()
    if not sub_link: sub_link = "https://www.reddit.com/r/funnyvideos/"
    download_videos(sub_link)

    remove_duplicate_videos()

    mid_txt.place(x=15, y=65)

    print("Finished")
    sleep(1)
    print('***')

    dled_button = Button(canvas_TR, text='Open Downloaded Videos In Folder', fg='white', bg='#4AADAD', padx=71,
                         pady=20, bd=1, command=open_downloaded_dir)
    dled_button.place(x=20, y=220)

# Compiling the downloaded videos from step2 into msg single Video

def Compile_Videos():
    global done_txt, bot_txt
    open("Concat.txt", "w").close()
    with open("Concat.txt", "a") as f:
        for i in os.listdir(downloaded_dir):
            if path.isdir(downloaded_dir + i) or i.endswith("txt") or i.endswith("py") or i == "out.mp4":
                continue
            f.write(f"file {downloaded_dir + i}\n")

    cmd = ["ffmpeg", "-f", "concat", "-safe", "0", "-i", "Concat.txt", "-c", "copy", "-y", "Out//out.mp4"]
    output = subprocess.check_output(cmd).decode("utf-8").strip()
    print(output)
    print('Finished Compiling.')
    bot_txt.place(x=15, y=115)
    # -----------

    done_txt.place(x=540, y=10)

    if mb.askyesno("Confirmation", "Delete the downloaded videos ?"):
        for temp in os.listdir(downloaded_dir):
            os.remove(downloaded_dir + temp)
        print('Temp Folder Cleaned')
    print('Finished')
    print('***')

# Functions that use/are used by GUI elements
# tkinter GUI

window = Tk()
window.title("[ Video Downloader ]")
window.iconbitmap('logo.ico')
window.geometry("1000x600")
window.minsize(width=1000, height=600)
window.maxsize(width=1000, height=600)
options_bg = PhotoImage(file="options_bg.png")
reddit_bg = PhotoImage(file="reddit_bg.png")
notebook = ttk.Notebook(window)
ttk.Style().theme_create("MyStyle", parent="alt", settings={
    "TNotebook": {"configure": {"tabmargins": [0, 0, 1, 0]}},
    "TNotebook.Tab": {"configure": {"padding": [40, 4],
                                    "font": ('', '11', '')}, }})
ttk.Style().theme_use("MyStyle")
# Reddit Tab
Reddit_Frame = Frame(notebook, width=1000, height=600)
notebook.add(Reddit_Frame, text='Reddit')
background_label = Label(Reddit_Frame, image=reddit_bg)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
# Tl = Top Left
canvas_TL = Canvas(Reddit_Frame, width=300, height=376, bg='#ff4301', bd=2, relief=SUNKEN)
canvas_TL.place(x=10, y=10)
# Change the subreddit link / Use the default one
text_subreddit = Label(canvas_TL, text="1. Use Link: ", fg='white', bg='#912B11', font=('Verdana', 11),
                       relief=SUNKEN)
text_subreddit.place(x=15, y=30)
subreddit_link = Entry(window)
canvas_TL.create_window(128, 78, window=subreddit_link, height=25, width=230)
button_subreddit = Button(text=" OK ", fg='white', bg='#4AADAD', command=link_added)
canvas_TL.create_window(270, 80, window=button_subreddit)
# Parse the subreddit page for the links and download them
text_link_dl = Label(canvas_TL, text="2. Download The Videos: ", fg='white', bg='#912B11', font=('Verdana', 11),
                     relief=SUNKEN)
text_link_dl.place(x=15, y=150)
button_link_dl = Button(canvas_TL, text="      Start      ", fg='white', bg='#4AADAD', command=Start)
canvas_TL.create_window(250, 200, window=button_link_dl)
# Compile the videos downloaded
text_mp4 = Label(canvas_TL, text="3. Concat The Videos: ", fg='white', bg='#912B11', font=('Verdana', 11),
                 relief=SUNKEN)
text_mp4.place(x=15, y=270)
button_mp4 = Button(canvas_TL, text="      Start      ", fg='white', bg='#4AADAD', command=Compile_Videos)
canvas_TL.create_window(250, 320, window=button_mp4)
# TR = Top Right
canvas_TR = Canvas(Reddit_Frame, width=630, height=380, bg='white', relief=SUNKEN)
canvas_TR.place(x=333, y=10)
# B = Bottom
canvas_B = Canvas(Reddit_Frame, width=950, height=155, bg='#191919', bd=2, relief=SUNKEN)
canvas_B.place(x=10, y=400)
mid_txt = Label(canvas_B, text="Step2: Downloading Videos ---> Completed (Select .mp4s to keep in folder)", fg='white',
                bg='#191919', font=('fixedsys', 7))
done_txt = Label(canvas_B, text=" | DONE |", fg='white', bg='#191919', font=('fixedsys', 100))
bot_txt = Label(canvas_B, text="Step3: Video Compiling and Exporting ---> Completed", fg='white', bg='#191919',
                font=('fixedsys', 7))
# Settings Tab
Options_Frame = Frame(notebook, width=1000, height=600)
background_label = Label(Options_Frame, image=options_bg)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
canvas_Options = Canvas(Options_Frame, width=630, height=505, bg='white')
canvas_Options.place(x=20, y=40)

notebook.add(Options_Frame, text='Settings')
top = 0
# Change limit of links parsed
change_limit_text = Label(canvas_Options, text='Change The Limit Number Of Downloads:', fg='black', bg='white',
                          font=('', 13))
change_limit_text.place(x=20, y=top + 15)
new_limit = Entry(canvas_Options)
canvas_Options.create_window(175, top + 75, window=new_limit, height=25, width=50)
limit_button = Button(canvas_Options, text='Change', fg='white', bg='black', command=change_limit_of_links, height=1,
                      width=8)
limit_button.place(x=300, y=top + 60)
limit_current = Label(canvas_Options, text='( Current: ' + str(limit_of_links) + ' )', fg='grey', bg='white',
                      font=('', 10))
limit_current.place(x=445, y=top + 15)
top += 100

notebook.pack()
window.mainloop()
