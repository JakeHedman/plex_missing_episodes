#coding: utf-8

from datetime import datetime
from opster import command
from plexapi.myplex import MyPlexUser
import getpass
import os
import tvdb_api

@command()
def main():
    tvdb = tvdb_api.Tvdb()
    username = os.environ.get('plex_user') or raw_input("Plex username? ")
    password = os.environ.get('plex_pass') or getpass.getpass("{0} password? ".format(username))

    user = MyPlexUser(username, password)
    servers = user.servers()
    for i, server in enumerate(servers):
        print i, server.name

    server_id = int(os.environ.get('plex_server') or raw_input("Server ID? "))
    print
    server = servers[server_id].connect()

    sections = server.library.sections()
    for i, section in enumerate(sections):
        print i, section.title
    section_id = int(os.environ.get('plex_section') or raw_input("Section ID? "))
    print
    section = sections[section_id]
    shows = {}
    for show in section.all():
        seasons = {}
        for season in show.seasons():
            ep_list = []
            for episode in season.episodes():
                ep_list.append(episode.index)
            seasons[season.index] = ep_list
        shows[show.title] = seasons
#        break
    missing = []
    for show in sorted(shows):
        seasons = shows[show]
        try:
            tvdb_show = tvdb[show]
        except:
            print "Show named \"", show, "\"not found on TVDB"
            continue

        for season in tvdb_show:
            if season == 0:
                continue
            for episode in tvdb_show[season].values():
                e = episode['episodenumber']
                s = episode['seasonnumber']
                fa = episode['firstaired']
#                print episode.keys(), episode.values()
                try:
                    aired = datetime.strptime(fa, "%Y-%m-%d %H:%M:%S")
                except:
                    try:
                        aired = datetime.strptime(fa, "%Y-%m-%d")
                    except:
                        aired = datetime(3000,1,1)
                if aired > datetime.today():
                    continue
                if not e in seasons.get(s, []):
                    missing.append((show, s.zfill(2), e.zfill(2), ))

    if len(missing):
        print "Missing episodes:"
        missing.append(('',0,0),)
        i = 0
        while i < len(missing) - 1:
            miss = missing[i]
            missing_end = missing[i+1:]
            last_inner_miss = None
            succession = 0
            for j, inner_miss in enumerate(missing_end):
                if miss[0] == inner_miss[0] and miss[1] == inner_miss[1] and \
                        (int(miss[2]) + j + 1) == int(inner_miss[2]):
                    succession += 1
                else:
                    if succession > 0:
                        i += succession + 1
                        print u"{0} S{1}E{2} - S{1}E{3}".format(miss[0], miss[1], miss[2], last_inner_miss[2])
                        break
                last_inner_miss = inner_miss
            else:
                print u"{0} S{1}E{2}".format(*miss)
                i += 1
    else:
        print "No missing episodes found!"
