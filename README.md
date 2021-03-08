# Mulbo
Mulbo - audio experiments

## This sound is not real
A page like [this person does not exist](https://thispersondoesnotexist.com), except it generates new sounds.

## Audio Library
Library organizer that manages a file structure with your audio data.
1. Put all your music on your server and free up space on your local machine
2. Only keep the songs you *need* locally.
3. Systematically organize _sub-libraries_.

## Next Steps
* [x] Find solution for [RapidAPI 413 discussion](https://rapidapi.com/apidojo/api/shazam/discussions?issueId=19362&issueTitle=payload-validation-and-how-to-deal-with-%22413-Request-Entity-Too-Large%22).
* [ ] Expand telegram bot interface with [Advanced Filters](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions-%E2%80%93-Advanced-Filters)

## Database and Folder structure
The database is built from the following four tables:
* *My Collection* - A generic placeholder where new songs are added. This is the only folder scanned by the program.
* *Originals* - Each file in my collection is assigned a uuid and copied by to this folder under its id. Files only make it here if their signal can be read.
* *Raw files* - Each original file signal is written as a raw audio file to this directory. The uuid persists across filenames.
* *Responses* - Each signal if sampled and sent to the Shazam API. The response is pickled and saved to this directory under its uuid.

The sqlite database *mulbo.db* stores the song datamodel relationships and paths to raw data. Folders are organized in the following tree structure:
```
library
├── mulbo.db
├── mycollection
│   ├── 'some artist - some song (some album).wav'
│   ├── ...
│   └── 'other artist - other song (other album).mp3'
├── originals
│   ├── 049aed2c9ab95b658c19fd01c55fbb6b.wav
│   ├── ...
│   └── 31e951d4bc9e5d228ea53a199b15cd00.mp3
├── rawfiles
│   ├── 049aed2c9ab95b658c19fd01c55fbb6b.raw
│   ├── ...
│   └── 31e951d4bc9e5d228ea53a199b15cd00.raw
└── responses
    ├── 049aed2c9ab95b658c19fd01c55fbb6b.pkl
    ├── ...
    └── 31e951d4bc9e5d228ea53a199b15cd00.pkl
```
