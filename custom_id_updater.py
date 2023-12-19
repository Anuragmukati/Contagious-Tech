class TrackerIDUpdater:
    def __init__(self):
        self.track_dict = {
            "1" : None,
            "2" : None,
            "3" : None,
        }
    
    def reset(self, tracks):
        for key in self.track_dict.keys():
            flag = False
            for track in tracks:
                if self.track_dict[key] == track.track_id:
                    flag = True
                    break
            if flag == False:
                self.track_dict[key] = None  
        
        for track in tracks:
            flag = False
            for key in self.track_dict.keys():
                if track.track_id == self.track_dict[key]:
                    flag = True
                    break
            if flag == False:
                for key in self.track_dict.keys():
                    if self.track_dict[key] == None:
                        self.track_dict[key] = track.track_id
                        break
        
    def get_updated_track_id(self, deep_sort_id):
        for key in self.track_dict.keys():
            if self.track_dict[key] == deep_sort_id:
                return int(key)
        
        return -1
