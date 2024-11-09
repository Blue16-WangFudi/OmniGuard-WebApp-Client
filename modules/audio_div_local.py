import uuid

from moviepy.editor import VideoFileClip
from config import *
import oss2
import shutil
import os


def init_oss():
    # 阿里云账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM账号进行API访问或日常运维，请登录RAM控制台创建RAM账号。
    auth = oss2.AuthV4(oss_api_key, oss_api_secret)
    # Endpoint以杭州为例，其它Region请按实际情况填写。
    # 填写Bucket名称，例如examplebucket。
    bucket = oss2.Bucket(auth, oss_api_endpoint, oss_api_bucket_name, region=oss_api_region)
    return auth, bucket


def start_task(parameters: dict) -> dict:
    # 删除路径../temp/并创建目录：../temp/
    # Remove and recreate the temp directory
    temp_dir = '../temp/'
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
    auth, bucket = init_oss()
    # 根据对象键提取出文件名
    fileName = os.path.basename(parameters['video'])  # Extract file name from path, e.g., "video.mp4"
    bucket.get_object_to_file(parameters['video'], os.path.join(temp_dir, fileName))
    video = VideoFileClip(os.path.join(temp_dir, fileName))
    audio = video.audio
    if audio is not None:
        audio.write_audiofile(os.path.join(temp_dir, "audio.mp3"))
        oss_frame_path = os.path.join("video/audio/", str(uuid.uuid4()) + ".mp3")
        bucket.put_object_from_file(oss_frame_path, os.path.join(temp_dir, "audio.mp3"))
        # Upload to specified folder in OSS
        return {"path": oss_frame_path}
    else:
        return {"path": None}
