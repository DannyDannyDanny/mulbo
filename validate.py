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


def write_rawfile(filepath):
    """tries to load specified filepath, writes signal to rawfile:
    44100Hz, 1 channel (Mono), signed 16 bit PCM little endian"""
    # load file

    print(8*'------')
    print(f'reading file\t{filepath}')
    audio_array, samplerate = sf.read(filepath)
    print(f'\tsamples\t{audio_array.shape}')
    print(f'\tsamplerate\t{samplerate}')

    if samplerate != 44100:
        # TODO add samplerate adjustment
        print('needs to adjust samplerate')

    # generate uuid for outname
    id = filepath + str(audio_array.sum())
    id = uuid.uuid5(uuid.NAMESPACE_OID, id).hex
    outname = config.dirs['rawfiles'] + id + '.raw'

    # write rawfile
    print(f'writing rawfile\t{outname}')
    kwargs = dict(samplerate=samplerate, subtype='PCM_16', endian='BIG')
    sf.write(outname, audio_array, **kwargs)
    return outname


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
