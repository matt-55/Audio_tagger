#!/usr/bin/python3

'''
AUDIO FILE TAG MANIPULATION SCRIPT

Version		: V2.1

Date        : 16/07/2016

Author      : matt

Description : 

'''

import argparse
import taglib

# --- Global variables ---
verbLev = 0     # verbose level
verbLev1 = 1    # user messages only
verbLev2 = 2    # include debug messages


# --- Classes ---
class Pair(object):
    def __init__(self, s):
        e = s.split(",")
        
        if len(e) == 2:
            self.first = e[0]
            self.second = e[1]

        else:
            raise ValueError("2 elements expectend but \
            {0} found".format(len(e))) 

        def __str__(self):
            return "{},{}".format(self.first,self.second)

        def __repr__(self):
            return self.__str__()


# --- Functions ---
def print_msg(msg, level):

    if level <= verbLev:
        print(msg)     


def load_tracks(files):
    tracks = []
    
    for f in files:
        try:
            tracks.append(taglib.File(f))
        
        except Exception as e: 
            print_msg("File {} does not exist.\n".format(f), verbLev1)
            print_msg("Load file error: {}\n".format(e), verbLev2)
            pass

    if tracks == []:
        raise Exception("No audio file selected. \n")

    return tracks
            

def read_tag(track, tag):
    print_msg("Processing file: {}".format(track), verbLev1)

    tag = tag.upper()
    
    if tag in track.tags:
        print_msg("\tTag {} value: {} \n".format(tag, track.tags[tag]), verbLev1) 

    else:
        print_msg("\tTrack doesn't contain {} tag\n".format(tag), verbLev1)
            
            

def write_tag(track, tag, value):
    print_msg("Processing file: {}".format(track), verbLev1)

    tag = tag.upper()    
        
    if tag in track.tags:
        cur_val = track.tags[tag]       

        print_msg("\tTag {} changed from {} to {}\n".format(tag, cur_val, value), verbLev1) 

    else:
        print_msg("\tNew tag {} created with value {}\n".format(tag, value), verbLev1)
            
    track.tags[tag] = [value]


def copy_tag(track, fromTag, toTag):
    print_msg("Processing file: {}".format(track), verbLev1)

    fromTag = fromTag.upper()
    toTag = toTag.upper()
        
    if fromTag in track.tags:
        cur_val = track.tags[fromTag]
        
        track.tags[toTag] = track.tags[fromTag]
        print_msg("\tTag {} value {} copied to tag {}\n".format(fromTag, cur_val,toTag), verbLev1)

    else:
        print_msg("\tTrack doesn't contain {} tag\n".format(fromTag), verbLev1)
            


def save_changes(track):
        e = track.save()

        print_msg("\tSave track message: {}\n".format(e), verbLev2) 



def main():
    global verbLev

    parser = argparse.ArgumentParser(description='Audio file tag manipulation')
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('-r', '--read', type=str, help='Read \
    specified tag.')
    action.add_argument('-w', '--write', type=Pair, help='Write value to \
    specified tag, use tag,value format.')
    action.add_argument('-c', '--copy', type=Pair, help='Copy between \
    tags, use from,to format.')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    parser.add_argument('files', nargs="+", help='Audio file(s) to be edited.')

    args = parser.parse_args()

    verbLev = args.verbose

    tracks = load_tracks(args.files)    # load "taglib" tracks from files
    
    
    # READ action
    if args.read:
        for track in tracks:
            verbLev = 1 # force user messages for read
            read_tag(track, args.read)

    # WRITE action
    elif args.write:
        for track in tracks:
            write_tag(track, args.write.first, args.write.second)
            save_changes(track)

    # COPY action
    elif args.copy: 
        for track in tracks:
            copy_tag(track, args.copy.first, args.copy.second)
            save_changes(track)
         


if __name__ == '__main__':
	main()
