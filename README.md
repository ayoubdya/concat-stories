concatenate snapchat public stories or instagram stories into one video with FFmpeg

### Installation

```
$ git clone https://github.com/ayoubdya/concat-stories.git
$ cd concat-stories/
$ bash setup.sh
```

### Snapchat

```
$ cd snapchat/
$ source venv/bin/activate
$ snapchat-dl daviddobrik
$ deactivate
```

### Instagram

```
$ cd instagram/
$ source venv/bin/activate
$ python pyinstastories.py -nt -ta -u <YOUR_USERNAME> -p <YOUR_PASS> -d justinbieber
$ deactivate
```

### Usage

```
$ python concat.py
```
