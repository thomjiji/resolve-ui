import glob
import os
from turtle import numinput
from pybmd import Bmd
from pybmd import toolkits

resolve = Bmd()
project = resolve.get_project_manager().get_current_project()
media_pool = project.get_media_pool()
root_folder = media_pool.get_root_folder()

ui = fusion.UIManager
dispatcher = bmd.UIDispatcher(ui)

createBinID = "Create bin"
inputID = "Input field"
testClickID = "Test click"
pathTreeID = "Path tree"
showPathID = "Show path"

# Define the window UI layout
win = dispatcher.AddWindow(
    {
        "ID": "myWindow",
        "WindowTitle": "sample",
    },
    ui.VGroup(
        {
            "Spacing": 5,
            "Weight": 0,
        },
        [
            ui.HGroup(
                {
                    "Spacing": 5,
                    "Weight": 0,
                },
                [
                    ui.LineEdit(
                        {
                            "ID": inputID,
                            "PlaceholderText": "Text Field",
                        }
                    ),
                ],
            ),
            ui.HGroup(
                {
                    "Spacing": 5,
                    "Weight": 0,
                },
                [
                    ui.Button(
                        {
                            "ID": createBinID,
                            "Text": "Create bin",
                            "Weight": 0,
                        },
                    ),
                    ui.Button(
                        {
                            "ID": testClickID,
                            "Text": "Test Click",
                            "Weight": 0,
                        }
                    ),
                    ui.Button(
                        {
                            "ID": showPathID,
                            "Text": "Show Path",
                            "Weight": 0,
                        },
                    ),
                ],
            ),
            ui.LineEdit(
                {
                    "PlaceholderText": "example text",
                }
            ),
            ui.SpinBox(
                {
                    "Value": 2,
                    "Minimum": 1,
                    "Maximum": 99,
                    "SingleStep": 1,
                    "Weight": 0,
                }
            ),
            ui.Tree(
                {
                    "ID": pathTreeID,
                    "AlternatingRowColors": True,
                    "HeaderHidden": True,
                    "SelectionMode": "ExtendedSelection",
                    "Weight": 2,
                }
            ),
        ],
    ),
)

itm = win.GetItems()


# Define the events handlers
def on_close(ev):
    dispatcher.ExitLoop()


def on_create_bin(ev):
    path = itm[inputID].Text
    toolkits.add_subfolders(media_pool, root_folder, path)


def test_click(ev):
    print(f"{itm[inputID].Text}")


def show_tree(ev):
    top_level_items = []
    row = itm[pathTreeID].NewItem()
    row.Text[0] = itm[inputID].Text
    top_level_items.append(row)
    itm[pathTreeID].AddTopLevelItems(top_level_items)


# Assign events handlers
win.On.myWindow.Close = on_close
win.On[createBinID].Clicked = on_create_bin
win.On[testClickID].Clicked = test_click
win.On[showPathID].Clicked = show_tree


if __name__ == "__main__":
    win.Show()
    dispatcher.RunLoop()
