import re

class Brain:

    def __init__(self):
        #self.segments=['3002','3003','1234']
        
        self.Segments = {"3002":"wm-lh-caudalanteriorcingulate ",
                         "3003":"wm-lh-caudalmiddlefrontal",
                         "3007":"wm-lh-fusiform"
                        }

        