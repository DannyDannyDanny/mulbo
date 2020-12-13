import config
from glob import glob
import soundfile as sf
import base64
import requests


def shazam_prepfile():
    # load prepfile
    print('loading prepfile')
    prepfile = config.dirs['prepfile']
    payload = base64.b64encode(open(prepfile, "rb").read())

    # validate payload encoding
    print('validating prepfile payload')
    contains_zeros = bool(str(payload).count(' '))
    if not contains_zeros:
        # launch shazam request!
        print('payload validated! Posting to Shazam!')
        url = "https://shazam.p.rapidapi.com/songs/detect"
        headers = {
            'content-type': "text/plain",
            'x-rapidapi-key': config.keys['shazam'],
            'x-rapidapi-host': "shazam.p.rapidapi.com"
        }
        response = requests.request("POST", url, data=payload, headers=headers)
    else:
        print('validating prepfile payload')
        response = None
    return response


def list_audio_file_paths():
    dir_audio = config.dirs['audio']
    files_audio = glob(dir_audio + '*')
    return files_audio


def generate_prepfile_from_filepath(filepath, head=0.02):
    """loads specified filepath, writes head of signal to prepfile"""
    # load file
    print(f'reading file\t{filepath}')
    audio_array, samplerate = sf.read(filepath)
    print(f'\tsamples\t{audio_array.shape}')
    print(f'\tsamplerate\t{samplerate}')
    # cut signal
    last_sample_index = int(head*audio_array.shape[0])
    print(f'prepfile cut set to {head} ({100*head} %)')
    audio_array = audio_array[0:last_sample_index, :]
    print(f'\tsamples\t{audio_array.shape}')
    # write cut signal to prepfile
    prepfile = config.dirs['prepfile']
    print('signal hash:', hash(audio_array.sum()))
    preptwin = prepfile.replace('.raw', '.wav')
    print('writing prepfile:', prepfile)
    sf.write(prepfile, audio_array, samplerate, subtype='PCM_16', endian='BIG')
    print('writing preptwin:', preptwin)
    sf.write(preptwin, audio_array, samplerate)


# %%
filepath = 'audio/Esma Redzepova - Chaje Shukarije.wav'
filepath = 'audio/Allj - Minimal.wav'
generate_prepfile_from_filepath(filepath)
response = shazam_prepfile()
print(response.text)
# %%
print(response.text)
# %%
print(response.text)
