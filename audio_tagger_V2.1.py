#!/usr/bin/python3

'''
AUDIO FILE TAG MANIPULATION SCRIPT

Version		: V2.1

Date        : 14/07/2016

Author      : matt

Description : 

'''

import argparse
import taglib

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


def load_tracks(files, verbose):
    tracks = []
    
    for file in files:
        try:
            tracks.append(taglib.File(file))
        
        except Exception as e: 
            if verbose:
                print(e)
            pass

    if tracks == []:
        raise Exception("No audio file in selected directory. \n")

    return tracks
            

def read_tag(track, tag, verbose):
    print("Processing file: {}".format(track))

    tag = tag.upper()
    
    if tag in track.tags:
        print("\tTag {} value: {} \n".format(tag, track.tags[tag])) 

    else:
        print("\tTrack doesn't contain {} tag\n".format(tag))
            
            

def write_tag(track, tag, value, verbose):
    print("Processing file: {}".format(track))

    tag = tag.upper()    
        
    if tag in track.tags:
        cur_val = track.tags[tag]       

        print("\tTag {} changed from {} to {}\n".format(tag, cur_val, value)) 

    else:
        print("\tNew tag {} created with value {}\n".format(tag, value))
            
    track.tags[tag] = [value]


def copy_tag(track, fromTag, toTag, verbose):
    print("Processing file: {}".format(track))

    fromTag = fromTag.upper()
    toTag = toTag.upper()
        
    if fromTag in track.tags:
        cur_val = track.tags[fromTag]
        
        track.tags[toTag] = track.tags[fromTag]
        print("\tTag {} value {} copied to tag {}\n".format(fromTag, cur_val,toTag))

    else:
        print("\tTrack doesn't contain {} tag\n".format(fromTag))
            


def save_changes(track, verbose):
        e = track.save()

        if verbose:
            print(e) 



def main():

    parser = argparse.ArgumentParser(description='Audio file tag manipulation')
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('-r', '--read', type=str, help='Read \
    specified tag.')
    action.add_argument('-w', '--write', type=Pair, help='Write value to \
    specified tag, use tag,value format.')
    action.add_argument('-c', '--copy', type=Pair, help='Copy between \
    tags, use from,to format.')

    parser.add_argument('--verbose', action='store_true', \
    help='Show system messages.')
    parser.add_argument('files', nargs="+", help='Audio file(s) to be edited.')

    args = parser.parse_args()

    tracks = load_tracks(args.files, args.verbose)    # load "taglib" tracks from files
    
    print("\n")    
    
    # READ action
    if args.read:
        for track in tracks:
            read_tag(track, args.read, args.verbose)        

    # WRITE action
    elif args.write:
        for track in tracks:
            write_tag(track, args.write.first, args.write.second, args.verbose)
            save_changes(track, args.verbose)

    # COPY action
    elif args.copy: 
        for track in tracks:
            copy_tag(track, args.copy.first, args.copy.second, args.verbose)
            save_changes(track, args.verbose)
         


if __name__ == '__main__':
	main()
