from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_HTML(string_with_HTML):
    s = MLStripper()
    s.feed(string_with_HTML)
    return s.get_data()