# K-Shoot Mania Difficulty Changer

Small tool to change the level scale on old SOUND VOLTEX converts.

### Details

This tool will look at the specified directory, and analyze the contents of each `.ksh` file to find the title, difficulty,
and current level of the chart. With this data, it compares it to the `.json` file and sees if there's a match on difficulty
and title. On a match, the `.ksh` file will be updated. At the end, the logging window will post the results of the update.

### Prerequisites

This tool is developed on Python 3.5.1 and is packaged for windows using `pyinstaller`. Only core libraries are leaned upon,
 which are `tkinter`, `json`, and `os.path`.
 
### Credits

rdtoi on Discord provided the `songs.json` file in order for this entire application to work.