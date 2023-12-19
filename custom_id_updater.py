class TrackerIDUpdater:
    def __init__(self):
        self.track_dict = {
            "1" : None,
            "2" : None,
            "3" : None,
        }
    
    def reset(self, id):
        is_id_present = False
        for key in self.track_dict.keys():
            if self.track_dict[key] == id:
                is_id_present = True
                break
        
        if is_id_present == False:
            for key in self.track_dict.keys():
                if self.track_dict[key] == None:
                    self.track_dict[key] = id
                    break
        
    def get_updated_track_id(self, deep_sort_id):
        for key in self.track_dict.keys():
            if self.track_dict[key] == deep_sort_id:
                return key
        
        return -1
