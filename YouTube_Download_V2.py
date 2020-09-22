from pytube import YouTube
import pytubemp3
import os

prev_perc = 0.0
now_perc = 0.0

title = ""

def progress_function(chunk, file_handle, bytes_remaining):
    global prev_perc, now_perc
    percent = (1 - bytes_remaining / file_size) * 100
    now_perc = percent
    if str(now_perc)[0:2] != str(prev_perc)[0:2]:
        print("{:00.0f}% downloaded".format(percent))
    prev_perc = now_perc

print("\tWelcome to Youtube video downloader!\n\n")

while True:
    ext = str(input("Please enter a valid file type(a̱udio/v̱ideo): "))

    if ext == "audio" or ext == "video":
        print()
        break
    elif ext == "a":
        ext = "audio"
        print()
        break
    elif ext == "v":
        ext = "video"
        print()
        break
    else:
        print("Incorrect value!")

while True:
    url = str(input("Please enter a valid url of a YouTube video: "))

    if "&list" in url:
        head, sep, tail = url.partition('&list')
        url=head

    if ext == "video":
        try:
            yt = YouTube(url, on_progress_callback=progress_function)

            title = yt.title
            title += ".mp4"

            vids = yt.streams.filter(type="video", progressive=True, file_extension = "mp4")
            for i in range(len(vids)):
                string = "- " + vids[i].mime_type

                if not "audio" in vids[i].mime_type:
                    string += (", resolution: " + vids[i].resolution)

                string += (", fps: " + str(vids[i].fps))

                print(i,string)

            while True:
                try:
                    vnum = int(input("Enter profile number: "))
                except:
                    print("Incorrect value!")
                    continue

                if vnum >= 0 and vnum <= len(vids):
                    break
                else:
                    print("Incorrect value!")
                    continue

            global file_size
            file_size = vids[vnum].filesize

            yt.streams[vnum].download()

            break
        except:
            print("Something went wrong(maybe the link is incorrect). Try again.")

    elif ext == "audio":
        try:
            vid = pytubemp3.YouTube(url, on_progress_callback=progress_function).streams.filter(only_audio=True).first()
            title = pytubemp3.YouTube(url).title
            title += ".mp3"

            file_size = vid.filesize

            vid.download()
            break
        except:
            print("Something went wrong(maybe the link is incorrect). Try again.\n")

print('\nThe video was downloaded to the program folder, with the name "' + title + '"')

input("\nPress enter to quit...")
