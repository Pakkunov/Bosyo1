from django.contrib.staticfiles.storage import ManifestStaticFilesStorage
import time


class CustomStaticFilesStorage(ManifestStaticFilesStorage):
    def hashed_name(self, name, content=None, filename=None):
        # generate a unique hash for the file name
        hash = super().hashed_name(name, content, filename)
        # append a timestamp to the hash to ensure uniqueness
        timestamp = str(int(time.time()))
        return f"{hash}-{timestamp}"
