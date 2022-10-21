import os
import subprocess
#from datetime import date

relPath = input("enter relative path : ")
path = os.path.join(os.getcwd(), relPath)
outputName = input("enter output name : ")
durationTime = int(input("enter duration time in secs : "))


def getFullPath(fileName):
  return os.path.join(path, fileName)


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
    if len(lines) < 4:
      with open(listPath, 'a') as txt:
        txt.write(f"{lines[-2]}\n")
    noAudioOutputPath = getFullPath(f'out-{i}-no-audio.mp4')
    subprocess.run(['ffmpeg', '-hwaccel', 'cuda', '-safe', '0', '-f', 'concat', '-i',
                   listPath, '-filter:v', "pad=width=max(iw\,ih*(16/9)):height=ow/(16/9):x='((ow-iw)/2)':y='((oh-ih)/2)'", '-vcodec', 'h264_nvenc', '-s', '1920x1080', '-r', '30', noAudioOutputPath])
    subprocess.run(['ffmpeg', '-i', noAudioOutputPath, '-f', 'lavfi', '-i', 'anullsrc=channel_layout=mono:sample_rate=44100',
                   '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-shortest', outputPath])
  else:
    subprocess.run(['ffmpeg', '-hwaccel', 'cuda', '-safe', '0', '-f', 'concat', '-i',
                   listPath, '-filter:v', "pad=width=max(iw\,ih*(16/9)):height=ow/(16/9):x='((ow-iw)/2)':y='((oh-ih)/2)'", '-vcodec', 'h264_nvenc', '-s', '1920x1080', '-r', '30', outputPath])


def main():
  ls = subprocess.Popen(['ls', '-rt', path], stdout=subprocess.PIPE)
  ls = ls.communicate()[0].decode("utf-8").split('\n')[:-1]
  ls = list(filter(lambda x: x[-3:] in ['jpg', 'mp4'], ll))
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
                   listPath, '-c', 'copy', outputName])
  else:
    subprocess.run(['mv', getFullPath('out-0.mp4'), outputName])


if __name__ == '__main__':
  main()
