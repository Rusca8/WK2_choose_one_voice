# import the main window object (mw) from aqt
from aqt import mw
# import all of the Qt GUI library
from aqt.qt import *
# import the "show info" tool from utils.py
from aqt.utils import showInfo, showWarning


def ask_which():
    """message box: choose male or female
    """
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Question)
    msg.setText("Which voice you want to keep?")
    msg.setWindowTitle("Choose Voice")
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    butOk = msg.button(QMessageBox.Ok)
    butOk.setText('Female')
    butC = msg.button(QMessageBox.Cancel)
    butC.setText('Male')
    msg.buttonClicked.connect(which_btn)

    msg.exec_()  # show message box


def which_btn(i):
    """Analysis of the current deck's audios

    Catches the button pressed on ask_which, counts audios, pairs and unprocessed pairs
    Shows message box asking for confirmation before deleting stuff.
    """
    deckname = mw.col.decks.current()["name"]  # get current deck name
    ids = mw.col.findNotes("deck:current")  # get id for all notes on the current deck

    # counting audios
    counts = [0, 0, 0, 0, 0, 0, 0, 0, 0]  # 1 to 8, and then the last one is "9 or more"
    cdouble = 0  # audios in pairs (2, 4, 6, 8)
    cdnew = 0  # audios in pairs never processed (when I process, I add "·" to avoid processing again 2s coming from 4s)
    for note_id in ids:
        note = mw.col.getNote(note_id)  # get note from the given id
        if "Audio" in note:
            if "[" in note["Audio"]:
                audios = note["Audio"].count("]")  # how many audios are there?
                counts[min(audios-1, 8)] += 1
                if not audios % 2:  # allegedly pairs of Female-Male
                    cdouble += 1
                    if "·" not in note["Audio"]:  # not-processed-before pairs
                        cdnew += 1

    # message box: analysis and confirmation
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    text = "<b>Deck: '%s'</b><br><br>Content:<br>" % deckname
    for n, x in enumerate(counts):
        if n == 8:
            text += "· %s notes with %s+ audios<br>" % (x, (n + 1))
        elif n == 0:
            text += "· %s notes with %s audio<br>" % (x, (n + 1))
        else:
            text += "· %s notes with %s audios<br>" % (x, (n+1))
    text += ("<br>Analysis:<br>· %s notes with audio pairs<br>· %s of those %s were never processed<br><br>"
             % (cdouble, cdnew, cdouble))
    if i.text() == "Female":  # keep female
        text += ("We will delete the <b>male</b> sounds from %s notes.<br><br>"
                 "<i>This assumes the Female sound is the first one you hear.</i>" % cdnew)
    elif i.text() == "Male":  # keep male
        text += ("We will delete the <b>Female</b> sounds from %s notes.<br><br>"
                 "<i>This assumes the Male sound is the second one you hear.</i>" % cdnew)
    msg.setText("The deletion will be permanent.")
    msg.setInformativeText(text)
    msg.setWindowTitle("CONFIRM PERMANENT ERASING")
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    butOk = msg.button(QMessageBox.Ok)
    butOk.setText("Erase")
    butC = msg.button(QMessageBox.Cancel)
    msg.setDefaultButton(butC)
    butC.setText("Cancel")

    # connect the msgbox either with keep_female or keep_male
    if i.text() == "Female":
        msg.buttonClicked.connect(keep_female)
    elif i.text() == "Male":
        msg.buttonClicked.connect(keep_male)
    else:
        showInfo("Something weird happened (Err: which_btn)")

    if any(x for x in counts):  # check if the deck is the proper one (audios in 'Audio' field)
        msg.exec_()  # show message box
    else:
        showWarning("I don't think you can do this here,<br>my friend...<br><br>Expected audios in 'Audio' field.<br>"
                    "Try it again on a WaniKani 2 deck.")


def keep_male(i):
    """Catches the pressed button and runs the deletion if needed"""
    if i.text() == "Erase":
        erase("Female")
    elif i.text() == "Cancel":
        showInfo("Deletion aborted.")
    else:
        showInfo("Something weird happened (Err:keep_male)")


def keep_female(i):
    """Catches the pressed button and runs the deletion if needed"""
    if i.text() == "Erase":
        erase("Male")
    elif i.text() == "Cancel":
        showInfo("Deletion aborted.")
    else:
        showInfo("Something weird happened (Err:keep_female)")


def erase(delete="Male"):
    """Goes through all notes in the deck and keeps only the selected audios.

    :param delete: which to delete (Male or Female)
    """
    # get id for all notes on the current deck
    ids = mw.col.findNotes("deck:current")
    # go through all of them
    for note_id in ids:
        note = mw.col.getNote(note_id)  # get note from the given id
        if "Audio" in note:
            if "[" in note["Audio"] and "·" not in note["Audio"]:  # already processed pairs will have a "·"
                count = note["Audio"].count("]")  # how many audios are there? (audios are like [somthing.mp3])
                if not count % 2:  # even number of audios (do nothing to odd quantities)
                    audios = note["Audio"].split("]")  # splits into a list of single audios
                    for x in range(len(audios)):  # get the "]" back (the split eats them hahah)
                        if audios[x]:
                            audios[x] += "]"
                    a_female = "·".join(audios[x] for x in range(len(audios)) if not x % 2)  # join even (female) audios
                    a_male = "·".join(audios[x] for x in range(len(audios)) if x % 2)  # join odd (male) audios
                    if a_female.endswith("·"):  # delete the last "·", which I don't need nor want
                        a_female = a_female[:-1]
                    if a_male.endswith("·"):    # otherwise join makes it like [sound]·[sound]· (or worse: [sound]·)
                        a_male = a_female[:-1]
                    # keep the chosen one
                    if delete == "Male":
                        note["Audio"] = a_female
                    elif delete == "Female":
                        note["Audio"] = a_male
                    note.flush()  # save changes
    showInfo("Deletion completed.")

# create a new menu item
action = QAction('Choose one voice (WK2)', mw)
# set it to call testFunction when it's clicked
action.triggered.connect(ask_which)
# and add it to the tools menu
mw.form.menuTools.addAction(action)
