import os
import re
import subprocess

debug = False
sampleRate = '44100'

typeOfStory = int(
  input("\t[0] snapchat\n\t[1] instagram\nenter type of story : "))
channelLayout = 'stereo'
if typeOfStory == 1:
  channelLayout = 'mono'

path = input("enter absolute path of the stories folder : ")
durationTime = int(input("enter duration time between pictures (sec) : "))
outputName = input("enter output name : ")


def getFullPath(fileName):
  return os.path.join(path, fileName)


def getSampleRate(filePath):
  ffprobe = subprocess.Popen(
      ['ffprobe', filePath], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  # ffprobe prints to stderr wtf -_-
  ffprobe = ffprobe.communicate()[1].decode("utf-8")
  # print('*' * 50 + f'\n{ffprobe}\n' + '*' * 50)
  try:
    rate = re.findall(r"(\d{5}) Hz", ffprobe)[0]
    layout = re.findall(r"Hz, (\w+),", ffprobe)[0]
  except Exception as e:
    print(e)
    return -1, -1
  return rate, layout


def appendList(i, ext, f):
  with open(getFullPath(f'list-{i}.txt'), 'a') as txt:
    filePath = getFullPath(f"'{f}'")
    if ext == 'jpg':
      txt.write(f"file {filePath}\nduration {durationTime}\n")
    else:
      txt.write(f"file {filePath}\n")


def renderList(i, ext):
  # ffmpeg -safe 0 -f concat -i list.txt -filter:v "pad=width=max(iw\,ih*(16/9)):height=ow/(16/9):x='((ow-iw)/2)':y='((oh-ih)/2)'" -vcodec libx264 -s 1920x1080 -r 30 out-0.mp4
  listPath = getFullPath(f'list-{i}.txt')
  outputPath = getFullPath(f'out-{i}.mp4')
  if ext == 'jpg':
    with open(listPath, 'r') as txt:
      lines = txt.readlines()
    if len(lines) <= 4:
      with open(listPath, 'a') as txt:
        txt.write(f"{lines[-2]}\n")
    noAudioOutputPath = getFullPath(f'out-{i}-no-audio.mp4')
    #'-hwaccel', 'cuda'
    subprocess.run(['ffmpeg', '-safe', '0', '-f', 'concat', '-i',
                   listPath, '-filter:v', "pad=width=max(iw\,ih*(16/9)):height=ow/(16/9):x='((ow-iw)/2)':y='((oh-ih)/2)'", '-vcodec', 'h264_nvenc', '-s', '1920x1080', '-r', '30', noAudioOutputPath])
    subprocess.run(['ffmpeg', '-i', noAudioOutputPath, '-f', 'lavfi', '-i', f'anullsrc=channel_layout={channelLayout}:sample_rate={sampleRate}',
                   '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-shortest', outputPath])
  else:
    with open(listPath, 'r') as txt:
      filePathList = [file.replace('file ', '').replace("'", "")
                      for file in txt.read().split('\n')[:-1]]
    text = ''
    for filePath in filePathList:
      if getSampleRate(filePath) == (-1, -1):
        noAudioPath = f"{filePath[:-4]}-na.mp4"
        print(filePath, noAudioPath)
        subprocess.run(['mv', filePath, noAudioPath])
        subprocess.run(['ffmpeg', '-i', noAudioPath, '-f', 'lavfi', '-i', f'anullsrc=channel_layout={channelLayout}:sample_rate={sampleRate}',
                        '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-shortest', filePath])
      if getSampleRate(filePath) != (sampleRate, channelLayout):
        newOutputPath = f"{filePath[:-4]}_mod.mp4"
        subprocess.run(['ffmpeg', '-i', filePath, '-af',
                        f'aformat=channel_layouts={channelLayout},asetrate={sampleRate}', '-c:v', 'copy', newOutputPath])
        text += f"file '{newOutputPath}'\n"
      else:
        text += f"file '{filePath}'\n"
    with open(listPath, 'w') as txt:
      txt.write(text)
    subprocess.run(['ffmpeg', '-hwaccel', 'cuda', '-safe', '0', '-f', 'concat', '-i', listPath, '-filter:v',
                   "pad=width=max(iw\,ih*(16/9)):height=ow/(16/9):x='((ow-iw)/2)':y='((oh-ih)/2)'", '-vcodec', 'h264_nvenc', '-s', '1920x1080', '-r', '30', outputPath])


def main():
  ls = subprocess.Popen(['ls', path], stdout=subprocess.PIPE)
  ls = ls.communicate()[0].decode("utf-8").split('\n')[: -1]
  ls = list(filter(lambda x: x[-3:] in ['jpg', 'mp4'], ls))
  ext = ls[0][-3:]
  i = 0
  for f in ls:
    if f.endswith(ext):
      appendList(i, ext, f)
    else:
      renderList(i, ext)
      ext = f[-3:]
      i += 1
      appendList(i, ext, f)
  renderList(i, ext)

  if i > 0:
    listPath = getFullPath('list-final.txt')
    with open(listPath, 'w') as txt:
      text = ''
      for j in range(i + 1):
        fullPath = getFullPath(f'out-{j}.mp4')
        text += f'file {fullPath}\n'
      txt.write(text)
    subprocess.run(['ffmpeg', '-safe', '0', '-f', 'concat', '-i',
                   listPath, '-c', 'copy', f'{outputName}.mp4'])
  else:
    subprocess.run(['mv', getFullPath('out-0.mp4'), f'{outputName}.mp4'])

  # if not debug:
  #   subprocess.run(f'rm {path}/out-* {path}/list-* {path}/*_mod.mp4')


if __name__ == '__main__':
  main()
