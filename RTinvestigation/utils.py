






class format:
    def __init__(self):
        pass

    def info2dict(self,info):
        '''convert information content from first line (command line) of the LUT files
           into dict object'''

        info = info.split('-')
        metadata = {}
        yep = 1
        for info_ in info[1:-1]:
            info_ = info_.split()
            try:
                if yep == 0:
                    metadata[meta_prev] = '-' + info_[0]
                else:
                    metadata[info_[0]] = info_[1]
                yep = 1
            except:
                meta_prev = info_[0]
                yep = 0

        return metadata