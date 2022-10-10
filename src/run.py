import os
from pprint import pprint
from typing import List, Dict, Union
from resolve_toolkits import main
from pybmd import Bmd
from pybmd import toolkits
from pybmd import timeline as bmd_timeline
from pybmd import folder as bmd_folder

INVALID_EXTENSION = ["DS_Store", "JPG", "JPEG", "SRT"]

resolve = Bmd()
project = resolve.get_project_manager().get_current_project()
media_pool = project.get_media_pool()
root_folder = media_pool.get_root_folder()
media_storage = resolve.get_media_stroage()

fusion = bmd.scriptapp("Fusion")  # type: ignore
ui = fusion.UIManager
dispatcher = bmd.UIDispatcher(ui)  # type: ignore

createBinID = "Create bin"
inputPathID = "Input path"
outputPathID = "Output path"
testID = "Test click"
pathTreeID = "Path tree"
addPathID = "Add path"
clearPathID = "Clear all path"
clearSelectedPathID = "Clear selected path"
comboBoxID = "Combo Box"
pathParseID = "Parse input path"
browseInputFileManagerID = "Browse input"
browseOutputFileManagerID = "Browse output"
clearAllContentID = "Clear all content in the media pool"
proxyRunID = "Proxy run"
addSinglePathID = "Add single path"


# Define the window UI layout
win = dispatcher.AddWindow(
    {
        "ID": "myWindow",
        # The position and size of the window on the screen, this
        # value allows it to appear right in the middle of the screen.
        "Geometry": [
            500,
            300,
            800,
            600,
        ],
        "WindowTitle": "Automator",
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
                    ui.VGroup(
                        {
                            "spacing": 5,
                            "Weight": 0,
                        },
                        [
                            ui.VGap(0.5),
                            ui.Label(
                                {
                                    "Text": "Input Path",
                                    "Weight": 0,
                                    "Alignment": {
                                        "AlignRight": True,
                                        "AlignVCenter": True,
                                    },
                                },
                            ),
                            ui.VGap(1),
                            ui.Label(
                                {
                                    "Text": "Output Path",
                                    "Weight": 0,
                                    "Alignment": {
                                        "AlignRight": True,
                                        "AlignVCenter": True,
                                    },
                                }
                            ),
                        ],
                    ),
                    ui.VGroup(
                        {
                            "Spacing": 5,
                            "Weight": 2,
                        },
                        [
                            ui.LineEdit(
                                {
                                    "ID": inputPathID,
                                    "ClearButtonEnabled": True,
                                    # "MaxLength": 10,
                                }
                            ),
                            ui.LineEdit(
                                {
                                    "ID": outputPathID,
                                    "ClearButtonEnabled": True,
                                    # "MaxLength": 10,
                                }
                            ),
                        ],
                    ),
                    ui.VGroup(
                        {
                            "Spacing": 5,
                            "Weight": 0,
                        },
                        [
                            ui.Button(
                                {
                                    "ID": browseInputFileManagerID,
                                    "Text": "Browse",
                                    "Weight": 0,
                                }
                            ),
                            ui.Button(
                                {
                                    "ID": browseOutputFileManagerID,
                                    "Text": "Browse",
                                    "Weight": 0,
                                }
                            ),
                        ],
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
                    ui.Button(
                        {
                            "ID": clearAllContentID,
                            "Text": "Clear All",
                            "Weight": 0,
                        }
                    ),
                    ui.Button(
                        {
                            "ID": addSinglePathID,
                            "Text": "Add Single Path",
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
                            "ID": proxyRunID,
                            "Text": "Run",
                            "Weight": 0,
                        }
                    )
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
                            # "Prefix": "The ",
                            # "Suffix": " Items",
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
def absolute_file_paths(path: str) -> List[str]:
    """Get the abs of all files from the input path, exclude files from
    INVALID_EXTENSION.
    """
    absolute_file_path_list = []
    for directory_path, _, filenames in os.walk(path):
        for filename in filenames:
            # Exclude invalid extension when getting abs for all files under the
            # input media path (素材)
            if filename.split(".")[1] not in INVALID_EXTENSION:
                absolute_file_path_list.append(
                    os.path.abspath(os.path.join(directory_path, filename))
                )

    return absolute_file_path_list


def get_sorted_path(path: str) -> List[str]:
    """Get the abs of all files from the input path, then sort the abs,
    and finally return a list of sorted abs.
    """
    filename_and_fullpath_dict = {
        os.path.basename(os.path.splitext(path)[0]): path
        for path in absolute_file_paths(path)
    }
    filenames = list(filename_and_fullpath_dict.keys())
    filenames.sort()
    fullpaths = [filename_and_fullpath_dict.get(i, "") for i in filenames]
    return fullpaths


def get_all_timeline() -> List[bmd_timeline.Timeline]:
    """Get all existing timelines. Return a list containing timeline object.

    Returns:
        A list containing all the timeline object in the media pool.

    """
    all_timeline = []
    for timeline_index in range(1, project.get_timeline_count() + 1, 1):
        all_timeline.append(project.get_timeline_by_index(timeline_index))
    return all_timeline


def get_subfolder_by_name(subfolder_name: str) -> Union[str, bmd_folder.Folder]:
    """Get subfolder (Folder object) under the root folder in the media
    pool.
    """
    all_subfolder = root_folder.get_sub_folder_list()
    subfolder_dict: Dict[str, bmd_folder.Folder] = {
        subfolder.get_name(): subfolder for subfolder in all_subfolder
    }
    return subfolder_dict.get(subfolder_name, "")


# Events handlers
def on_close(ev):
    """
    Close the window.
    """
    dispatcher.ExitLoop()


def on_create_bin(ev):
    path = itm[inputPathID].Text
    toolkits.add_subfolders(media_pool, root_folder, path)


def on_test_click(ev):
    print(f"{itm[inputPathID].Text}")


def on_add_all_path_to_tree(ev):
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


def on_click_input_browse_button(ev):
    selected = fusion.RequestDir()
    itm[inputPathID].Text = str(selected)[:-1]
    return selected


def on_click_output_browse_button(ev):
    selected = fusion.RequestDir()
    itm[outputPathID].Text = str(selected)[:-1]
    return selected


def on_click_tree_item(ev):
    # about to change
    current_item = itm[pathTreeID].TreePosition
    print(current_item)


def on_clear_and_restart(ev):
    """
    For the convenience of development, clear all the content in the media
    pool and switch back to Edit page.
    """
    all_timeline = get_all_timeline()
    media_pool.delete_timelines(all_timeline)
    subfolders_to_be_deleted = root_folder.get_sub_folder_list()
    media_pool.delete_folders(subfolders_to_be_deleted)
    media_pool.delete_clips(root_folder.get_clip_list())
    resolve.open_page("edit")


def on_run(ev):
    itm[proxyRunID].Enabled = False
    media_path = itm[inputPathID].Text
    proxy_path = itm[outputPathID].Text
    main(media_path, proxy_path)
    itm[proxyRunID].Enabled = True


def on_add_single_path_to_tree(ev):
    row = itm[pathTreeID].NewItem()
    row.Text[0] = itm[inputPathID].Text  # Add text to column 0
    row.Text[1] = itm[inputPathID].Text  # Add text to column 1
    itm[pathTreeID].AddTopLevelItem(row)


def build_header(treeitem):
    header = treeitem.NewItem()
    treeitem.SetHeaderItem(header)
    for i in range(0, len(tree_header)):
        info = tree_header[i]
        header.Text[i] = info["name"]
        treeitem.ColumnWidth[i] = info["width"]


tree_header = {
    0: {"name": "Header Position 0", "width": 350},
    1: {"name": "Header Position 1", "width": 250},
}

build_header(itm[pathTreeID])


# Assign events handlers
win.On.myWindow.Close = on_close
win.On[createBinID].Clicked = on_create_bin
win.On[testID].Clicked = on_test_click
win.On[addPathID].Clicked = on_add_all_path_to_tree
win.On[clearPathID].Clicked = on_clear_all_path
win.On[pathTreeID].ItemClicked = on_click_tree_item
win.On[pathParseID].Clicked = on_parse_input_path
win.On[browseInputFileManagerID].Clicked = on_click_input_browse_button
win.On[browseOutputFileManagerID].Clicked = on_click_output_browse_button
win.On[clearAllContentID].Clicked = on_clear_and_restart
win.On[proxyRunID].Clicked = on_run
win.On[addSinglePathID].Clicked = on_add_single_path_to_tree

if __name__ == "__main__":
    win.Show()
    dispatcher.RunLoop()
