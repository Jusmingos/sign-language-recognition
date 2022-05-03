# import necessary libraries
import os
import cv2
import numpy as np
import json

import shutil

# dictionary maps glosses to their corresponding frames
all_frames = {}
threshold = 50

# This is the method for splitting all video samples into frames.
def videosToFrames():
    directory = 'videos'
    
    # if the frames directory does not exist, create it
    # if not os.path.exists('frames'):
    #     os.makedirs('frames')
    
    # iterate over the sub directories in videos
    for gloss in os.listdir(directory):
        gloss_frames = [] # frames for all videos in the same gloss

        sub_dir = os.path.join(directory, gloss)
        # iterate over files in the directory
        for filename in os.listdir(sub_dir):
            f = os.path.join(sub_dir, filename) # file path
            if os.path.isfile(f):
                # create a VideoCapture object to read the video
                cap = cv2.VideoCapture(f)
                curr_frames = []

                # get the total number of frames in the video
                total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                print("Total frames for " + filename + " is " + str(total_frames) + " frames.")

                # Loop until the end of the video or until the threshold has been reached
                while (cap.isOpened()):
                    # capture frame by frame, ret will be None if the frame is not valid
                    ret, frame = cap.read()
                    
                    # break if the frame is not valid
                    if not ret:
                        break
                
                    # if total_frames > 50:
                    #     frames_skip = set()
                    #     num_skips = total_frames - threshold
                    #     interval = total_frames // num_skips

                    #     # resize the frame to a smaller size and add it to the list of frames
                    #     frame = cv2.resize(frame, (540, 380), fx=0, fy=0, interpolation=cv2.INTER_CUBIC)
                    #     curr_frame_num = cap.get(cv2.CAP_PROP_POS_FRAMES)

                    #     if (curr_frame_num % interval == 0 and len(frames_skip) <= num_skips):
                    #         frames_skip.add(curr_frame_num)
                    #     else:
                    #     # if (curr_frame_num not in frames_skip):
                    #         curr_frames.append(frame)
                    # else: # if total number of frames less than the threshold
                    curr_frames.append(frame)
                    
                # release the video capture object
                cap.release()
                
                # sample curr_frames to get 50 frames
                sampled_frames = sampling(curr_frames)
                
                # add the selected 50 frames to the list of all frames        
                gloss_frames.append(sampled_frames)

        # if not os.path.exists('frames/' + gloss):
        #     os.makedirs('frames/' + gloss)

        # print("Saving frames for " + filename)

        # # write the frames to the frames directory
        # for i in range(len(gloss_frames)):
        #     for j in range(len(gloss_frames[i])):
        #         # use OpenCv to write the frames to the gloss sub directory
        #         cv2.imwrite('frames/' + gloss + '/' + filename + '_' + str(i) + '.jpg', gloss_frames[i][j])
        
        # add all the frames to the all_frames dictionary
        all_frames[gloss] = gloss_frames
    
    # print("Printing all frames")
    # print(all_frames.keys())

    
    # frame_indices = make_dataset()
    # selected_frames = {}

    # all_frames - key: gloss, value: list of frames
    # frame_indices - key: gloss, value: list of lists (indices)
    # selected_frames - key: gloss, value: list of the selected frames

    # for each gloss in frame indices
    # for gloss, frames_index in frame_indices.items():
    #     selected_video_frames = []
    #     for video_frames_index in range(len(all_frames[gloss])):
    #         selected_video_indices = frames_index[video_frames_index]
    #         all_frames_video = all_frames[gloss][video_frames_index]
    #         selected_frames_video = []
    #         for i in range(len(all_frames_video)):
    #             if i in selected_video_indices: # if the index is in the list of selected indices
    #                 selected_frames_video.append(all_frames_video[i])
            
    #         selected_video_frames.append(selected_frames_video)
            
    #     selected_frames[gloss] = selected_video_frames
    
    # for key, value in selected_frames.items():
    
    #     for i in range(len(value)):
    #         print("Printing the number of frames selected from each video")
    #         print(len(value[i]))

    # # for each video in the dataset
    # for index in range(len(frame_indices)):
    #     # get the selected frames in the video
    #     video_frames = all_frames[index][frame_indices[index]]
    #     # add the selected frames to the list of selected frames
    #     selected_frames.append(video_frames)
    for key, value in all_frames.items():
        for i in range(len(value)):
            print("Printing number of frames")
            print(len(value[i]))

    return all_frames
    
def sampling(curr_frames):
    num_frames = len(curr_frames)
    frames_to_sample = []
    if num_frames > threshold:
        frames_skip = set()
        num_skips = num_frames - threshold
        interval = num_frames // num_skips

        for i in range(num_frames):
            if i % interval == 0 and len(frames_skip) <= num_skips:
                frames_skip.add(i)
        for i in range(num_frames):
            if i not in frames_skip:
                frames_to_sample.append(curr_frames[i])
    else:
        frames_to_sample = list(range(num_frames))
    
    return frames_to_sample

""""
This function loops through all objects in the dataset
and creates a custom data entry for each object. These data entries
are stored in the data list variable. After, it loops
over these data entries and sequentially samples the frames
and stores the indices of all frames in the all_frames list.
"""
# def make_dataset():
#     # store video instances into custom entries
#     data = {}
#     # set the split file
#     split = ['train', 'val']
#     # set the number of samples per video
#     num_samples = 50
#     # store the directory of the videos
#     index_file_path = "./WLASL_v0.3.json"
#     # store the list of all videos
#     all_videos = {}

#     # open the json file and read into content
#     with open(index_file_path, 'r') as f:
#         content = json.load(f)

#      # make dataset using glosses (i.e. words)
#     for gloss_entry in content:
#         # store the gloss and the video instances (there are multiple videos for each gloss)
#         gloss, instances = gloss_entry['gloss'], gloss_entry['instances']

#         # only create entires for desired glosses
#         if (gloss == "hello" or gloss == "world"):
#             gloss_data = []
#             # for each video instance
#             for instance in instances:
#                 # if the video is not in the train split
#                 if instance['split'] not in split:
#                     # skip the video instance
#                     continue
                
#                 # store the frame end and start, as well as the video id
#                 frame_end = instance['frame_end']
#                 frame_start = instance['frame_start']
#                 video_id = instance['video_id']

#                 # store the id, frame start, frame end as an entry in the data list
#                 instance_entry = video_id, frame_start, frame_end
#                 gloss_data.append(instance_entry)

#             data[gloss] = gloss_data
    
#     # go through each gloss and get its frames
#     for index in data.keys():
#         gloss_frames = []
#         # for each data instance in gloss_data
#         for datum in data[index]: 
#             # destructure the data entry stored above
#             video_id, frame_start, frame_end = datum
#             # sequential sampling the frames
#             frames = sequential_sampling(frame_start, frame_end, num_samples)
#             gloss_frames.append(frames)
        
#         all_videos[index] = gloss_frames


#     # go through each video and get its frame samples
    
#     # for index in range(len(data)):
#     #     # destructure the data entry stored above
#     #     video_id, frame_start, frame_end = data[index]
#     #     # sequential sampling the frames
#     #     frames = sequential_sampling(frame_start, frame_end, num_samples)
#     #     # store all the grabbed frames
#     #     all_videos.append(frames)
    
#     # return the list of the indices all frames selected

#     return all_videos
    

# """Keep sequentially ${num_samples} frames from the whole video sequence by uniformly skipping frames."""
# def sequential_sampling(frame_start, frame_end, num_samples):
#     # capture the number of frames in the video
#     num_frames = frame_end - frame_start + 1

#     # store the sampled frames
#     frames_to_sample = []
    
#     # if the number of frames exceeds the threshold number of frames
#     if num_frames > num_samples:
#         # store the number of frames to skip
#         frames_skip = set()

#         # the number of frames to skip is uniformly distributed between 0 and the number of frames
#         num_skips = num_frames - num_samples
#         interval = num_frames // num_skips

#         # for each frame from start to end
#         for i in range(frame_start, frame_end + 1):
#             # store frames to skip uniformly at random
#             if i % interval == 0 and len(frames_skip) <= num_skips:
#                 frames_skip.add(i)

#         # loop through the frames once more and store "non-skipped" frames
#         for i in range(frame_start, frame_end + 1):
#             if i not in frames_skip:
#                 frames_to_sample.append(i)
#     else:
#         # if the number of samples is less than the number of frames, the frames to sample are all the frames
#         frames_to_sample = list(range(frame_start, frame_end + 1))
    
#     # return all the frames to sample
#     return frames_to_sample

if __name__ == '__main__':
    videosToFrames()