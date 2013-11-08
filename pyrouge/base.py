class Doc(object):
    def __init__(self, id, sents=[]):
        self.id = id
        self.sents = sents

    @staticmethod
    def from_see(text):
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(text)
        raw = [(elem.attrs['id'], elem.text) for elem in soup.find_all("a") if 'id' in elem.attrs]
        return Doc(soup.title.text, [Sent(*tup) for tup in raw])

class Sent(object):
    def __init__(self, id, text, tokens=None):
        self.id = id
        self.text = text
        if not tokens:
            self.tokens = text.split(" ")
