import re

from url import Url

PICTURE = "Picture"
READING = "Reading"
VIDEO = "Video"

pictureFileTypes = ('.gif', '.jpeg', '.jpg', '.png')
pictureDomain = ('flickr.com', 'imgur.com', 'i.imgur.com', 'i.minus.com', "minus.com",  'qkme.me', 'quickmeme.com')
videoDomains = ('vimeo.com', 'youtube.com')
videoRegExs = [re.compile("\[video\]$", re.IGNORECASE), re.compile("^Video:", re.IGNORECASE), re.compile("\(VIDEO\)$")]


class Item:
    @staticmethod
    def __videoTitleRegExMatch__(title):
        for r in videoRegExs:
            if(r.match(title)):
                return True
        return False


    def __classify__(self):
        result = None
        domain = self.url.getDomain()
        fileType = self.url.getFileType()

        if(fileType in pictureFileTypes):
            result = PICTURE
        elif((domain in videoDomains) or (Item.__videoTitleRegExMatch__(self.title))):
            result = VIDEO
        elif(domain in pictureDomain):
            result = PICTURE
        else: 
            # Assume it's a READING
            result = READING

        return result


    def __init__(self, id, url, title, source):
        self.id = id
        self.url = Url(url)
        self.title = title
        self.source = source
        self.linkType = self.__classify__()


    def __repr__(self):
        return "<Item(%d, %s, %s, %s)>" % (self.id, self.title.encode('ascii', 'ignore'), self.url, self.source)
