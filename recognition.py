import numpy as np
from scipy.signal import find_peaks, butter, filtfilt
import pandas as pd
from scipy.stats import linregress

class Recognizer:
    def __init__(self, df):
        # model = YOLO('yolov8n.pt')
        # self.results = model(src, classes = 0, show = True,vid_stride = True, save = True)
        # self.df = self.build_raw_df()

        self.df = df

    def build_raw_df(self):
        x_min_list, y_min_list, x_max_list, y_max_list = [], [], [], []
        for r in self.results:
            boxes = r.boxes
            for box in boxes:
                b = box.xyxy[0] 
                x_min_list.append(b[0].item())
                y_min_list.append(b[1].item())
                x_max_list.append(b[2].item())
                y_max_list.append(b[3].item())

        # Creating a DataFrame from the lists of bounding box coordinates
        df = pd.DataFrame({
            'Xmin': x_min_list,
            'Ymin': y_min_list,
            'Xmax': x_max_list,
            'Ymax': y_max_list
        })

        df['W'] = ((df['Xmax'] - df['Xmin']) / 2).astype(int)
        df['H'] = ((df['Ymax'] - df['Ymin']) / 2).astype(int)
        df['X'] = ((df['Xmax'] + df['Xmin']) / 2).astype(int)
        df['Y'] = ((df['Ymax'] + df['Ymin']) / 2).astype(int)

        return df
    
    def butter_highpass_filter(self, data, cutoff_frequency, sample_rate, order=4):
        nyquist = 0.5 * sample_rate
        normal_cutoff = cutoff_frequency / nyquist
        b, a = butter(order, normal_cutoff, btype='high', analog=False)
        y = filtfilt(b, a, data)
        return y
    
    def extract_peaks(self, y_scaled):
        t = np.arange(0, len(y_scaled))
        signal_data = y_scaled

        # Apply high-pass filter to the signal
        cutoff_frequency = 1.0  # Adjust as needed
        filtered_signal = self.butter_highpass_filter(signal_data, cutoff_frequency, sample_rate=1000)

        # Find peaks in the filtered signal
        threshold = 2
        peaks, _ = find_peaks(filtered_signal, height=threshold)  # Set an appropriate threshold

        if len(peaks) > 0: return True
        else: return False
    
    def detect_activity(self, type, run_threshold = 0.001, jump_threshold = 2.5, crawl_threshold = 2.5):
        if type == 'jump':
            # Calculate the mean of the column
            y_mean = self.df['Y'].mean()
            self.df['jump_signal'] = self.df['Y']

            # Update values less than the mean to be equal to the mean
            self.df.loc[self.df['Y'] < y_mean, 'jump_signal'] = y_mean

            scaled_jump_signal = (self.df['jump_signal'] - self.df['jump_signal'].mean())/self.df['jump_signal'].std()

            return self.extract_peaks(scaled_jump_signal)
        
        elif type == 'crawl':
            ##Crawl Signal
            print("I am crwaling")

            x_mean = self.df['X'].mean()
            self.df['crawl_signal'] = self.df['W']/ self.df['H']

            scaled_crawl_signal = (self.df['crawl_signal'] - self.df['crawl_signal'].mean()) / self.df['crawl_signal'].std()

            return self.extract_peaks(scaled_crawl_signal)
            
        elif type == 'run':
            x, y, w, h  = self.df['X'], self.df['Y'], self.df['W'], self.df['H']

            self.df['running_signal'] = (x + y)/ (w*h)

            scaled_run_signal = (self.df['running_signal'] - self.df['running_signal'].mean()) / self.df['running_signal'].std()
            t = np.arange(0, len(scaled_run_signal))

            slope, intercept, _, _, _ = linregress(t, scaled_run_signal)

            if abs(slope) > run_threshold: return True
            else: return False
        