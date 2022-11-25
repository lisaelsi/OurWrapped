import json
import os
import requests
import base64
from secrets import CREATE_PLAYLIST_TOKEN, SPOTIFY_USER_ID, GET_PLAYLIST_TOKEN, GET_TRACKS_TOKEN, CLIENT_SECRET, CLIENT_ID

# Create new playlist OurWrapped
    # TODO --> set playlist description as usernames of collaborators! 

# For each user

    # Go to user 

    # Go to Wrapped playlist

    # For top three song in Wrapped 

        # Add song to OurWrapped

playlist_name = "Nu är det höst"

# ----- copied code ------- #
# Step 1 - Authorization 
url = "https://accounts.spotify.com/api/token"
headers = {}
data = {}

# Encode as Base64
message = f"{CLIENT_ID}:{CLIENT_SECRET}:"
print(message)
messageBytes = message.encode('ascii')
base64Bytes = base64.b64encode(messageBytes)
base64Message = base64Bytes.decode('ascii')

headers['Authorization'] = f"Basic {base64Message}"
data['grant_type'] = "client_credentials"

r = requests.post(url, headers=headers, data=data)

token = r.json()['access_token']


# -------------------------------------------- # 

def create_playlist():
    # Create playlist on spotify 
    request_body = json.dumps({
        "name": "OurWrapped",
        "description": "OurWrapped",
        "public": True
    })

    query = "https://api.spotify.com/v1/users/{}/playlists".format(
        SPOTIFY_USER_ID)
    response = requests.post(
        query,
        data=request_body,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(token)
        }
    )
    response_json = response.json()
    return response_json

def get_user_playlists():
    # TODO - fixa limit och offset
    limit = 5
    offset = 10
    query = "https://api.spotify.com/v1/users/{}/playlists?limit={}&offset={}".format(
        SPOTIFY_USER_ID,
        limit, 
        offset)
    response = requests.get(
        query,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(token)
        }
    )
    response_json = response.json()
    return(response_json)

def get_user_playlist_id(response, playlist_name):
    playlists = response.get('items')
    
    for p in playlists:
        if p.get("name") == playlist_name:
            return(p.get('id'))
    
    print('Playlist not found')
            
        # ------  TODO - error handling ------

def get_tracks_from_playlist(no_of_tracks, playlist_id):
    limit = no_of_tracks
    offset = 10     # TODO - fix hardcoded value

    query = "https://api.spotify.com/v1/playlists/{}/tracks?fields=items(track(id))&limit={}&offset={}".format(
        playlist_id,
        limit,
        offset
    )

    response = requests.get(
        query,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(token)
        }
    )

    return response.json()

def get_track_ids(no_of_tracks, playlist_id):
    tracks_dict = get_tracks_from_playlist(no_of_tracks, playlist_id)
    
    tracks = tracks_dict.get('items')

    track_ids = [item['track']['id'] for item in tracks]

    return track_ids

def get_playlists_id(new_playlist_info):
    print(new_playlist_info.get('id'))

def add_track_to_playlist(track_ids):
    # add track to ourwrapped 
    pass

if __name__ == '__main__':
    new_playlist_info = create_playlist()
    print(new_playlist_info)

    no_of_tracks = 3

    #user_playlists = get_user_playlists()
    #playlist_id = get_user_playlist_id(user_playlists, playlist_name)
    #track_ids = get_track_ids(no_of_tracks, playlist_id)

    #get_playlists_id(new_playlist_info)
