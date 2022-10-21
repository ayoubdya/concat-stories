import os
import subprocess
#from datetime import date

relPath = input("enter relative path : ")
path = os.path.join(os.getcwd(), relPath)
outputName = input("enter output name : ")
durationTime = int(input("enter duration time in secs : "))


def appendList(i, ext, f):
  with open(f'{path}/list-{i}.txt', 'a') as txt:
    filePath = os.path.join(path, f"'{f}'")
    if ext == 'jpg':
      txt.write(f"file {filePath}\nduration {durationTime}\n")
    else:
      txt.write(f"file {filePath}\n")


def renderList(i, ext):
  # ffmpeg -safe 0 -f concat -i list.txt -filter:v "pad=width=max(iw\,ih*(16/9)):height=ow/(16/9):x='((ow-iw)/2)':y='((oh-ih)/2)'" -vcodec libx264 -s 1920x1080 -r 30 out-0.mp4
  listPath = os.path.join(path, f'list-{i}.txt')
  outputPath = os.path.join(path, f'out-{i}.mp4')
  if ext == 'jpg':
    with open(f'{path}/list-{i}.txt', 'r') as txt:
      lines = txt.readlines()
    if len(lines) < 4:
      with open(f'{path}/list-{i}.txt', 'a') as txt:
        txt.write(f"{lines[-2]}\n")
    noAudioOutputPath = os.path.join(path, f'out-{i}-no-audio.mp4')
    subprocess.run(['ffmpeg', '-hwaccel', 'cuda', '-safe', '0', '-f', 'concat', '-i',
                   listPath, '-filter:v', "pad=width=max(iw\,ih*(16/9)):height=ow/(16/9):x='((ow-iw)/2)':y='((oh-ih)/2)'", '-vcodec', 'h264_nvenc', '-s', '1920x1080', '-r', '30', noAudioOutputPath])
    subprocess.run(['ffmpeg', '-i', noAudioOutputPath, '-f', 'lavfi', '-i', 'anullsrc=channel_layout=mono:sample_rate=44100',
                   '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-shortest', outputPath])
  else:
    subprocess.run(['ffmpeg', '-hwaccel', 'cuda', '-safe', '0', '-f', 'concat', '-i',
                   listPath, '-filter:v', "pad=width=max(iw\,ih*(16/9)):height=ow/(16/9):x='((ow-iw)/2)':y='((oh-ih)/2)'", '-vcodec', 'h264_nvenc', '-s', '1920x1080', '-r', '30', outputPath])


def main():
  ls = subprocess.Popen(['ls', '-rt', path], stdout=subprocess.PIPE)
  ll = ls.communicate()[0].decode("utf-8").split('\n')[:-1]
  ll = list(filter(lambda x: x[-3:] in ['jpg', 'mp4'], ll))
  ext = ll[0][-3:]
  i = 0
  for f in ll:
    if f.endswith(ext):
      appendList(i, ext, f)
    else:
      renderList(i, ext)
      ext = f[-3:]
      i += 1
      appendList(i, ext, f)
  renderList(i, ext)
  i += 1

  if i > 1:
    with open(f'{path}/list-final.txt', 'w') as txt:
      text = ''
      for j in range(i):
        text += f'file {path}/out-{j}.mp4\n'
      txt.write(text)
    subprocess.run(['ffmpeg', '-safe', '0', '-f', 'concat', '-i',
                   f'{path}/list-final.txt', '-c', 'copy', outputName])
  else:
    subprocess.run(['mv', f'{path}/out-0.mp4', outputName])


if __name__ == '__main__':
  main()
