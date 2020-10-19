# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo, showWarning
# import all of the Qt GUI library
from aqt.qt import *


def ask_which():
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
    deckname = mw.col.decks.current()["name"]  # get current deck name

    ids = mw.col.findNotes("deck:current")  # get id for all notes on the current deck
    # counting audios
    count = 0
    cdouble = 0
    for note_id in ids:
        note = mw.col.getNote(note_id)  # get note from the given id
        if "Audio" in note:
            if "[" in note["Audio"]:
                count += 1
                if "][" in note["Audio"]:
                    cdouble += 1

    # message box choose male vs female
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    text = ("<b>Deck: '%s'</b><br>"
            "· %s notes with audio<br>"
            "· %s notes with both audios<br><br>" % (deckname, count, cdouble))
    if i.text() == "Female":  # keep female
        text += ("We will delete the <b>male</b> sounds from %s notes.<br><br>"
                 "<i>This assumes the Female sound is the first one you hear.</i>" % cdouble)
    elif i.text() == "Male":  # keep male
        text += ("We will delete the <b>Female</b> sounds from %s notes.<br><br>"
                 "<i>This assumes the Male sound is the second one you hear.</i>" % cdouble)
    msg.setText("The deletion will be permanent.")
    msg.setInformativeText(text)
    msg.setWindowTitle("CONFIRM PERMANENT ERASING")
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    butOk = msg.button(QMessageBox.Ok)
    butOk.setText("Erase")
    butC = msg.button(QMessageBox.Cancel)
    msg.setDefaultButton(butC)
    butC.setText("Cancel")

    if i.text() == "Female":
        msg.buttonClicked.connect(keep_female)
    elif i.text() == "Male":
        msg.buttonClicked.connect(keep_male)
    else:
        showInfo("Something weird happened (Err: which_btn)")

    if count:
        msg.exec_()  # show message box
    else:
        showWarning("I don't think you can do this here,<br>my friend...<br><br>Expected audios in 'Audio' field.<br>"
                    "Try it again on a WaniKani 2 deck.")


def keep_male(i):
    if i.text() == "Erase":
        erase("Female")
    elif i.text() == "Cancel":
        showInfo("Deletion aborted.")
    else:
        showInfo("Something weird happened (Err:keep_male)")


def keep_female(i):
    if i.text() == "Erase":
        erase("Male")
    elif i.text() == "Cancel":
        showInfo("Deletion aborted.")
    else:
        showInfo("Something weird happened (Err:keep_female)")


def erase(delete="Male"):
    # get id for all notes on the current deck
    ids = mw.col.findNotes("deck:current")
    # processing all of them
    a_female = "none"
    a_male = "none"
    for note_id in ids:
        note = mw.col.getNote(note_id)  # get note from the given id
        if "Audio" in note:
            if "][" in note["Audio"]:
                a_female, a_male = note["Audio"].split("]")[:2]
                a_female += "]"
                a_male += "]"
                # keep the chosen one
                if delete == "Male":
                    note["Audio"] = a_female
                elif delete == "Female":
                    note["Audio"] = a_male
                note.flush()
    showInfo("Deletion completed.")
    # showInfo("Last note<br>%s<br>%s" % (a_female, a_male))

# create a new menu item
action = QAction('Choose one voice (WK2)', mw)
# set it to call testFunction when it's clicked
action.triggered.connect(ask_which)
# and add it to the tools menu
mw.form.menuTools.addAction(action)