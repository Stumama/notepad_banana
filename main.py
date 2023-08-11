#start to create smart notes app
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QTextEdit, QPushButton, QLineEdit, QInputDialog
import json

notes = {
    "Welcome!" : {
        "text" : "This is the best note taking app int he world",
        "tags" : ["good", "instructions"]
    }
}

with open("note.json", "w") as file:
    json.dump(notes,file)

app = QApplication([])
main = QWidget()
main.setWindowTitle("Microsoft walmart notepad")
main.resize(600, 500)

notepad = QTextEdit()
notes_list_text = QLabel("List of Notes:")
notes_list = QListWidget()
btn_create = QPushButton("Create note")
btn_delet = QPushButton("Delete note")
hashtag_text = QLabel("List of Hashtags:")
hashtag_list = QListWidget()

search_box = QLineEdit()
search_box.setPlaceholderText("Enter a tag...")

btn_tag = QPushButton("Pin to note")
btn_untag = QPushButton("Unpin Tag")
btn_search = QPushButton("Search")
btn_save = QPushButton("Save")

master_layout = QHBoxLayout()

col1 = QVBoxLayout()
col2 = QVBoxLayout()

row1 = QHBoxLayout()
row2 = QHBoxLayout()
row3 = QHBoxLayout()
row4 = QHBoxLayout()

col1.addWidget(notepad)
col2.addWidget(notes_list_text)
col2.addWidget(notes_list)

row1.addWidget(btn_create)
row1.addWidget(btn_delet)
row2.addWidget(btn_save)
col2.addLayout(row1)
col2.addLayout(row2)

col2.addWidget(hashtag_text)
col2.addWidget(hashtag_list)

col2.addWidget(search_box)

row3.addWidget(btn_tag)
row3.addWidget(btn_untag)

row4.addWidget(btn_search)
col2.addLayout(row3)
col2.addLayout(row4)

master_layout.addLayout(col1, 70)
master_layout.addLayout(col2, 30)

master_layout.addLayout(col1)

main.setLayout(master_layout)

def show_note():
    key = notes_list.selectedItems()[0].text()
    print(key)
    notepad.setText(notes[key]["text"])
    hashtag_list.clear()
    hashtag_list.addItems(notes[key]["tags"])

def create_note():
    note = list()
    note_name, ok = QInputDialog.getText(main, "Add note", "Enter note name")
    if note_name and ok != "":
        notes[note_name] = {"text":"", "tags":[]}
        notes_list.addItems(notes)
        with open("note.json", "w") as file:
            json.dump(notes, file)

def delete_note():
    if notes_list.selectedItems():
        key = notes_list.selectedItems()[0].text()
        del notes[key]
        notes_list.clear()
        hashtag_list.clear()
        notepad.clear()
        notes_list.addItems(notes)
        with open("note.json", "w") as file:
            json.dump(notes, file)
    else:
        print("No note selected")
        
def save_note():
    if notes_list.selectedItems()[0]:
        key = notes_list.selectedItems()[0].text()
        notes[key]["text"] = notepad.toPlainText()
        with open("note.json", "w") as file:
            json.dump(notes, file)
        print(notes)
    else:
        print("Note to save is note selected")

def add_tag():
    if notes_list.selectedItems():
        key = notes_list.selectedItems()[0].text()
        tag = search_box.text()
        if tag not in notes[key]["tags"]:
            notes[key]["tags"].append(tag)
            hashtag_list.addItem(tag)
            notepad.clear()
        with open("note.json", "w") as file:
            json.dump(notes, file)
    else:
        print("No Tag Here!")

def del_tag():
    if notes_list.selectedItems():
        key = notes_list.selectedItems()[0].text()
        try:
            tag = hashtag_list.selectedItems()[0].text()
        except IndexError:
            print("Index Error")

        notes[key]["tags"].remove(tag)
        hashtag_list.clear()            
        hashtag_list.addItems(notes[key]["tags"])

        with open("note.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print("Note to delete a tag is not selected!")

def search_tag():
    tag = search_box.text()
    if btn_search.text() == "Search" and tag:
        filter_note = {}
        for note in notes:
            if tag in notes[note]["tags"]:
                filter_note[note] = notes[note]
        btn_search.setText("Clear result")
        notes_list.clear()
        hashtag_list.clear()
        notes_list.addItems(filter_note)
    elif btn_search.text() == "Clear result" and tag:
        notes_list.clear()
        hashtag_list.clear()
        search_box.clear()
        notes_list.addItems(notes)
        btn_search.setText("Search")
    else:
        pass






notes_list.itemClicked.connect(show_note)
btn_create.clicked.connect(create_note)
btn_delet.clicked.connect(delete_note)
btn_save.clicked.connect(save_note)
btn_tag.clicked.connect(add_tag)
btn_untag.clicked.connect(del_tag)
btn_search.clicked.connect(search_tag)

with open("note.json", "r") as file:
    notes = json.load(file)

notes_list.addItems(notes)
main.show()
app.exec_()