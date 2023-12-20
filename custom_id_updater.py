class TrackerIDUpdater:
    def __init__(self):
        self.track_dict = {
            "1" : None,
            "2" : None,
            "3" : None,
        }
    
    def reset(self, tracks):
        track_ids = list(map(lambda track: track.track_id, tracks))
        track_dict_ids = list(self.track_dict.values())
        
        if set(track_ids) != set(track_dict_ids):
        
            # Check if previous id in track dict missing in current track_ids
            for key in self.track_dict.keys():
                if self.track_dict[key] != None and self.track_dict[key] not in track_ids:
                    self.track_dict[key] = None
            
            # Check if an id in current track_ids was absent in previous ids
            for id in track_ids:
                if id not in track_dict_ids:
                    for key in self.track_dict.keys():
                        if self.track_dict[key] is None:
                            self.track_dict[key] = id
                            break
            
        # for key in self.track_dict.keys():
        #     flag = False
        #     for track in tracks:
        #         if self.track_dict[key] == track.track_id:
        #             flag = True
        #             break
        #     if flag == False:
        #         self.track_dict[key] = None  
        
        # for track in tracks:
        #     flag = False
        #     for key in self.track_dict.keys():
        #         if track.track_id == self.track_dict[key]:
        #             flag = True
        #             break
        #     if flag == False:
        #         for key in self.track_dict.keys():
        #             if self.track_dict[key] == None:
        #                 self.track_dict[key] = track.track_id
        #                 break
        
    def get_updated_track_id(self, deep_sort_id):
        for key in self.track_dict.keys():
            if self.track_dict[key] == deep_sort_id:
                return int(key)
        
        return -1
