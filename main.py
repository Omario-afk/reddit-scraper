from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException as Selenium_Error

from time import time

import os
import shutil

from time import sleep

from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb

import socket

from datetime import datetime as date

from moviepy.editor import VideoFileClip, concatenate_videoclips

# S => Settings Dictionary
with open("settings.txt", "r") as f:
    limit_of_links = int(f.read())


# Changes in Settings Tab
def edit_current_settings(value):
    with open("settings.txt", "w") as f:
        f.write(value)
    return


def change_lol():
    # lol = limit_of_links
    global limit_of_links
    global limit_current
    global top

    try:
        limit = int(new_limit.get())
        limit_of_links = limit
        limit_current.place_forget()
        limit_current = Label(canvas_Options, text='( Current: ' + str(limit_of_links) + ' )', fg='grey', bg='white',
                              font=('', 10))
        limit_current.place(x=445, y=top + 15)
        edit_current_settings('Slimit_of_links', new_limit.get())
    except ValueError:
        mb.showerror('  Error  ', '  New Limit Must Be A Number  ')

    return


def empty_comp_folder():
    global delete_files_button
    comp_dir = 'Temp\\'
    if not os.listdir(comp_dir):
        mb.showinfo('Info', 'The File Is Already Empty')
        pass
    else:
        for i in os.listdir(comp_dir):
            os.remove(comp_dir + i)
        mb.showinfo('Info', 'The File Has Been Emptied')
    return


New_Link_Added = False


def link_added():
    global subreddit_link
    global Default_links_list
    global New_Link_Added
    global downloaded_dir
    global video_title
    s_link = subreddit_link.get()
    int_txt = Label(canvas_B, text="Step1: Getting Link ---> Completed", fg='white', bg='#191919',
                    font=('fixedsys', 7))
    int_txt.place(x=15, y=15)
    if s_link != '' and s_link.startswith('https:'):
        pass
    else:
        mb.showerror('Invalid Link', '     Please Enter A Valid URL         ')
        pass
    return


downloaded_dir = 'E:\\Python\\Project400\\Temp\\'


# =======================================================================================================================
# =======================================================================================================================
# =======================================================================================================================
# Reddit
# =======================================================================================================================
# =======================================================================================================================
# =======================================================================================================================

# Parsing the subreddit link for links of videos and Downloading them
# GD => Get links and Download them (videos)
def Start():
    from selenium.webdriver.common.keys import Keys
    chrome_options = webdriver.ChromeOptions()
    prefs = {'profile.default_content_setting_values.notifications': 2, 'download.default_directory': downloaded_dir}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument('--incognito')
    ask = mb.askyesnocancel('Start', '    Run Everything In The Background?    ')
    if ask:
        chrome_options.add_argument('--headless')
        withdraw_window = True
    elif ask is None:
        return
    else:
        withdraw_window = False
        pass

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    #Default_links_list_len = sum(1 * (i != '') for i in Default_links_list)
    #limit_of_iterations = int(limit_of_links / Default_links_list_len)
    #print('Iterations: ' + str(limit_of_iterations))

    # functions only used locally:

    def remove_duplicate_videos():
        # Deleting duplicates
        # new_path to reload contents of old path
        path = os.listdir(downloaded_dir)
        sizes = []
        for np in path:
            item_path = downloaded_dir + np
            size = os.path.getsize(item_path)
            if size in sizes:
                os.remove(item_path)
            else:
                sizes.append(size)
        print('Doubles Deleted')
        sleep(1)

    def new_tab():
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[0])
        driver.close()
        driver.switch_to.window(driver.window_handles[-1])

    def open_downloaded_dir():
        os.startfile(downloaded_dir)

    def get_reddit(reddit_link):

        link_parts = [reddit_link.split('/')]
        try:
            print('Parsing: ' + link_parts[0][3] + '/' + link_parts[0][4] + '/' + link_parts[0][
                5] + ', Location: ' + downloaded_dir)

        except IndexError:
            print('Parsing' + ', Location: ' + downloaded_dir)

        sleep(0.5)

        print('Fetching Links...')

        driver.get(reddit_link)

        print('Driver Opened')
        # Time for the page to load
        sleep(5)

        # Couldn't copy video links => Copying header links. All videos have headers but not all headers have video links
        # If msg video is downloaded twice, one of them will be deleted in trim_mp4()
        # Limit_of_links to be changed in settings/Settings.txt
        print('Scrolling...')

        reached_limit = 0
        limit = 0
        scroll_more = 1
        while True:

            elements = driver.find_elements_by_class_name('_3jOxDPIQ0KaOWpzvSQo-1s')
            links = [element.get_attribute('href') for element in elements]
            if len(links) == limit:
                reached_limit += 1
                scroll_more += .5
            else:
                limit = len(links)

            # keeping number of links below limits
            if len(links) > limit_of_iterations:
                links = links[0:limit_of_links]
                break

            else:
                driver.execute_script(f"window.scrollTo(0, {100000 * scroll_more})")
                print(len(links), "links...")
                sleep(5)
                pass

            if reached_limit == 6:
                print('couldn\'t reach {}, going with the limit: {}!'.format(limit_of_iterations, len(links)))
                break
        print('Links Fetched')

        number_of_links = len(links)

        print('Total = ' + str(number_of_links))

        print('--')

        new_tab()

        print('Starting Download...')

        downloaded = 0
        skipped = 0

        for a_link in links:

            sleep(1)

            driver.get('https://www.viddit.red')

            sleep(2)

            try:
                search_bar = driver.find_element_by_xpath('//*[@id="dlURL"]')
                search_bar.send_keys(a_link + Keys.RETURN)

                sleep(2)

                dl_button = driver.find_element_by_id('dlbutton')
                dl_link = dl_button.get_attribute('href')

                # The links that have 'redd' are either Pictures or Videos with no audio

                if 'youtube' in dl_link or 'redd.it' in dl_link or dl_link.endswith('.png') or dl_link.endswith(
                        '.jpg') or 'www.reddit.com' in dl_link:
                    skipped += 1
                    pass

                else:
                    # Opening the dl_link with no redd starts the download automatically
                    driver.get(dl_link)
                    downloaded += 1
                    remaining = str(number_of_links - downloaded - skipped)
                    str_format = len(str(number_of_links)) - len(remaining)
                    print('Remaining: ' + str(
                        remaining) + ' ' * str_format + ' || ' + 'Downloaded: {}, Skipped: {}'.format(
                        downloaded, skipped))
            except Selenium_Error:
                pass

    def GD_done():

        new_tab()

        print("Waiting for downloads...")

        print('waiting', end='')

        while True:

            stop = True

            for file in os.listdir(downloaded_dir):

                if file.endswith('.crdownload'):
                    stop = False
                    break

                else:
                    pass

            if stop:
                break

            else:
                pass

            sleep(2)

        print('---')

        print('Elapsed time: ' + str(int(time() - starting_time) // 60) + ' Minutes ' + str(
            int(time() - starting_time) % 60) + ' Seconds')

        remove_duplicate_videos()

        print('Folder Cleaned')

        mid_txt.place(x=15, y=65)

        print("Finished")
        sleep(1)
        print('***')

        driver.quit()

        if withdraw_window:
            window.deiconify()
        else:
            pass

        dled_button = Button(canvas_TR, text='Open Downloaded MP4s In Folder', fg='white', bg='#4AADAD', padx=71,
                             pady=20, bd=1, command=open_downloaded_dir)
        dled_button.place(x=20, y=220)

        shut_down()

        return

    # Show warning in case default setting to shut down pc is on

    print('Starting [A]')
    sleep(0.5)
    print('--------')

    if withdraw_window:
        window.withdraw()
    else:
        pass

    check_day()

    starting_time = time()

    GD_done()


# Compiling the downloaded videos from step2 into msg single .mp4 using VSDC
New_Vid_name = ''


def Compile_mp4():
    # temp_dir = downloaded_dir  #"E:\\Python\\Nier\\Comp_Vids\\_Temp\\"
    # added
    temp_dir = "E:\\Python\\Project400\\Temp\\"
    for i in os.listdir(downloaded_dir):
        shutil.move(downloaded_dir + "\\" + i, temp_dir)
    # end_added

    files = [temp_dir + i for i in os.listdir(temp_dir)]
    clips = [VideoFileClip(file) for file in files]
    tmp = [clip.resize(1280 / clip.h) for clip in clips]
    clips = tmp

    # print   ('Videos Copied.')
    # sleep(1)
    final_clip = concatenate_videoclips(clips, method="compose")
    print('Starting Video Compilation...')

    final_clip.write_videofile('E:\\Python\\Nier\\Comp_Vids\\Output\\{}.mp4'.format(New_Vid_name), codec="mpeg4")

    print('Finished Compiling.')
    # this ^ on the GUI
    bot_txt = Label(canvas_B, text="Step3: Video Compiling and Exporting ---> Completed", fg='white', bg='#191919',
                    font=('fixedsys', 7))
    bot_txt.place(x=15, y=115)
    # -----------
    end_txt = Label(canvas_B, text=" | DONE |", fg='white', bg='#191919', font=('fixedsys', 100))
    end_txt.place(x=540, y=10)

    for temp in os.listdir(temp_dir):
        os.remove(temp_dir + temp)
    print('Temp Folder Cleaned')
    sleep(1)
    print('Finished')
    sleep(1)
    print('***')


# =======================================================================================================================
# Functions that use/are used by GUI elements
# =======================================================================================================================
# =======================================================================================================================
# tkinter GUI
# =======================================================================================================================


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
# =======================================================================================================================
# =======================================================================================================================
# =======================================================================================================================
# Reddit Tab
# =======================================================================================================================
# =======================================================================================================================
# =======================================================================================================================
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
canvas_TL.create_window(115, 78, window=subreddit_link, height=25, width=200)
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
button_mp4 = Button(canvas_TL, text="      Start      ", fg='white', bg='#4AADAD', command=Compile_mp4)
canvas_TL.create_window(250, 320, window=button_mp4)

# TR = Top Right
canvas_TR = Canvas(Reddit_Frame, width=630, height=380, bg='white', relief=SUNKEN)
canvas_TR.place(x=333, y=10)
# B = Bottom
canvas_B = Canvas(Reddit_Frame, width=950, height=155, bg='#191919', bd=2, relief=SUNKEN)
canvas_B.place(x=10, y=400)
mid_txt = Label(canvas_B, text="Step2: Downloading Videos ---> Completed (Select .mp4s Manually)", fg='white',
                bg='#191919', font=('fixedsys', 7))
# =======================================================================================================================
# =======================================================================================================================
# =======================================================================================================================
# [\O\p\t\i\o\n\s\] Settings Tab
# =======================================================================================================================
# =======================================================================================================================
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
limit_button = Button(canvas_Options, text='Change', fg='white', bg='black', command=change_lol, height=1, width=8)
limit_button.place(x=300, y=top + 60)
limit_current = Label(canvas_Options, text='( Current: ' + str(limit_of_links) + ' )', fg='grey', bg='white',
                      font=('', 10))
limit_current.place(x=445, y=top + 15)

# Delete the Compiling videos
delete_files_text = Label(canvas_Options, text='Empty The Compiling Videos Folder:', fg='black', bg='white',
                          font=('', 13))
delete_files_text.place(x=20, y=top + 100 + 15)
delete_files_button = Button(canvas_Options, text='Delete', fg='white', bg='black', command=empty_comp_folder, height=1,
                             width=8)
delete_files_button.place(x=300, y=top + 100 + 55)
# files_current_empty = Label(canvas_Options, text='(Current: Empty)', fg='grey', bg='white', font=('', 10))
# files_current_not_empty = Label(canvas_Options, text='(Current: Not Empty)', fg='grey', bg='white', font=('', 10))

notebook.pack()
window.mainloop()
