import tkinter as tk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
from tkinter.scrolledtext import ScrolledText

import json
import os.path

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        master.minsize(width=770, height=310)
        master.maxsize(width=770, height=310)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        #Text Frame - Directory
        self.text_frame = tk.Frame(self, width=500, height=23)
        self.text_frame.grid()
        self.text_frame.grid_propagate(False)
        #Text
        self.text = tk.Text(self.text_frame,borderwidth=1, relief="sunken",  width=78)
        self.text.insert('1.0', 'Select \'songs\' directory...')
        self.text.config(font=("consolas", 8), undo=False, wrap='word', state='disabled')
        self.text.grid(row=0, column=0, sticky="nsew", padx=10, pady=0)


        self.browse = tk.Button(self, text='Browse', command=self.select_directory)
        self.browse.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.update_files = tk.Button(self, text='Update Difficulties', command=self.update_directory)
        self.update_files.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)

        #Text Frame - Logging
        self.logging_frame = tk.Frame(self, width=500, height=250)
        self.logging_frame.grid()
        self.logging_frame.grid_propagate(False)
        # Text - Logging
        self.logging_text = ScrolledText(self.logging_frame, borderwidth=1, relief="groove", width=78, height=18)
        self.logging_text.insert('1.0', """Updated files will be listed here.""")
        self.logging_text.config(font=("consolas", 8), undo=False, wrap='word', state='disable')
        self.logging_text.grid(row=1, column=0, columnspan=1, rowspan = 3, sticky="nsew", padx=10, pady=10)

        self.credits = tk.Label(self, text='\n\n\n\n\n\n\n\n\n\n\n\n\n\nCreated by Kuenaimaku#8206 and rdtoi1#7673\nFind us on Discord!')
        self.credits.grid(row=1, column=1, columnspan=2, sticky="new", padx=10, pady=10)

        self.warning = tk.Label(self, fg='red',
                                text='\n\n\n\nIf your SDVX converts are out of date,\nsome charts may not be updated.')
        self.warning.grid(row=1, column=1, columnspan=2, sticky="new", padx=10, pady=10)

        self.instructions = tk.Label(self,
                                     text='Before updating, remove any SDVX Heavenly \nHaven songs and custom charts from your\nsongs directory.')
        self.instructions.grid(row=1, column=1, columnspan=2, sticky="new", padx=10, pady=10)

    def select_directory(self):
        directory = filedialog.askdirectory(initialdir='~')
        if directory:
            self.directory = directory
            self.text.config(state='normal')
            self.text.delete('1.0', '2.0')
            self.text.insert('1.0', directory)
            self.text.config(state='disabled')
        else:
            self.directory = None
            self.directory = directory
            self.text.config(state='normal')
            self.text.delete('1.0', '2.0')
            self.text.insert('1.0', 'Select \'songs\' directory...')
            self.text.config(state='disabled')

    def update_directory(self):
        if '/songs' in self.directory:
            with open('storage/songs.json', 'r', encoding='utf-8') as f:
                song_list = json.load(f)
            f.close()
            self.logging_text.config(state='normal')
            self.logging_text.delete('1.0', '2.0')
            self.logging_text.insert('end', '=====SONGS UPDATED=====\n\n')
            self.logging_text.config(state='disable')
            exhaust_names = ['extended']
            gravity_names = ['infinite']
            file_list = []
            for root, dirs, files in os.walk(self.directory):
                for file in files:
                    if str(file).endswith('.ksh'):
                        file_list.append('{}/{}'.format(root.replace("\\", "/"), file))

            for file in file_list:
                with open(file, 'r', encoding='utf-8') as song_file:
                    song_data = song_file.read().splitlines()
                song_file.close()
                song_title = song_data[0][6:len(song_data[0])].replace('=', '', 1)
                for song in song_list:
                    if song["title"] == song_title:
                        update = False
                        song_difficulty = song_data[5][10:len(song_data[5])].replace('=', '', 1)
                        song_level = song_data[6][6:len(song_data[6])].replace('=', '', 1)
                        if song_difficulty in exhaust_names and "exhaust" in song.keys():
                            self.logging_text.config(state='normal')
                            self.logging_text.insert('end','{} {} - Update {} to {}\n'.format(song["title"], 'Exhaust', song_level, song["exhaust"]))
                            song_data[6] = 'level={}'.format(song["exhaust"])
                            song["exhaust_update"] = True
                            update = True
                        elif song_difficulty in gravity_names and "gravity" in song.keys():
                            self.logging_text.config(state='normal')
                            self.logging_text.insert('end', '{} {} - Update {} to {}\n'.format(song["title"], 'Gravity ', song_level, song["gravity"]))
                            song_data[6] = 'level={}'.format(song["gravity"])
                            song["gravity_update"] = True
                            update = True
                        else:
                            update = False
                        self.logging_text.config(state='disable')
                        if update:
                            with open(file, 'wt', encoding='utf-8') as f:
                                for l in song_data:
                                    f.write('{}\n'.format(l))
                                f.close()
            self.logging_text.config(state='normal')
            self.logging_text.insert('end', '\n=====SONGS NOT FOUND=====\n\n')
            for song in song_list:
                if ('exhaust_update' not in song) and ('exhaust' in song):
                    self.logging_text.insert('end',"{} - {} not found\n".format(song["title"], 'exhaust'))
                if ('gravity_update' not in song) and ('gravity' in song):
                    self.logging_text.insert('end',"{} - {} not found\n".format(song["title"], 'gravity'))
            self.logging_text.config(state='disable')

        else:
            messagebox.showerror("songs directory not found","songs not found in directory structure. Stopping now...")
            return


root = tk.Tk()
root.title("K-SHOOT MANIA SDVX Convert Difficulty Updater")
root.iconbitmap(r'drill.ico')
root.resizable(width=False, height=False)
app = Application(master=root)

app.mainloop()

