from flask import *
import db_tools as db_tools
from flask_simplelogin import login_required
from account_management import have_access_to_admin
videos=Blueprint('videos',__name__)

@videos.route('/videos')
def video_page():
    # Get the list of videos
    videos = db_tools.get_videos()

    # Remove newlines
    videos = [i.replace(' \n', '') for i in videos]
    # Split videos into a list of sublists, each with two items, the title and the id.
    videos = [i.split('|') for i in videos]

    # A function from chrisalbon.com to break the list into rows
    def break_list(list_to_break, chunk_size):
        for i in range(0, len(list_to_break), chunk_size):

            yield list_to_break[i:i+chunk_size]

    video_master_list = list(break_list(videos, 3))
    # This list is then broken into chunks of three to form rows:
    # [
    #   [
    #       [video0,video0id],
    #       [video1,video1id],
    #       [video2,video2id]
    #   ],
    #   [
    #       [video3,video3id],
    #       [video4,video4id],
    #       [video5,video5id]
    #   ]
    # ]

    return render_template('videos.html', video_master_list=video_master_list)

# The upload form sends its data here.
@videos.route('/videos/newupload', methods=["POST"])
@login_required(must=have_access_to_admin)
def new_video_upload():
    # Title is the title to be shown on jforseth.tech, not the title on youtube.
    title = request.form.get('title')
    # This is the link to the video, not the id.
    # Playlists and youtu.be links are hit or miss.
    youtube_id = request.form.get('youtube_id')

    # If there are any seperators, delete them, they'll break things later.
    title = title.replace('|', '')

    # If the link the user uploaded isn't a youtube link, let them know.
    if 'https://www.youtube.com/watch?v=' not in youtube_id and 'https://youtu.be/' not in youtube_id:
        return "This doesn't look like a YouTube link. Try again."

    # Remove the url part, all we care about is the video id.
    youtube_id = youtube_id.replace('https://www.youtube.com/watch?v=', '')
    youtube_id = youtube_id.replace('https://youtu.be/', '')

    # Get the existing video list.
    video_list = db_tools.get_videos()

    # Take the title and id of the new video and format it for the list.
    newvideo = title+'|'+youtube_id+'\n'

    # Insert it at the top of the list
    video_list.insert(0, newvideo)

    # Write the updated list to the file.
    db_tools.overwrite_videos(video_list)

    # Return to the video page.
    return redirect('../videos')

# The delete button sends the video id it wants deleted here.
@videos.route('/videos/deletion', methods=["POST"])
@login_required(must=have_access_to_admin)
def deletion():
    # This is the id of the youtube video to delete.
    # It is not a URL!
    youtube_id = request.form.get('youtube_id')

    # Read the list of videos.
    video_list = db_tools.get_videos()
    if len(youtube_id) < 12:
        return "This doesn't look like a valid youtube link."
    # This magical line removes videos that have the link requested for deletion.
    # It iterates through the list of videos, discarding any that element with the id that is to be deleted.
    # Note: A malicious request containing only one character may delete multiple videos.
    # MAKE SURE ALL ADMINS ARE TRUSTED.
    video_list = [v for v in video_list if youtube_id not in v]

    # Finally, it overwrites the old list.
    db_tools.overwrite_videos(video_list)
    return redirect('../videos')

# The video rename form sends its data here.
@videos.route('/videos/rename', methods=["POST"])
@login_required(must=have_access_to_admin)
def rename():

    # New title of renamed video
    title = request.form.get('title')

    # This is the id of the youtube video to delete.
    # It is not a URL!
    youtube_id = request.form.get('youtube_id')

    # Again, reads the list of videos.
    video_list = db_tools.get_videos()
    # List comprehensions didn't seem like a good option.
    video_list2 = []
    for i in video_list:

        # Search for the video to be renamed by id.
        if youtube_id in i:
            # Keep the id, throw the old name away.
            _, iyoutube_id = i.split('|')

            # Put new title, old id together, in the proper format.
            video_list2.append(title+'|'+iyoutube_id)
        else:

            # If its not the video we're looking for, don't do anything.
            video_list2.append(i)

    # Basically a list comprehension. Replace the old list with the new one.
    video_list = video_list2

    # Overwrite the old list.
    db_tools.overwrite_videos(video_list)
    # Redirect to video page, should just look like reload.
    return redirect('../videos')

@videos.route('/videos/updateid', methods=["POST"])
@login_required(must=have_access_to_admin)
def update_video_id():

    # Original id of the video.
    old_youtube_id = request.form.get('old_youtube_id')
    # New id of the video.
    new_youtube_id = request.form.get('new_youtube_id')

    # If the user sends a link and not an id, quietly delete the parts that don't matter.
    new_youtube_id = new_youtube_id.replace(
        'https://www.youtube.com/watch?v=', '')
    new_youtube_id = new_youtube_id.replace('https://youtu.be/', '')

    # Read the video list.
    video_list = db_tools.get_videos()

    # TODO: Make this into a list comprehension.
    # Basically, search for the id you want to replace, replace it, write your changes to a new list.
    video_list2 = []
    for video in video_list:
        if old_youtube_id in video:
            i = i.replace(old_youtube_id, new_youtube_id)
        video_list2.append(i)

    # Point the old list to your new one.
    video_list = video_list2

    # Overwrite and reload. You know the drill.
    db_tools.overwrite_videos(video_list)
    return redirect('../videos')

# The move up and move down buttons send data here.
@videos.route('/videos/move', methods=["POST"])
@login_required(must=have_access_to_admin)
def move():
    # This is the EXACT element in the video list. If its not, it'll cause a ValueError.
    video_list_element = request.form.get('element')+'\n'

    # The direction to move the video, 'up' or 'down'
    direction = request.form.get('direction')

    # Again, just reading the video list.
    video_list = db_tools.get_videos()

    # Find the index for the desired element.
    videoindex = video_list.index(video_list_element)

    # Remove the element at that position. Without this line,
    # the video will appear twice, both in the old position, and the new one.
    video_list.pop(videoindex)

    # Now, shift the index by one.
    if direction == 'up':
        # I know subtracting seems counter-intuitive, but remember, index 0 is the top of the list.
        videoindex -= 1
    else:
        # The bigger index, the lower on the list.
        videoindex += 1

    # Insert the element, exactly as it was, in its new position, exactly one higher or one lower.
    video_list.insert(videoindex, video_list_element)

    # Overwrite and refresh.
    db_tools.overwrite_videos(video_list)
    return redirect('../videos')