# Author: Alexander Decurnou
# Team: iDev

from glob import glob
from os import makedirs
from os.path import join, basename, splitext, expanduser, abspath
import json

PROJECTS_DIR = join(".", "projects")
WATSON_CREDENTIALS = "watson_creds.json"
FULL_TRANSCRIPT_BASENAME = 'full-transcript.txt'
DEFAULT_AUDIO_SEGMENT_DURATION_SEC = 180


class Project:
    # Set the project slug to the filename of the video
    def __init__(self, filename, flag_no_seg, flag_multi, flag_audio_only, flag_give_alts):
        self.abspath = abspath(filename)
        self.filename = str(filename)
        self.slug = splitext(basename(filename))[0]
        self.audio_dest = str(self.slug + ".webm")
        self.flag_audio_only = flag_audio_only
        self.flag_no_seg = flag_no_seg
        self.flag_multi = flag_multi
        self.flag_give_alts = flag_give_alts

        #if not flag_no_seg and seg_length > 0:
        #    self.seg_length = seg_length
        #else:
        #    self.seg_length = DEFAULT_AUDIO_SEGMENT_DURATION_SEC

    def _make_proj_dir(self):
        """
        This will take the project's slug and expand to the full path. It will
        then attempt to create a directory for the project. exist_ok is set to
        True as it will not wipe the directory if it already exists, which is
        fine in my case
        """
        xslug = self.slug.replace("projects/", "").rstrip('/')
        try:
            self.path = join(PROJECTS_DIR, xslug)
            self.path = abspath(expanduser(self.path))
            makedirs(self.path, exist_ok=True)
            print("Project directory " + self.slug + " created.")
        except OSError as ex:
            if ex.errno != errno.EEXIST:
                print("Project directory cannot be created!")
                raise

    # Same as make_proj_dir, only it creates a subfolder in the project folder
    def _audio_seg_dir(self):
        try:
            self.audio_seg_path = join(self.path, "audio_seg")
            makedirs(self.audio_seg_path, exist_ok=True)
            print("Audio segement directory for project created.")
        except OSError as ex:
            if ex.errno != errno.EEXIST:
                print("Audio segment directory cannot be created!")
                raise

    # Seems to be a pattern here.
    def _transcripts_dir(self):
        try:
            self.trans_path = join(self.path, "transcripts")
            makedirs(self.trans_path, exist_ok=True)
            print("Transcript directory for project created.")
            self.full_transcript_path = join(self.path, FULL_TRANSCRIPT_BASENAME)
        except OSError as ex:
            if ex.errno != errno.EEXIST:
                print("Transcript directory cannot be created!")
                raise

    # Easy way to create the required folders
    def create_req_paths(self):
        self._make_proj_dir()

        # Only create the segment folder if the no_segment flag is false
        if not self.flag_no_seg:
            self._audio_seg_dir()

        self._transcripts_dir()

    # This will create a list of each of the audio segments found in a project.
    def segment_names(self):
        self.seg_list = glob(join(self.audio_seg_path, '*.webm'))
        print("Segment list created.")

    # This will create a list of each of the transcripts in a project folder
    def transcript_names(self):
        self.trans_list = glob(join(self.trans_path, '*.json'))
        if not self.flag_no_seg:
            self.trans_list = sorted(self.trans_list, key=lambda x: int(basename(x).split('-')[0]))

    # This will load the credentials for the Bluemix service
    def get_credentials(self, filename=WATSON_CREDENTIALS):
        with open(filename, 'r') as f:
            self.data = json.load(f)
