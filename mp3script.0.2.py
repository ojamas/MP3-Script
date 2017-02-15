# Orin James
# Written for Python 2.7.13 (required for eyed3)

'''

Script for modifying the details of MP3 files, specifically artist, album, number, etc.

 _______________________________________________
| NOTE: the documentation is incomplete thus far|


Sources:
        # initial build: http://opentechschool.github.io/python-scripting-mp3/
        # eyed3: http://eyed3.nicfit.net/
        # os.path: https://docs.python.org/3/library/os.path.html

Change Log:

    11/27/2016: initial investigation of eyed3 module
    12/18/2016: actual implementation and experimentation
    12/22/2016: notes
        # no eyed3 module for python 2.7 installed yet
        # how did one install for 3 if it isn't supported??
    12/24/2016: notes
        # eyed3 working for 2.7.13
        # pip working
        # problems with eyed3 for 2.7, pip, and issues with Python 3 solved by
                # by uninstalling both versions completely and reinstalling only
                # Python 2.7 for simplicity. Potential PATH variable conflicts.
        # script running but information doesn't appear to be updating
    1/2/2017: issues
        # information still not updating on songs
        # for simplicity's and diagnosis' sake, attempted to run script on
                # smaller subsets of songs. Originally tested a full album
                # within a folder first
        # problem: the smaller subsets of songs are throwing a windows syntax
                # error which suggests that there is some text formatting issue
        # up to this point, only updating album and artist has been tested
    1/3/2017: add user input handling
        # ID3 information updated successfully but only after manually inputting
                # data first and then running script is new data applied correctly.
                # It does appear that data is updated but not added to "Details"
                # screen of the MP3 file properties
    1/24/2017: answer from StackOverflow
        # http://stackoverflow.com/questions/41495351/eyed3-package-for-python-not-properly-setting-id3-metadata/41792244#41792244
        # Problem seems to be because Windows uses only a certain version of ID3 tags
                # but the generic x.tag.save() only applies non-supported ID3 versions
        #version=(1,None,None) doesn't seem to work perfectly

    1/26/2017: Added functionality for user dialog. Option to read or write
                fields of choice for a single song.
    1/27/2017: Added read folder functionality. Option to read specific fields
                from the MP3s in an entire directory.
    1/27/2017: Added more invalid input handling, write single file, write folder functionality.

'''
import os           # Module for operating system dependent functionality. Allows access to files and folders.
import eyed3        # Module for accessing and editing MP3 metadata (ID3).
import eyed3.mp3    # Doesn't work without this, but not sure why.

"""
readID3

    Function to read ID3 fields from a single MP3 file.

    Parameters:
        path ->
        
"""
def readID3(path,fields):
    if eyed3.mp3.isMp3File(path):
        # Load MP3 file
        audiofile = eyed3.load(path)
        print " _________________________"
        if "title" in fields or "all" in fields:
            print "| Title:  ", audiofile.tag.title
        if "artist" in fields or "all" in fields:
            print "| Artist: ", audiofile.tag.artist
        if "album" in fields or "all" in fields:
            print "| Album:  ", audiofile.tag.album
        print "|_________________________"
    else:
        print "File is not MP3."

"""
readDir

    Function to read ID3 fields for an entire directory.

    Parameters:
        path ->
        
"""
def readDir(dir_path,fields):
    song_count = 1
    if os.path.isdir(dir_path):
        for file in os.listdir(dir_path):   # loops through each file in directory
            if eyed3.mp3.isMp3File(file):
                audiofile = eyed3.load(dir_path+"\\"+file)
                if "title" in fields or "all" in fields:
                    print "%d. Title:  " % song_count, audiofile.tag.title
                if "artist" in fields or "all" in fields:
                    print "   Artist: ", audiofile.tag.artist
                if "album" in fields or "all" in fields:
                    print "   Album:  ", audiofile.tag.album
                print ""
                song_count += 1
    else:
        print "This is not a directory. Please use a directory path."


"""
writeID3

    Function to write chosen ID3 fields for a single MP3 file.

    Parameters:
        path -> Required. Location of file to be updated.
        title -> Optional
        artist -> Optional
        album -> Optional
"""
def writeID3(path,title=None,artist=None,album=None):
    if eyed3.mp3.isMp3File(path):
        audiofile = eyed3.load(path)	# load file from file path

        print "~~~~~~~~~~ is mp3 file ~~~~~~~~~~~~~"
        print "TITLE:  ", audiofile.tag.title
        print "ARTIST: ", audiofile.tag.artist
        print "ALBUM:  ", audiofile.tag.album

        if title is not None:
            audiofile.tag.title = unicode(title)    # eyed3 expects unicode
        if artist is not None:
            audiofile.tag.artist = unicode(artist)
        if album is not None:
            audiofile.tag.album = unicode(album)

        # Save tags
        #audiofile.tag.save(version=(1,None,None))
        audiofile.tag.save(version=(2,3,0))     # updates ID3v2.3 tags for Windows Explorer
        audiofile.tag.save()                    # updates ID3v2.4 tags for other programs
                
        print "========== Track Updated =============="
        print "TITLE:  ", audiofile.tag.title
        print "ARTIST: ", audiofile.tag.artist
        print "ALBUM:  ", audiofile.tag.album
    else:
        print "File is not MP3."
"""
writeDir

    Function to write chosen ID3 fields for an entire directory.

    
"""
def writeDir(dir_path,title=None,artist=None,album=None):
    song_count = 1
    # Check first that path is for a directory
    if os.path.isdir(dir_path):
        for file in os.listdir(dir_path):   # loops through each file in directory
            # First check if file is MP3
            # "file" = only name of file without path
            if eyed3.mp3.isMp3File(file):
                audiofile = eyed3.load(dir_path+"\\"+file)    # Load file from file path
                print "\n%d. =============== Original ===============" % song_count
                print "  | TITLE:  ", audiofile.tag.title
                print "  | ARTIST: ", audiofile.tag.artist
                print "  | ALBUM:  ", audiofile.tag.album

                if title is not None:
                    audiofile.tag.title = unicode(title)    # eyed3 expects unicode
                if artist is not None:
                    audiofile.tag.artist = unicode(artist)
                if album is not None:
                    audiofile.tag.album = unicode(album)

                # Save tags
                audiofile.tag.save(version=(2,3,0))     # updates ID3v2.3 tags for Windows Explorer
                audiofile.tag.save()                    # updates ID3v2.4 tags for other programs
                        
                print "   =============== Updated ================"
                print "  | TITLE:  ", audiofile.tag.title
                print "  | ARTIST: ", audiofile.tag.artist
                print "  | ALBUM:  ", audiofile.tag.album

                song_count += 1
    else:
        print "This is not a directory. Please use a directory path."

def writeEachDir(dir_path, fields):
    song_count = 1
    if os.path.isdir(dir_path):
        for file in os.listdir(dir_path):
            if eyed3.mp3.isMp3File(file):
                print "Filename:  ",file
                audiofile = eyed3.load(dir_path+"\\"+file)

                print "\n%d. =============== Original ===============" % song_count
                print "  | TITLE:  ", audiofile.tag.title
                print "  | ARTIST: ", audiofile.tag.artist
                print "  | ALBUM:  ", audiofile.tag.album
                
                if "all" in fields:
                    title = raw_input("Enter title: ")
                    artist = raw_input("Enter artist: ")
                    album = raw_input("Enter album: ")

                    if (title != "skip"):
                        audiofile.tag.title = unicode(title)
                    if (artist != "skip"):
                        audiofile.tag.artist = unicode(artist)
                    if (album != "skip"):
                        audiofile.tag.album = unicode(album)
                if "title" in fields:
                    title = raw_input("Enter title: ")
                    if (title != "skip"):
                        audiofile.tag.title = unicode(title)
                if "artist" in fields:
                    artist = raw_input("Enter artist: ")
                    if (artist != "skip"):
                        audiofile.tag.artist = unicode(artist)
                if "album" in fields:
                    album = raw_input("Enter album: ")
                    if (album != "skip"):
                        audiofile.tag.album = unicode(album)

                # Save tags
                audiofile.tag.save(version=(2,3,0))     # updates ID3v2.3 tags for Windows Explorer
                audiofile.tag.save()                    # updates ID3v2.4 tags for other programs
                        
                print "   =============== Updated ================"
                print "  | TITLE:  ", audiofile.tag.title
                print "  | ARTIST: ", audiofile.tag.artist
                print "  | ALBUM:  ", audiofile.tag.album
                song_count += 1
    else:
        print "This is not a directory. Please use a directory path."

def main():
    
    yesChoice = ['yes','y']
    noChoice = ['no','n']
    readChoice = ['read','r']
    writeChoice = ['write','w']
    writeEachChoice = ['write each','writeeach','each','e']


    print "\n     Welcome to the MP3 field update tool!"
    print "\nThis tool is used to update a variety of the metadata fields of an MP3 file."
    print "These fields are known as ID3 tags. Currently, the tags you can read or write are:"
    print "  - Title\n  - Artist\n  - Album"
    print "Folow the prompts to read or write the fields for a single file or all of the files"
    print "within a folder."
    print "\nPress 'q' during any input prompt to quit the program (except while entereing data)."


    # Asks user for file or directory path to use
    valid_path = False
    while valid_path ==False:
        # Ask user for a file or folder path
        path_input = raw_input("Enter a file or folder path: ")
        if os.path.isdir(path_input):
            dir_path = path_input
            valid_path = True
        elif eyed3.mp3.isMp3File(path_input):
            file_path = path_input
            valid_path = True
        # Added option to skip path input for testing
        elif path_input == "skip":
            valid_path = True
        elif path_input == "q":
            quit()
        else:
            print "\nInvalid path. Enter either path to MP3 file or folder containing MP3 files."




    file_path = "C:\Users\Orin\Documents\Python\eyed3\Mura Masa - Miss You.mp3"
    dir_path = "C:\Users\Orin\Documents\Python\eyed3\Young Thug - Slime Season 2"
    #dir_path = "C:\Users\Orin\Documents\Python\eyed3\songs"



    valid_action = False
    while valid_action == False:
        # Ask user if they want to read or write information
        action_input = raw_input("\nDo you want to read or write ID3 data? (r/w/e)\nThe other option is writing fields individually for each file in folder (r).\n - Read (r). \n - Write (w). \n - Write individually in folder (e).\n").lower()


        # Read data
        if action_input in readChoice:    
            valid_amount = False
            while valid_amount == False:
                # Ask user if they want to read a single file or entire folder
                amount_input = raw_input("\nRead a single file or entire folder? \n -File\n -Folder\n").lower()
                if amount_input == "file":
                    valid_field = False
                    while valid_field == False:
                        # Collect fields that user would like to read
                        read_fields = raw_input("\nWhich fields would you like to check? Enter choices separated by a comma or choose all.\n -All \n -Title \n -Artist \n -Album \n").lower()                  
                        if ("all" in read_fields) or ("title" in read_fields) or ("artist" in read_fields) or ("album" in read_fields):
                            # Call read function which determines what is printed
                            readID3(file_path,read_fields)
                            valid_field = True
                        elif read_fields == "q":
                            quit()
                        else:
                            print ""
                            print "Invalid field entry."
                    valid_amount = True
                elif amount_input == "folder":
                    valid_field = False
                    while valid_field == False:
                        # Collect fields that user would like to read
                        read_fields = raw_input("\nWhich fields would you like to check? Enter choices separated by a comma or choose all.\n -All \n -Title \n -Artist \n -Album \n").lower()                  
                        if ("all" in read_fields) or ("title" in read_fields) or ("artist" in read_fields) or ("album" in read_fields):
                            # Call read directory function which determines what is printed
                            readDir(dir_path,read_fields)
                            valid_field = True
                        elif read_fields == "q":
                            quit()
                        else:
                            print ""
                            print "Invalid field entry."
                    valid_amount = True
                elif amount_input == "q":
                    quit()
                else:
                    print ""
                    print "Invalid option. Choose file or folder."
            # Below code handles choice to exit the program or performing another action.
            valid_yn_input = False
            while valid_yn_input == False:
                done_input = raw_input("Finished with program? \n - Yes (y). \n - No (n).\n").lower()
                if done_input in yesChoice:
                    valid_yn_input = True
                    quit()
                elif done_input in noChoice:
                    valid_yn_input = True
                else:
                    print ""
                    print "Invalid yes/no entry."
            #valid_action = True

        # Write data
        elif action_input in writeChoice:
            title_input = None
            artist_input = None
            album_input = None

            valid_write_amount = False
            while valid_write_amount == False:
                # Ask user if they want to write a single file or entire folder
                write_amount_input = raw_input("\nWrite a single file or entire folder? \n -File\n -Folder\n").lower()
                if write_amount_input == "file":
                    valid_field = False
                    while valid_field == False:
                        # Ask what fields user wants to input
                        print "Enter blank input to set field to None (Nonetype)."
                        write_fields = raw_input("\nWhich fields would you like to update? Enter choices separated by a comma or choose all.\n -All \n -Title \n -Artist \n -Album \n").lower()
                        if ("all" in write_fields) or ("title" in write_fields) or ("artist" in write_fields) or ("album" in write_fields):
                            if "all" in write_fields:
                                title_input = raw_input("Enter title: ")
                                artist_input = raw_input("Enter artist: ")
                                album_input = raw_input("Enter album: ")
                            if "title" in write_fields:
                                title_input = raw_input("Enter title: ")
                            if "artist" in write_fields:
                                artist_input = raw_input("Enter artist: ")
                            if "album" in write_fields:
                                album_input = raw_input("Enter album: ")
                            # Call writeID3 passing updated fields
                            writeID3(file_path, title = title_input, artist = artist_input ,album = album_input)
                            valid_field = True
                        elif write_fields == "q":
                            quit()
                        else:
                            print "\nInvalid field entry."
                        valid_write_amount = True
                elif write_amount_input == "folder":
                    valid_field = False
                    while valid_field == False:
                        # Ask what fields user wants to input
                        print "\nWARNING: Changes to the following fields will be applied to all MP3 files in folder."
                        print "Enter blank input to set field to None (Nonetype)."
                        write_fields = raw_input("Which fields would you like to update? Enter choices separated by a comma or choose all.\n -All \n -Title \n -Artist \n -Album \n").lower()
                        if ("all" in write_fields) or ("title" in write_fields) or ("artist" in write_fields) or ("album" in write_fields):
                            if "all" in write_fields:
                                title_input = raw_input("Enter title: ")
                                artist_input = raw_input("Enter artist: ")
                                album_input = raw_input("Enter album: ")
                            if "title" in write_fields:
                                title_input = raw_input("Enter title: ")
                            if "artist" in write_fields:
                                artist_input = raw_input("Enter artist: ")
                            if "album" in write_fields:
                                album_input = raw_input("Enter album: ")
                            # Call writeDir passing updated fields
                            writeDir(dir_path, title = title_input, artist = artist_input ,album = album_input)
                            valid_field = True
                        elif write_fields == "q":
                            quit()
                        else:
                            print "\nInvalid field entry."
                        valid_write_amount = True
                elif write_amount_input == "q":
                    quit()
                else:
                    print ""
                    print "Invalid option. Choose file or folder."

            # Below code handles choice to exit the program or performing another action.
            valid_yn_input = False
            while valid_yn_input == False:
                done_input = raw_input("Finished with program? \n - Yes (y). \n - No (n).\n").lower()
                if done_input in yesChoice:
                    valid_yn_input = True
                    quit()
                elif done_input in noChoice:
                    valid_yn_input = True
                else:
                    print ""
                    print "Invalid yes/no entry."
            #valid_action = True


        # Write specific data for each file in folder
        elif action_input in writeEachChoice:
            valid_field = False
            while valid_field == False:
                # Collect fields that user would like to read
                write_each_fields = raw_input("\nWhich fields would you like to update for each file? Enter choices separated by a comma or choose all.\n -All \n -Title \n -Artist \n -Album \n").lower()                  
                if ("all" in write_each_fields) or ("title" in write_each_fields) or ("artist" in write_each_fields) or ("album" in write_each_fields):
                    # Call writeEachDir function which prompts user for input on each file
                    writeEachDir(dir_path, write_each_fields)
                    valid_field = True
                elif write_each_fields == "q":
                    quit()
                else:
                    print ""
                    print "Invalid field entry."
            # Below code handles choice to exit the program or performing another action.
            valid_yn_input = False
            while valid_yn_input == False:
                done_input = raw_input("Finished with program? \n - Yes (y). \n - No (n).\n").lower()
                if done_input in yesChoice:
                    valid_yn_input = True
                    quit()
                elif done_input in noChoice:
                    valid_yn_input = True
                else:
                    print ""
                    print "Invalid yes/no entry."
            #valid_action = True
        elif action_input == "q":
            quit()
        else:
            print ""
            print "Invalid option. Choose read or write."
    

# Standard for Python main function call
# If being executed directly (such as a script in this case) module __name__ is
    # set to __main__
if __name__ == "__main__":
    main()  # execute main function
