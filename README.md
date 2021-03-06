# transcript-helper
A utility that uses IBM's Bluemix Speech-to-Text service to assist in adding transcripts to videos in order to maintain ADA compliance at a particular institution of higher learning. Basically, it makes my job easier.

## Getting Started
### Requirements
You will need the following packages, which can easily be installed using your favorite Python package manager. The exception to this is ffmpeg, which can just as easily be installed to your system. Note that it will need to be built/installed with libvorbis; on a Mac, this can be done through Homebrew by running `brew install libvpx libvorbis` and then `brew install ffmpeg --with-libvpx --with-libvorbis`.
```
moviepy
requests
spacy
youtube-dl
```

You will also need an account with IBM's Bluemix service. After creating an account, generate credentials for the Speech-to-Text service and save them in a file called `watson_creds.json`, which is to be placed in the root directory of the repository.

### Modifications
You may want to change a few of the default options in the `audio_op.py` module found in the stuff folder. Please refer to the Bluemix API documentation for more information.

## Usage
1. Download the video to be transcribed using youtube-dl.
  + Right now, the code takes the video as an MP4. Feel free to change it or use the following snippet to download the video in the correct format: `youtube-dl -f mp4 -o *output_file.mp4* *full_YouTube_url*`
2. Run `python main.py [OPTIONS] *video_file*`

There are a number of flags available to change the flow of the utility. They are as follows:
  + audio-only `-a`: use when there is only audio (no video) supplied
  + multiple speaker detection `-m`: enable multi-speaker detection
  + no segmentation `-ns`: process audio in one file, instead of segments (more information below)

And that's it! The utility will create all the folders needed to organize the intermediary data. It will extract and segment the audio according to the defined parameters, and then send the segments for transcription to the Bluemix API, according to the options you define. An SRT file with timestamps and all _should_ be written to the project directory.

## TODO
+ Design algorithm using spaCy NLP module that will flag "out-of-place" words (hopefully in less than O(n^2 ) time)

## Additional Information
### libvorbis
Originally, the utility formatted the audio as WAV files to send to the Bluemix service. However, the service institutes a 100 MB restriction for non-streaming transcription. As WAV is a lossless format, the size of certain files became an issue, even at smaller lengths. The ability to use audio-only webms was introduced in a recent update. Some crude testing showed that the use of webms and the libvorbis codec cut the file size by about 85-90%.

### Segmentation: Speed vs. Accuracy
The documentation indicates that the accuracy of a transcription process improves as the length of the provided audio file/stream increases. The segmentation option allows one to use multithreading to send all of the segments to the service at the same time, which decreases the total transcription time to the length of the longest segment. Thus, there is a tradeoff between speed and accuracy. Hypothetically, the most accurate transcription will be one in which the entire audio file is passed to the service. The fastest transcription will be one in which segments are very short.
