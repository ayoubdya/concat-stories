import ffmpeg
import os

folder_path = input("enter absolute path of the stories folder : ")
ext = '.mp4'
output_file = input("enter output name : ")
DELAY_SEC = 1
RESOLUTION = (480, 852)

input_files = os.listdir(folder_path)
input_files.sort(key=lambda file: os.path.getmtime(
    os.path.join(folder_path, file)))

resolution = RESOLUTION
try:
    probe_file = list(filter(lambda file: file.endswith(ext), input_files))[0]
    probe_file = ffmpeg.probe(os.path.join(folder_path, probe_file))
    resolution = (probe_file['streams'][0]['width'],
                  probe_file['streams'][0]['height'])
except Exception as e:
    print(e)
    pass

input_streams_spread = []

for file in input_files:
    if file.endswith(".mp4"):
        stream = ffmpeg.input(os.path.join(folder_path, file))
        probe = ffmpeg.probe(os.path.join(folder_path, file))
        if len(probe['streams']) < 2:
            empty_audio = ffmpeg.input(
                'anullsrc', f='lavfi', t=probe['streams'][0]['duration'])
            input_streams_spread.extend([stream, empty_audio])
        else:
            input_streams_spread.extend([stream['v'], stream['a']])
    else:
        image = ffmpeg.input(os.path.join(folder_path, file),
                             t=DELAY_SEC, loop=1, framerate=30)
        image = ffmpeg.filter_(image, 'scale', *resolution)
        empty_audio = ffmpeg.input('anullsrc', f='lavfi', t=DELAY_SEC)
        input_streams_spread.extend([image, empty_audio])

joined = ffmpeg.concat(*input_streams_spread, v=1, a=1, unsafe=True).node
ffmpeg.output(joined[0], joined[1], os.path.join(
    "./", output_file + ".mp4")).run()
