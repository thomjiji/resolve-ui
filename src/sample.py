from cmath import pi
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
testID = "Test click"
pathTreeID = "Path tree"
addPathID = "Add path"
clearPathID = "Clear all path"
clearSelectedPathID = "Clear selected path"
comboBoxID = "Combo Box"

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
            ui.Label(
                {
                    "Text": "Test Window - thomjiji",
                    "Weight": 0,
                    "Alignment": {
                        "AlignHCenter": True,
                        "AlignVCenter": True,
                    },
                },
            ),
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
                            "MaxLength": 10,
                        }
                    ),
                    ui.HGap(3),
                    ui.SpinBox(
                        {
                            "Value": 0,
                            "Minimum": 0,
                            "Maximum": 99,
                            "SingleStep": 1,
                            "Prefix": "The ",
                            "Suffix": " Items",
                            "Weight": 0.5,
                        }
                    ),
                    ui.Slider(
                        {
                            "Value": 0,
                            "Minimum": 0,
                            "Maximum": 100,
                            "SliderPosition": "Center",
                        }
                    ),
                    ui.ComboBox(
                        {
                            "ID": comboBoxID,
                            "Editable": False,
                            "Enable": True,
                            # "CurrentText": "Info down below",
                        }
                    ),
                    ui.CheckBox(
                        {
                            "Text": "Check Or Not",
                            "Checkable": True,
                            "Checked": False,
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
                            "ID": testID,
                            "Text": "Test",
                            "Weight": 0,
                        }
                    ),
                    ui.Button(
                        {
                            "ID": createBinID,
                            "Text": "Create bin",
                            "Weight": 0,
                        },
                    ),
                    ui.Button(
                        {
                            "ID": addPathID,
                            "Text": "Add Path",
                            "Weight": 0,
                        },
                    ),
                    ui.Button(
                        {
                            "ID": clearSelectedPathID,
                            "Text": "Remove Selected Path",
                            "Weight": 0,
                        },
                    ),
                    ui.Button(
                        {
                            "ID": clearPathID,
                            "Text": "Clear All Path",
                            "Weight": 0,
                        },
                    ),
                ],
            ),
            ui.Tree(
                {
                    "ID": pathTreeID,
                    "AlternatingRowColors": True,
                    "HeaderHidden": True,
                    "SelectionMode": "ExtendedSelection",
                    "Weight": 1,
                    "AutoScroll": True,
                }
            ),
        ],
    ),
)

itm = win.GetItems()
itm[comboBoxID].AddItems(["From Premiere", "From Baselight"])

# Define the events handlers
def on_close(ev):
    dispatcher.ExitLoop()


def on_create_bin(ev):
    path = itm[inputID].Text
    toolkits.add_subfolders(media_pool, root_folder, path)


def on_test_click(ev):
    # current_tree_item = itm[pathTreeID].CurrentItem()
    # print(f"current TreeItem object is {current_tree_item}.")
    print(f"{itm[inputID].Text}")


def on_add_tree(ev):
    top_level_items = []
    row = itm[pathTreeID].NewItem()
    row.Text[0] = itm[inputID].Text
    top_level_items.append(row)
    itm[pathTreeID].AddTopLevelItems(top_level_items)


def on_clear_all_path(ev):
    itm[pathTreeID].Clear()


def on_click_tree_item(ev):
    current_item = itm[pathTreeID].CurrentItem()
    print(current_item)


def on_remove_select_tree_item(ev):
    current_selection = itm[pathTreeID].CurrentItem()
    itm[pathTreeID].RemoveChild(current_selection)


# Assign events handlers
win.On.myWindow.Close = on_close
win.On[createBinID].Clicked = on_create_bin
win.On[testID].Clicked = on_test_click
win.On[addPathID].Clicked = on_add_tree
win.On[clearPathID].Clicked = on_clear_all_path
win.On[pathTreeID].ItemClicked = on_click_tree_item
win.On[clearSelectedPathID].Clicked = on_remove_select_tree_item


if __name__ == "__main__":
    win.Show()
    dispatcher.RunLoop()
