#!/usr/bin/python3

'''
AUDIO FILE TAG MANIPULATION SCRIPT

Version		: V2.0

Date        : 13/07/2016

Author      : matt

Description : 

'''

import argparse
import taglib

def PairWithDefault(default):
    class Pair(object):
        def __init__(self, s):
            e = s.split(",")
            
            if len(e) == 1:
                self.first = e[0].upper()
                self.second = default
            
            elif len(e) == 2:
                self.first = e[0].upper()
                self.second = e[1].upper()

            else:
                raise ValueError("1 or 2 elements expectend but \
                {0} found".format(len(e))) 

        def __str__(self):
            return "{},{}".format(self.first,self.second)

        def __repr__(self):
            return self.__str__()

    return Pair


def check_tag(track, tag):
    if tag in track.tags:
        return True

    else:
        return False

 
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
    
    if check_tag(track, tag):
        print("    Tag {} value: {}".format(tag, track.tags[tag])) 
        print("\n")

    else:
        print("     Track doesn't contain {} tag".format(tag))
        print("\n")
            
            

def write_tag(track, tag, value, verbose):
    print("Processing file: {}".format(track))
        
    if check_tag(track, tag):
        cur_val = track.tags[tag]       

        print("    Tag {} changed from {} to {}".format(tag, cur_val, value)) 
        print("\n")

    else:
        print("     New tag {} created with value {}".format(tag, value))
        print("\n")
            
    track.tags[tag] = [value]


def copy_tag(track, fromTag, toTag, verbose):

    print("Processing file: {}".format(track))
        
    if check_tag(track, fromTag):
        cur_val = track.tags[fromTag]
        
        track.tags[toTag] = track.tags[fromTag]
        print("    Tag {} value {} copied to tag {}".format(fromTag, cur_val,toTag))
        print("\n")

    else:
        print("     Track doesn't contain {} tag".format(fromTag))
        print("\n")
            


def save_changes(track, verbose):
        e = track.save()

        if verbose:
            print(e) 



def main():

    PairA = PairWithDefault("COMMENT")


    parser = argparse.ArgumentParser(description='Audio file tag manipulation')
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--read', type=PairA, help='Read specified tag.')
    action.add_argument('--write', type=PairA, help='Write specified \
    tag.')
    action.add_argument('--copy', type=PairA, help='Copy between tags,\
    use from,to format; defaul for to is "COMMENT".')

    parser.add_argument('--val', type=str, help='Value to be written to tag.')
    parser.add_argument('--verbose', action='store_true', \
    help='Show system messages.')
    parser.add_argument('files', nargs="+", help='Audio file(s) to be edited.')

    args = parser.parse_args()

    tracks = load_tracks(args.files, args.verbose)    # load "taglib" tracks from files
    
    print("\n")    
    
    # READ action
    if args.read is not None:
        for track in tracks:
            read_tag(track, args.read.first, args.verbose)        

    # WRITE action
    elif args.write is not None:
        if args.val is not None:
            for track in tracks:
                write_tag(track, args.write.first, args.val, args.verbose)

                save_changes(track, args.verbose)

        else:
            raise Exception("Tag value needs to be provided.")

    # COPY action
    elif args.copy is not None:
        for track in tracks:
            copy_tag(track, args.copy.first, args.copy.second, args.verbose)
            save_changes(track, args.verbose)
         


if __name__ == '__main__':
	main()
