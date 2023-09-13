"""
Reduces the volume of the song.
"""

from pydub import AudioSegment

def computeDbToReduce(song):
    """
    Computes decibel count to reduce.
    """

    CONST_DB_REDUCE_MULTIPLIER = 0.891229
    rms = song.rms
    if rms <= 5000:
        return 0

    dbToReduce = 0
    while rms > 5000:
        rms *= CONST_DB_REDUCE_MULTIPLIER
        dbToReduce += 1
    return (dbToReduce - 1)

def reduceVolume(path):
    """
    Downloads the song from PC using its path.
    Reduces its volume.
    Saves it on PС.
    """

    song = AudioSegment.from_mp3(path)
    dbRoReduce = computeDbToReduce(song)
    if dbRoReduce > 0:
        song -= dbRoReduce
        song.export(path, 'mp3')
