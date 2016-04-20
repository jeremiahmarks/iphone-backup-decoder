# Major Update #

## A GUI version is available ##

I have written a Mac OS X GUI version of this tool.  It is available for download at [my website](http://supercrazyawesome.com/).  The GUI app supersedes this script, and I will not be continuing to maintain this version.  Please download the new app, and let me know what you think.


---


iTunes stores a backup of some of the iPhone files on your computer.  This script will extract these files so that you can view and edit them.

The script does not currently support re-encoding.

Make a copy of your `~/Library/Application Support/MobileSync/Backup/` and run the script against the `*.mdbackup` files.  The script will create a `MobileSyncExport` folder which will contain the extracted files.

Currently supports Mac OS X. Tested on Python 2.3.5 and upwards.  Tested with iPhone OS 2.1 / iTunes 8.0 backups.

The output is a folder full of plist and SQLite databases.  If that doesn't mean anything to you or you don't know how to use Terminal to run a python script, this script will not be of use to you.

Thanks to Eric A Merrill for suggesting a fix for 1.1.4 and to joachimb for suggesting a patch.
