import os
import pytest
import json
import urllib.request
import time

domain = os.getenv("DOMAIN", "http://opensuse.stream.stud-srv.sdu.dk")



def test_home():
    start = time.time()
    testing = urllib.request.urlopen(domain + '/service01')
    output = testing.getcode()
    assert 200 == output
    print("The test took " + str(time.time() - start) + " seconds")

def test_getUsers():
    start = time.time()
    testing = urllib.request.urlopen(domain + '/service01/users')
    output = testing.getcode()
    assert 200 == output
    print("The test took " + str(time.time() - start) + " seconds")

def test_get_user_profile():
    start = time.time()
    testing = urllib.request.urlopen(domain + '/service01/users')
    output = testing.read().decode('utf-8')
    
    idstart = output.find("\"")+1
    idend = idstart + 36
    userid = output[idstart:idend]

    testing = urllib.request.urlopen(domain+'/service01/users/'+userid)
    output = testing.read().decode('utf-8')

    assert "_id" in output
    assert "age" in output
    assert "country" in output
    assert "dob" in output
    assert "email" in output
    assert "gender" in output
    assert "name" in output
    print("The test took " + str(time.time() - start) + " seconds")

def test_get_history():
    start = time.time()
    testing = urllib.request.urlopen(domain + '/service01/users')
    users = testing.read().decode('utf-8')

    found = False
    while(not found):
        idstart = users.find("\"")+1
        idend = idstart + 36
        userid = users[idstart:idend]
        url= domain + '/service01/users/'+userid+'/songs'

        testing = urllib.request.urlopen(url)
        output = testing.read().decode('utf-8')
        if(len(output) > 8):
            found=True
        else:
            users = users[idend+2:len(users)]
    global globaluserid
    globaluserid = userid
    #print(globaluserid)
    assert "song" in output
    assert "artist" in output
    assert "genre" in output
    assert "title" in output
    assert "timestamp" in output
    print("The test took " + str(time.time() - start) + " seconds")

def test_get_search_history():
    start = time.time()
    testing = urllib.request.urlopen(domain + '/service01/users')
    users = testing.read().decode('utf-8')

    found = False
    while(not found):
        idstart = users.find("\"")+1
        idend = idstart + 36
        userid = users[idstart:idend]

        testing = urllib.request.urlopen(domain + '/service01/users/'+userid+'/searches')
        output = testing.read().decode('utf-8')
        if(len(output) > 8):
            found=True
        else:
            users = users[idend+2:len(users)]

    assert "searchterm" in output
    assert "timestamp" in output
    print("The test took " + str(time.time() - start) + " seconds")


def test_amount_song_played_by_user():
    start = time.time()
    testing = urllib.request.urlopen(domain + '/service01/users/'+globaluserid+'/songs')
    songs = testing.read().decode('utf-8')
    
    idstart = songs.find("title")+9
    idend = songs.find("}")-5
    songname = songs[idstart:idend]

    songname = songname.replace(" ", "%20")
    global globalsong
    globalsong = songname
 
    testing = urllib.request.urlopen(domain + '/service01/users/'+globaluserid+'/songs/'+songname+'/amount_played')
    output = testing.read().decode('utf-8')
    assert "plays" in output
    print("The test took " + str(time.time() - start) + " seconds")

def test_amount_artist_played_by_user():
    start = time.time()
    testing = urllib.request.urlopen(domain + '/service01/users/'+globaluserid+'/songs')
    songs = testing.read().decode('utf-8')
    
    idstart = songs.find("artist")+10
    idend = songs.find("genre")-11
    artistname = songs[idstart:idend]

    artistname = artistname.replace(" ", "%20")
    global globalartist
    globalartist = artistname
    
    testing = urllib.request.urlopen(domain + '/service01//users/'+globaluserid+'/artists/'+artistname+'/amount_played')
    output = testing.read().decode('utf-8')
    
    assert "plays" in output
    print("The test took " + str(time.time() - start) + " seconds")

def test_amount_song_played():
    start = time.time()
    testing = urllib.request.urlopen(domain + '/service01/songs/'+globalsong+'/amount_played')
    output = testing.read().decode('utf-8')
    assert "plays" in output
    print("The test took " + str(time.time() - start) + " seconds")

def test_artist_amount_played():
    start = time.time()
    testing = urllib.request.urlopen(domain + '/service01/artists/'+globalartist+'/amount_played')
    output = testing.read().decode('utf-8')
    assert "plays" in output
    print("The test took " + str(time.time() - start) + " seconds")


def test_ad_amount_clicked():#/ads/<id>/amount_clicked
    start = time.time()
    testing = urllib.request.urlopen(domain + '/service01/ads')
    output = testing.read().decode('utf-8')
    
    idstart = output.find("_id")+7
    idend = output.find("_index")-9
    adid = output[idstart:idend]

    testing = urllib.request.urlopen(domain + '/service01/ads/'+adid+'/amount_clicked')
    output = testing.read().decode('utf-8')

    assert "clicks" in output
    print("The test took " + str(time.time() - start) + " seconds")


def test_get_top_songs():
    start = time.time()
    testing = urllib.request.urlopen(domain + '/service01/songs/top')
    output = testing.read().decode('utf-8')
    assert "plays" in output
    assert "song" in output
    print("The test took " + str(time.time() - start) + " seconds")

def test_get_top_artists():
    start = time.time()
    testing = urllib.request.urlopen(domain + '/service01/artists/top')
    output = testing.read().decode('utf-8')
    assert "artist" in output
    assert "plays" in output
    print("The test took " + str(time.time() - start) + " seconds")

def test_get_top_artist_for_user():
    start = time.time()
    testing = urllib.request.urlopen(domain + '/service01/users/' +globaluserid+ '/artists/top')
    output = testing.read().decode('utf-8')
    assert "artist" in output
    assert "plays" in output
    print("The test took " + str(time.time() - start) + " seconds")

def test_get_top_songs_for_user():
    start = time.time()
    testing = urllib.request.urlopen(domain + '/service01/users/' +globaluserid+ '/songs/top')
    output = testing.read().decode('utf-8')
    assert "song" in output
    assert "plays" in output
    print("The test took " + str(time.time() - start) + " seconds")

def test_get_top_genres_for_user():
    start = time.time()
    testing = urllib.request.urlopen(domain + '/service01/users/' +globaluserid+ '/genres/top')
    output = testing.read().decode('utf-8')
    assert "genre" in output
    assert "plays" in output
    print("The test took " + str(time.time() - start) + " seconds")

def test_get_namespace_log():
    start = time.time()
    testing05 = urllib.request.urlopen(domain + '/service01/logs/team05')
    testingkube = urllib.request.urlopen(domain + '/service01/logs/kube-system')
    testinglonghorn = urllib.request.urlopen(domain + '/service01/logs/longhorn')
    testingfluent = urllib.request.urlopen(domain + '/service01/logs/fluent')
    testingingress = urllib.request.urlopen(domain + '/service01/logs/ingress-nginx')
    
    output05 = testing05.getcode()
    outputkube = testingkube.getcode()
    outputlonghorn = testinglonghorn.getcode()
    outputfluent = testingfluent.getcode()
    outputingress = testingingress.getcode()
    assert 200 == output05
    assert 200 == outputkube
    assert 200 == outputlonghorn
    assert 200 == outputfluent
    assert 200 == outputingress
    print("The test took " + str(time.time() - start) + " seconds")

def test_get_user_recommendations_songs():
    start = time.time()
    testing = urllib.request.urlopen(domain + '/service01/users/' +globaluserid+ '/recommendation/songs')
    output = testing.getcode()
    assert 200 == output
    print("The test took " + str(time.time() - start) + " seconds")

def test_get_user_recommendations_artists():
    start = time.time()
    testing = urllib.request.urlopen(domain + '/service01/users/' +globaluserid+ '/recommendation/artists')
    output = testing.getcode()
    assert 200 == output
    print("The test took " + str(time.time() - start) + " seconds")

'''
def test_reverse_proxy():
    testing = urllib.request.urlopen(domain + '/service02/visuals/user')
    output = testing.getcode()
    assert 200 == output
    testing = urllib.request.urlopen(domain + '/service02/kibana')
    output = testing.getcode()
    assert 200 == output
'''

'''
def test_data_puller():
    testing = urllib.request.urlopen(domain + '/service03/pullUsers')
    output = testing.getcode()
    assert 200 == output
    #second call to assure output
    testing = urllib.request.urlopen(domain + '/service03/pullUsers')
    output = testing.read().decode('utf-8')
    assert 'Users is up to date' in output
'''
test_ad_amount_clicked()
test_getUsers()
test_get_user_profile()
test_get_history()
test_get_search_history()
test_amount_song_played_by_user()
test_amount_artist_played_by_user()
test_amount_song_played()
test_artist_amount_played()
test_get_top_songs()
test_get_top_artists()
test_get_top_artist_for_user()
test_get_top_songs_for_user()
test_get_top_genres_for_user()
test_get_user_recommendations_songs()
test_get_user_recommendations_artists()
#test_get_namespace_log()
