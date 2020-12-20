import config
from glob import glob
import soundfile as sf
import sounddevice as sd
import base64
import requests
import pandas as pd
import uuid
from scipy import signal
import matplotlib.pyplot as plt
import random as r


def get_shazam_tags(rawfile, nsec=3):
    """Takes path to a rawfile, retuns shazam tags or None."""
    kw = dict(channels=1, samplerate=44100, format='RAW', subtype='PCM_16')
    sig, fs = sf.read(rawfile, **kw)

    # get 3 or nsec seconds of signal
    cut_sig_len_sec = nsec
    cut_sig_len_sam = int(cut_sig_len_sec * 44100)
    cut_sig_max_offset = sig.shape[0] - cut_sig_len_sam
    cut_sig_firs = r.randint(0, cut_sig_max_offset - 1)
    cut_sig_last = cut_sig_firs + cut_sig_len_sam
    cut_sig = sig[cut_sig_firs: cut_sig_last]

    # write it to a raw prepfile
    prepfile = config.dirs['library'] + 'prepfile.raw'
    kwargs = dict(samplerate=fs, subtype='PCM_16', endian='LITTLE')
    sf.write(prepfile, cut_sig, **kwargs)

    # read the prepfile and b64 encode
    payload = base64.b64encode(open(prepfile, "rb").read())

    # launch shazam request!
    url = "https://shazam.p.rapidapi.com/songs/detect"
    headers = {
        'content-type': "text/plain",
        'x-rapidapi-key': config.keys['shazam'],
        'x-rapidapi-host': "shazam.p.rapidapi.com"
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    guid = raw.split('/')[-1].split('.')[0]
    resp_pdsr = pd.Series(response.__dict__)
    resp_path = config.dirs['responses'] + guid + '.pkl'
    resp_pdsr.to_pickle(resp_path)
    return resp_pdsr


def list_audio_file_paths():
    dir_audio = config.dirs['audio']
    files_audio = glob(dir_audio + '*')
    return files_audio


def read_audio_file(filepath):
    """takes filepath to audio file,
    returns array of signal array and sampleate"""
    audio_array, samplerate = sf.read(filepath)
    return audio_array, samplerate


def write_rawfile(filepath, play=False):
    """tries to load specified filepath, writes signal to rawfile:
    44100Hz, 1 channel (Mono), signed 16 bit PCM little endian"""
    # the series / row that will be appended to the dataframe
    db_ser = pd.Series(dtype=object)
    # load file
    sig, fs = read_audio_file(filepath)
    if play:
        sd.play(sig, fs)
        input()
        sd.stop()
    nsamples, nchannels = sig.shape
    db_ser['samplerate'] = fs
    db_ser['nsamples'] = nsamples
    db_ser['original_file'] = filepath
    if nchannels != 1:
        sig = sig[:, 1:]
    desired_samplerate = 44100
    if fs != desired_samplerate:
        print('resampling...')
        num = int(desired_samplerate * (nsamples/fs))
        sig = signal.resample(sig, num)
    # generate uuid for rawfile
    id = filepath + str(sig.sum())
    id = uuid.uuid5(uuid.NAMESPACE_OID, id).hex
    rawfile = config.dirs['rawfiles'] + id + '.raw'
    # write rawfile
    db_ser['rawfile'] = rawfile
    kwargs = dict(samplerate=fs, subtype='PCM_16', endian='LITTLE')
    sf.write(rawfile, sig, **kwargs)
    # print(db_ser.to_markdown())
    return db_ser


# %%
for filepath in glob(config.dirs['originals']+'*'):
    try:
        rawfile_data = write_rawfile(filepath)
        print(f'scannned:\t{filepath}')
    # except TypeError as e:
    #     print(f'skipping: {e}')
    except RuntimeError as e:
        print(f'skipping:\t{e}')

# %%
for raw in glob(config.dirs['rawfiles']+'*'):
    kw = dict(channels=1, samplerate=44100, format='RAW', subtype='PCM_16')
    sig, fs = sf.read(raw, **kw)
    break

response = get_shazam_tags(raw)
# %%
# %%
pd.read_pickle(resp_path)
