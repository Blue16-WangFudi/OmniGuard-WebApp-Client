# 删除路径../temp/并创建目录：../temp/
import shutil
import os
from config import *
import cv2
import operator
import numpy as np
from scipy.signal import argrelextrema

# Setting fixed threshold criteria
USE_THRESH = False
# fixed threshold value
THRESH = 0.7
# Setting fixed threshold criteria
USE_TOP_ORDER = False
# Setting local maxima criteria
USE_LOCAL_MAXIMA = True
# Number of top sorted frames
NUM_TOP_FRAMES = 20


def smooth(x, window_len=13, window='hanning'):
    """smooth the data using a window with requested size.

    This method is based on the convolution of a scaled window with the signal.
    The signal is prepared by introducing reflected copies of the signal
    (with the window size) in both ends so that transient parts are minimized
    in the begining and end part of the output signal.

    input:
        x: the input signal
        window_len: the dimension of the smoothing window
        window: the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'
            flat window will produce a moving average smoothing.

    output:
        the smoothed signal

    example:

    import numpy as np
    t = np.linspace(-2,2,0.1)
    x = np.sin(t)+np.random.randn(len(t))*0.1
    y = smooth(x)

    see also:

    numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman, numpy.convolve
    scipy.signal.lfilter

    TODO: the window parameter could be the window itself if an array instead of a string
    """
    print(len(x), window_len)
    if x.ndim != 1:
        raise ValueError("smooth only accepts 1 dimension arrays.")

    if x.size < window_len:
        raise ValueError("Input vector needs to be bigger than window size.")

    if window_len < 3:
        return x

    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError("Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'")

    s = np.r_[2 * x[0] - x[window_len:1:-1],
    x, 2 * x[-1] - x[-1:-window_len:-1]]
    # print(len(s))

    if window == 'flat':  # moving average
        w = np.ones(window_len, 'd')
    else:
        w = getattr(np, window)(window_len)
    y = np.convolve(w / w.sum(), s, mode='same')
    return y[window_len - 1:-window_len + 1]


# Class to hold information about each frame
class Frame:
    def __init__(self, id, frame, value):
        self.id = id
        self.frame = frame
        self.value = value

    def __lt__(self, other):
        if self.id == other.id:
            return self.id < other.id
        return self.id < other.id

    def __gt__(self, other):
        return other.__lt__(self)

    def __eq__(self, other):
        return self.id == other.id and self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)


def rel_change(a, b):
    x = (b - a) / max(a, b)
    print(x)
    return x


def scene_div(video_path, dir, threshold):
    # Video path of the source file
    # video_path = sys.argv[0]
    # Directory to store the processed frames
    # dir = sys.argv[1]
    # smoothing window size
    # len_window = int(sys.argv[3])
    len_window = threshold
    print("Video :" + video_path)
    print("Frame Directory: " + dir)
    cap = cv2.VideoCapture(str(video_path))

    curr_frame = None
    prev_frame = None

    frame_diffs = []
    frames = []
    ret, frame = cap.read()
    i = 1

    while (ret):
        luv = cv2.cvtColor(frame, cv2.COLOR_BGR2LUV)
        curr_frame = luv
        if curr_frame is not None and prev_frame is not None:
            # logic here
            diff = cv2.absdiff(curr_frame, prev_frame)
            count = np.sum(diff)
            frame_diffs.append(count)
            frame = Frame(i, frame, count)
            frames.append(frame)
        prev_frame = curr_frame
        i = i + 1
        ret, frame = cap.read()
    """
        cv2.imshow('frame',luv)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    """
    cap.release()
    # cv2.destroyAllWindows()

    if USE_TOP_ORDER:
        # sort the list in descending order
        frames.sort(key=operator.attrgetter("value"), reverse=True)
        for keyframe in frames[:NUM_TOP_FRAMES]:
            name = "frame_" + str(keyframe.id) + ".jpg"
            cv2.imwrite(dir + "/" + name, keyframe.frame)

    if USE_THRESH:
        print("Using Threshold")
        for i in range(1, len(frames)):
            if (rel_change(np.float64(frames[i - 1].value), np.float64(frames[i].value)) >= THRESH):
                # print("prev_frame:"+str(frames[i-1].value)+"  curr_frame:"+str(frames[i].value))
                name = "frame_" + str(frames[i].id) + ".jpg"
                cv2.imwrite(dir + "/" + name, frames[i].frame)

    if USE_LOCAL_MAXIMA:
        print("Using Local Maxima")
        diff_array = np.array(frame_diffs)
        len_window = int(len(diff_array) / len_window)
        sm_diff_array = smooth(diff_array, len_window)
        frame_indexes = np.asarray(argrelextrema(sm_diff_array, np.greater))[0]
        for i in frame_indexes:
            name = "frame_" + str(frames[i - 1].id) + ".jpg"
            # print(dir+name)
            cv2.imwrite(dir + name, frames[i - 1].frame)

    # plt.figure(figsize=(40, 20))
    # plt.locator_params(nbins=100)
    # plt.stem(sm_diff_array)
    # plt.savefig(dir + 'plot.png')
    # scene_div("../test.mp4", "../temp/", 3)


def init_oss():

    # 阿里云账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM账号进行API访问或日常运维，请登录RAM控制台创建RAM账号。
    auth = oss2.AuthV4(oss_api_key, oss_api_secret)
    # Endpoint以杭州为例，其它Region请按实际情况填写。
    # 填写Bucket名称，例如examplebucket。
    bucket = oss2.Bucket(auth, oss_api_endpoint, oss_api_bucket_name, region=oss_api_region)
    return auth, bucket


def start_task(parameters):
    '''
    获取视频的关键帧
    :param parameters: object_video:视频对象键；folder_frames：视频关键帧在OSS存放的路径
    :return: 帧路径的列表
    '''
    auth, bucket = init_oss()

    # Remove and recreate the temp directory
    temp_dir = './temp/'
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)

    # 获取对象键
    object_video = parameters['object_video']  # 例如testfolder/video.mp4
    folder_frames = parameters['folder_frames']  # 例如testfolder/

    # 根据对象键提取出文件名
    fileName = os.path.basename(object_video)  # Extract file name from path, e.g., "video.mp4"

    # 下载对应视频文件到../temp/{videoname}目录
    # 填写Object完整路径，完整路径中不包含Bucket名称，例如testfolder/exampleobject.txt。
    # 下载Object到本地文件，并保存到指定的本地路径../temp/{fileName}。
    bucket.get_object_to_file(object_video, os.path.join(temp_dir, fileName))

    # 创建目录../temp/frames
    frames_dir = os.path.join(temp_dir, 'frames')
    os.makedirs(frames_dir)
    para1 = str(os.path.join(temp_dir, fileName))
    para2 = temp_dir + "frames/"
    para3 = int(parameters['threshold'])

    # 首先调用scene_div获取视频关键帧，并将其保存到../temp/frames
    scene_div(para1, para2, para3)

    # 遍历文件夹./temp/frames的所有文件（关键帧），并上传识别结果到指定的目录folder_frames中
    frame_paths = []  # List to store all OSS frame paths
    for frame_file in os.listdir(frames_dir):
        local_frame_path = os.path.join(frames_dir, frame_file)
        oss_frame_path = os.path.join(folder_frames, frame_file)  # Upload to specified folder in OSS
        bucket.put_object_from_file(oss_frame_path, local_frame_path)
        frame_paths.append(oss_frame_path)  # Add OSS path to the list

    # Return the list of OSS frame paths
    return {"frame_paths": frame_paths}
