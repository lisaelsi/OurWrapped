import json
import os
import requests
import base64
from secrets import SPOTIFY_USER_ID as user_id
from refresh import Refresh
import urllib.parse

# Create new playlist OurWrapped
    # TODO --> set playlist description as usernames of collaborators! 

# For each user

    # Go to user 

    # Go to Wrapped playlist

    # For top three song in Wrapped 

        # Add song to OurWrapped

playlist_name = "Nu är det höst"


def create_playlist():
    # Create playlist on spotify 
    request_body = json.dumps({
        "name": "OurWrapped",
        "description": "OurWrapped",
        "public": True
    })

    query = "https://api.spotify.com/v1/users/{}/playlists".format(
        user_id)
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
        user_id,
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

def get_new_playlists_id(new_playlist_info):
    return(new_playlist_info.get('id'))

def add_track_to_playlist(track_id, playlist_id):
    
    track = 'spotify:track:' + track_id
    print(track)

    track_encoded = urllib.parse.quote(track)
    print(track_encoded)

    #query = "https://api.spotify.com/v1/playlists/{}/tracks?uris=spotify%3Atrack%3A4iV5W9uYEdYUVa79Axb7Rh".format(
    #    playlist_id)
    #response = requests.post(
    #    query,
    #    data='',
    #    headers={
    #        "Content-Type": "application/json",
    #        "Authorization": "Bearer {}".format(token)
    #    }
    #)
    #response_json = response.json()
    #return response_json
    
    
    
    pass


def call_refresh():
    refresh_caller = Refresh()
    print('Token refreshed')
    return(refresh_caller.refresh())
 

if __name__ == '__main__':

    token = call_refresh()

    new_playlist_info = create_playlist()
    #print(new_playlist_info)
    no_of_tracks = 3

    user_playlists = get_user_playlists()
    #print(user_playlists)
    playlist_id = get_user_playlist_id(user_playlists, playlist_name)
    #print(playlist_id)
    track_ids = get_track_ids(no_of_tracks, playlist_id)

    # TODO - later do this for each track
    track_id = track_ids[0]
    # print(track_id)
    
    new_playlist_id = get_new_playlists_id(new_playlist_info)

    add_track_to_playlist(track_id, new_playlist_id)

