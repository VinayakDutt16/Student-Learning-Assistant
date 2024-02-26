# youtube_suggestor.py

from googleapiclient.discovery import build

def suggest_youtube_video_based_on_hobby(api_key, hobby):
    youtube = build("youtube", "v3", developerKey=api_key)

    # Search for videos based on the user's hobby
    search_response = youtube.search().list(
        q=hobby,
        type="video",
        part="id, snippet",
        maxResults=10
    ).execute()

    # Check if there are any search results
    if "items" not in search_response or not search_response["items"]:
        return None

    # Extract the first video from the search results
    video_info = search_response["items"][0]["snippet"]

    # Extract the video title
    video_title = video_info.get("title", "No Title Available")

    # Extract the video ID and thumbnail URL
    video_id = search_response["items"][0]["id"]["videoId"]
    thumbnail_url = video_info["thumbnails"]["medium"]["url"]

    # Construct the YouTube video URL
    video_url = f"https://www.youtube.com/watch?v={video_id}"

    return {"title": video_title, "thumbnail_url": thumbnail_url, "video_url": video_url}
