class FileEmptyOrUnsupportedType(Exception):
    def __init__(self, url):
        self.str = "File empty or unsupported type: %s" % (url)
    def __str__(self):
        return self.str

