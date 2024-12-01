import ffmpeg
import os
from loguru import logger

RESOLUTION = (480, 852)
EXT = ".mp4"
FRAMERATE = 30


class ConcatStories:
  def __init__(self, dir_name: str, output: str, loop_duration_image: int = 1, is_quiet: bool = True):
    self.dir_name = dir_name
    stories = os.listdir(self.dir_name)
    stories.sort(key=lambda file: os.path.getmtime(os.path.join(self.dir_name, file)))
    self.stories = stories
    self.output = output
    self.resolution = RESOLUTION
    self.loop_duration_image = loop_duration_image
    self.is_quiet = is_quiet
    try:
      probe_file = list(filter(lambda file: file.endswith(EXT), stories))[0]
      probe_file = ffmpeg.probe(os.path.join(self.dir_name, probe_file))
      self.resolution = (probe_file['streams'][0]['width'], probe_file['streams'][0]['height'])
    except Exception as e:
      print(e)

  def concat(self):
    input_streams_spread = []

    for file in self.stories:
      if file.endswith(".mp4"):
        stream = ffmpeg.input(os.path.join(self.dir_name, file))
        probe = ffmpeg.probe(os.path.join(self.dir_name, file))
        if len(probe['streams']) < 2:
          empty_audio = ffmpeg.input(
              'anullsrc', f='lavfi', t=probe['streams'][0]['duration'])
          input_streams_spread.extend([stream, empty_audio])
        else:
          input_streams_spread.extend([stream['v'], stream['a']])
      else:
        image = ffmpeg.input(os.path.join(self.dir_name, file), t=self.loop_duration_image, loop=1, framerate=FRAMERATE)
        image = ffmpeg.filter_(image, 'scale', *self.resolution)
        empty_audio = ffmpeg.input('anullsrc', f='lavfi', t=self.loop_duration_image)
        input_streams_spread.extend([image, empty_audio])

    joined = ffmpeg.concat(*input_streams_spread, v=1, a=1, unsafe=True).node
    loglevel = "quiet" if self.is_quiet else "info"
    ffmpeg.output(joined[0], joined[1], os.path.join(".", self.output + ".mp4"), loglevel=loglevel).run()
    logger.info(f"Stories concatenated to {self.output}.mp4")
