# WK2 Choose One Voice
> Anki add-on to erase one of the two audio speakers coming with the 'WaniKani Ultimate 2: Electric Boogaloo' deck.

## How does it work?
Each note with audio in WK2 has two audios* (first Female, then Male) in a field named 'Audio'.
The script finds each of those notes and keeps only the first or the second of the audios, depending on what speaker you choose.

When executed, any card with only one audio in the 'Audio' field is left as it is.

_* Actually, a really small part of the notes come with only one of the audios._

## How to use it
### Adding the script to anki
1. Find the add-ons folder (```addons21```) in your computer (you can access it from anki at ```tools/add-ons/open addons folder```).
2. Download this repository (you just need the ```choose_one_voice``` folder).
3. Put the ```choose_one_voice``` folder inside the add-ons folder (and restart anki if it was open).

### Executing the script
4. Select the "WaniKani Ultimate 2: Electric Boogaloo" deck in Anki (so that it's the current deck).
5. Go to ```tools/choose one voice (WK2)``` in the Anki menu.
6. Choose which voice you want to keep (male or female).  
_It'll ask for confirmation before erasing stuff._
7. Once audio references are deleted from the field, you can check for unused media to actually delete the ```.mp3``` files.

### Deleting the unused .mp3 files
8. Go to ```tools/check media``` on the Anki menu.
9. Press ```delete unused``` at the bottom.
10. You can also delete them from the ```media trash``` folder too, if you want.

### Deleting them from the recycling bin too
11. Find the user folder (outside of the add-ons folder there's your folder, probably named ```User 1```).
12. Go inside and find the ```media.trash``` folder.
13. Delete stuff from there (this is all the media files Anki has used in the past but were deleted when choosing ```delete unused```).
