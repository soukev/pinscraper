from tkinter import *
from PIL import ImageTk, Image
import sqlite3
import sys

def back():
    global cur # current image index
    cur = cur - 1
    set_image()

def forward():
    global cur # current image index
    cur = cur + 1
    set_image()


def set_image():
    global root
    global images
    global label
    global button_back
    global button_exit
    global button_forward
    global cur # current image index
    label.grid_forget()
    img = images[cur]
    label = Label(image=img)

    label.grid(row=1, column=0,columnspan=3)
    root.geometry(str(images[cur].width()) + 'x' + str(images[cur].height() + 50))
    if(cur == 0):
        button_back['state'] = DISABLED
    else:
        button_back['state'] = NORMAL

    if(cur == len(images) - 1):
        button_forward['state'] = DISABLED
    else:
        button_forward['state'] = NORMAL


def get_images(dbfile='data.sqlite'):
    global images
    with sqlite3.connect(dbfile, detect_types=sqlite3.PARSE_DECLTYPES) as conn:
        # check existence of database
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS images
                    (id TEXT, file_name TEXT, custom_title TEXT, url TEXT, PRIMARY KEY(id,url))''')
        c.execute('''CREATE INDEX IF NOT EXISTS idx_id ON images (id)''')

        c.execute('SELECT id, file_name, custom_title, url FROM images')
        r = c.fetchall()
        for row in r:
            try:
                img = Image.open("downloaded_imgs/" + row[1])
                height, width= img.size
                # image is too big, change size
                if (height > 900):
                    h = 900
                    ratio = 900 / img.height() # get ratio in percentage
                    w = img.width() * ratio # change width and remain aspect ratio
                    img.resize(w, h)
                images.append(ImageTk.PhotoImage(img))
            except Exception as err:
                continue


def main():
    global root
    global images
    global label
    global button_back
    global button_exit
    global button_forward
    global cur # current image index
    cur = 0
    root = Tk()
    root.title("Pinscrape image viewer")
    root.bind('n', lambda event: forward() if cur < len(images) -1 else None)
    root.bind('p', lambda event: back() if cur > 0 else None)


    images = []
    get_images()
    if(len(images) <= 0):
        print("NO IMAGES")
        sys.exit()
    label = Label(image=images[0])

    button_back = Button(root, text="Back", command=back)

    button_exit = Button(root, text="Exit", command=root.quit)

    button_forward = Button(root, text="Forward", command=forward)
    set_image()

    button_back.grid(row=5, column=0)
    button_exit.grid(row=5, column=1)
    button_forward.grid(row=5, column=2)

    root.mainloop()

if __name__ == "__main__":
    main()
