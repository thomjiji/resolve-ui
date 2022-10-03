import os
from pprint import pprint
from pybmd import Bmd
from pybmd import toolkits

INVALID_EXTENSION = ["DS_Store", "JPG", "JPEG", "SRT"]

resolve = Bmd()
project = resolve.get_project_manager().get_current_project()
media_pool = project.get_media_pool()
root_folder = media_pool.get_root_folder()
media_storage = resolve.get_media_stroage()

ui = fusion.UIManager
fu = bmd.scriptapp("Fusion")
dispatcher = bmd.UIDispatcher(ui)

createBinID = "Create bin"
inputPathID = "Input path"
testID = "Test click"
pathTreeID = "Path tree"
addPathID = "Add path"
clearPathID = "Clear all path"
clearSelectedPathID = "Clear selected path"
comboBoxID = "Combo Box"
pathParseID = "Parse input path"
browseFileManagerID = "Browse"

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
                    ui.Label(
                        {
                            "Text": "Location",
                            "Weight": 0,
                        }
                    ),
                    ui.LineEdit(
                        {
                            "ID": inputPathID,
                            "ClearButtonEnabled": True,
                            # "MaxLength": 10,
                        }
                    ),
                    ui.Button(
                        {
                            "ID": browseFileManagerID,
                            "Text": "Browse",
                            "Weight": 0,
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
                            "ID": clearPathID,
                            "Text": "Clear All Path",
                            "Weight": 0,
                        },
                    ),
                    ui.Button(
                        {
                            "ID": pathParseID,
                            "Text": "Parse Path",
                            "Weight": 0,
                        }
                    ),
                ],
            ),
            ui.Tree(
                {
                    "ID": pathTreeID,
                    "AlternatingRowColors": True,
                    "HeaderHidden": False,
                    "SelectionMode": "ExtendedSelection",
                    "Weight": 1,
                    "AutoScroll": True,
                    "SortingEnabled": True,
                }
            ),
            ui.HGroup(
                {
                    "Weight": 0,
                },
                [
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
        ],
    ),
)
itm = win.GetItems()

itm[comboBoxID].AddItems(["From Premiere", "From Baselight"])
itm[pathTreeID].SetHeaderLabel("Camera Name")


# General functions
def absolute_file_paths(path: str) -> list:
    """
    Get the abs of all files from the input path, exclude files from INVALID_EXTENSION.
    """
    absolute_file_path_list = []
    for directory_path, _, filenames in os.walk(path):
        for filename in filenames:
            # Exclude invalid extension when getting abs for all files under the input media path (素材)
            if filename.split(".")[1] not in INVALID_EXTENSION:
                pprint(filename)
                absolute_file_path_list.append(
                    os.path.abspath(os.path.join(directory_path, filename))
                )

    return absolute_file_path_list


def get_sorted_path(path: str) -> list:
    """
    Get the abs of all files from the input path, then sort the abs,
    and finally return a list of sorted abs.
    """
    filename_and_fullpath_dict = {
        os.path.basename(os.path.splitext(path)[0]): path
        for path in absolute_file_paths(path)
    }
    filenames = list(filename_and_fullpath_dict.keys())
    filenames.sort()
    fullpaths = [
        filename_and_fullpath_dict.get(i) for i in filenames
    ]
    return fullpaths


# Events handlers
def on_close(ev):
    dispatcher.ExitLoop()


def on_create_bin(ev):
    path = itm[inputPathID].Text
    toolkits.add_subfolders(media_pool, root_folder, path)


def on_test_click(ev):
    print(f"{itm[inputPathID].Text}")


def on_add_tree(ev):
    top_level_items = []
    row = itm[pathTreeID].NewItem()
    row.Text[0] = itm[inputPathID].Text
    top_level_items.append(row)
    itm[pathTreeID].AddTopLevelItems(top_level_items)


def on_clear_all_path(ev):
    itm[pathTreeID].Clear()


def on_parse_input_path(ev):
    """Extract the sub paths under the input path and add them to the tree."""
    input_path = itm[inputPathID].Text
    all_files_abs = get_sorted_path(input_path)
    pprint(all_files_abs)

    top_level_items = []
    for i in all_files_abs:
        row = itm[pathTreeID].NewItem()
        row.Text[0] = i
        top_level_items.append(row)
    itm[pathTreeID].AddTopLevelItems(top_level_items)


def on_click_browse_button(ev):
    selected = fu.RequestDir()
    itm[inputPathID].Text = str(selected)
    return selected


def on_click_tree_item(ev):
    # about to change
    current_item = itm[pathTreeID].TreePosition
    print(current_item)


# Assign events handlers
win.On.myWindow.Close = on_close
win.On[createBinID].Clicked = on_create_bin
win.On[testID].Clicked = on_test_click
win.On[addPathID].Clicked = on_add_tree
win.On[clearPathID].Clicked = on_clear_all_path
win.On[pathTreeID].ItemClicked = on_click_tree_item
win.On[pathParseID].Clicked = on_parse_input_path
win.On[browseFileManagerID].Clicked = on_click_browse_button

if __name__ == "__main__":
    win.Show()
    dispatcher.RunLoop()