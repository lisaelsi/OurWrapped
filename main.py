import json
import os
import requests
import base64
from secrets import SPOTIFY_USER_ID as key_user
from refresh import Refresh
import urllib.parse
import random

def create_playlist(user, token):
    # Create playlist on spotify 
    request_body = json.dumps({
        "name": "OurWrapped",
        "description": "OurWrapped",
        "public": True
    })

    query = "https://api.spotify.com/v1/users/{}/playlists".format(
        user)
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

def get_user_playlists(user, token):
    limit = 10
    offset = 0    
    query = "https://api.spotify.com/v1/users/{}/playlists?limit={}&offset={}".format(
        user,
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
            print(id)

    print('Playlist not found')

        # ------  TODO - error handling ------

def get_tracks_from_playlist(no_of_tracks, playlist_id, token):
    limit = no_of_tracks
    offset = 0    

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

def get_track_ids(no_of_tracks, playlist_id, token):
    tracks_dict = get_tracks_from_playlist(no_of_tracks, playlist_id, token)

    tracks = tracks_dict.get('items')

    track_ids = [item['track']['id'] for item in tracks]

    return track_ids

def get_new_playlists_id(new_playlist_info):
    return(new_playlist_info.get('id'))

def encode_tracks(track_ids):
    
    encoded_tracks = ''

    for t_id in track_ids:
        track = 'spotify:track:' + t_id + ','
        track_encoded = urllib.parse.quote(track)
        encoded_tracks = encoded_tracks + track_encoded
    
    return encoded_tracks

def add_tracks(track_ids, playlist_id, token):

    random.shuffle(track_ids)

    tracks = encode_tracks(track_ids)
    query = "https://api.spotify.com/v1/playlists/{}/tracks?uris={}".format(
        playlist_id,
        tracks)
    response = requests.post(
        query,
        data='',
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(token)
        }
    )

def call_refresh():
    refresh_caller = Refresh()
    print('Token refreshed')
    return(refresh_caller.refresh())
 

def main():

    token = call_refresh()

    input_users = input("Enter usernames: ")

    users = input_users.split()

    # Select playlist to get songs from
    playlist_name = input("Input playlist name: ")

#    # Create OurWrapped playlist
    new_playlist_info = create_playlist(key_user, token)

#    # Get id of newly created playlist 
    new_playlist_id = get_new_playlists_id(new_playlist_info)

#    # Determines number of tracks to select
    no_of_tracks = input("Enter number of tracks: ")

    # For each user 
    for user in users:

        # Gets users playlists
        user_playlists = get_user_playlists(user, token)
 
        # Gets playlist id of selected playlist 
        playlist_id = get_user_playlist_id(user_playlists, playlist_name)

        # Gets tracks ids from selected playlist 
        track_ids = get_track_ids(no_of_tracks, playlist_id, token)
    
        # Add tracks to newly created playlist
        add_tracks(track_ids, new_playlist_id, token)


if __name__ == '__main__':
    main()