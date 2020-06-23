import random

from flask import *
from flask_simplelogin import login_required, get_username, is_logged_in

from account_management import have_access_to_admin, get_current_access

videos = Blueprint("videos", __name__)


def get_videos(videotitle=None, videoid=None):
    # videotitle|videoid
    with open("text/videos.txt", "r") as file:
        videos = file.readlines()
    videos = [i.replace("\n", "") for i in videos]
    videos = [i.split("|") for i in videos]
    if videotitle:
        for i in videos:
            pass
            #print(i[0], videotitle)
        return [i for i in videos if i[0] == videotitle][0]
    if videoid:
        return [i for i in videos if i[0] == videoid][0]
    return videos


def overwrite_videos(video_list):
    video_list = ["|".join(i) + "\n" for i in video_list]
    with open("text/videos.txt", "w") as file:
        file.writelines(video_list)


@videos.route("/videos")
def video_page():
    videos = get_videos()
    # This doesn't actually do anything.
    # As long as the number is a multiple of 3,
    # or greater than the total number of videos
    # it works.
    VIDEOS_PER_ROW = 3
    video_master_list = []
    for i in range(0, len(videos), VIDEOS_PER_ROW):
        video_master_list.append(videos[i : i + VIDEOS_PER_ROW])

    return render_template("videos/videos.html", video_master_list=video_master_list)


@videos.route("/videos/newupload", methods=["POST"])
@login_required(must=have_access_to_admin)
def new_video_upload():
    title = escape(request.form.get("title"))
    title = title.replace("|", "")

    youtube_id = request.form.get("youtube_id")
    if (
        "https://www.youtube.com/watch?v=" not in youtube_id
        and "https://youtu.be/" not in youtube_id
    ):
        flash("This doesn't look like a YouTube link. Try again.", category="warning")
        return redirect("/videos")
    youtube_id = youtube_id.replace("https://www.youtube.com/watch?v=", "")
    youtube_id = youtube_id.replace("https://youtu.be/", "")

    newvideo = [title, youtube_id]

    video_list = get_videos()
    video_list.insert(0, newvideo)

    overwrite_videos(video_list)
    return redirect("../videos")


@videos.route("/videos/deletion", methods=["POST"])
@login_required(must=have_access_to_admin)
def deletion():
    youtube_id = request.form.get("youtube_id")

    video_list = get_videos()
    if len(youtube_id) < 11:
        flash("This doesn't look like a YouTube link. Try again.", category="warning")
        return redirect("/videos")

    video_list = [video for video in video_list if youtube_id not in video]

    overwrite_videos(video_list)
    return redirect("../videos")


@videos.route("/videos/rename", methods=["POST"])
@login_required(must=have_access_to_admin)
def rename():
    new_title = escape(request.form.get("title"))
    youtube_id = request.form.get("youtube_id")
    video_list = get_videos()

    video_list2 = []
    for video in video_list:

        if youtube_id in video:
            current_videos_id = video[1]
            # Put new title, old id together, in the proper format.
            video_list2.append([new_title, current_videos_id])

        else:
            # If its not the video we're looking for, don't do anything.
            video_list2.append(video)
    video_list = video_list2
    overwrite_videos(video_list)
    return redirect("../videos")


@videos.route("/videos/updateid", methods=["POST"])
@login_required(must=have_access_to_admin)
def update_video_id():
    old_youtube_id = request.form.get("old_youtube_id")
    new_youtube_id = request.form.get("new_youtube_id")

    new_youtube_id = new_youtube_id.replace("https://www.youtube.com/watch?v=", "")
    new_youtube_id = new_youtube_id.replace("https://youtu.be/", "")

    video_list = get_videos()

    video_list = [
        [video[0], video[1].replace(old_youtube_id, new_youtube_id)]
        for video in video_list
    ]

    overwrite_videos(video_list)
    return redirect("../videos")


@videos.route("/videos/move", methods=["POST"])
@login_required(must=have_access_to_admin)
def move():
    video_to_move = request.form.get("element").split("|")
    direction = escape(request.form.get("direction"))

    video_list = get_videos()

    index_of_video = video_list.index(video_to_move)

    video_list.pop(index_of_video)

    if direction == "up":
        # I know subtracting seems counter-intuitive. The lower the number, the higher the position.
        index_of_video -= 1
    else:
        index_of_video += 1

    video_list.insert(index_of_video, video_to_move)

    overwrite_videos(video_list)
    return redirect("../videos")


@videos.route("/videos/video/<video>")
def individual_video_page(video):
    try:
        video = get_videos(video)
    except IndexError:
        return redirect("/videos")
    videos = get_videos()
    random.shuffle(videos)
    return render_template("/videos/individual_video.html", video=video, videos=videos)
