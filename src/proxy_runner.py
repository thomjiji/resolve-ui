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

inputPathID = "Input path"
outputPathID = "Output path"
testID = "Test click"
pathTreeID = "Path tree"
clearSelectedPathID = "Clear selected path"
comboBoxID = "Combo Box"
browseInputFileManagerID = "Browse input"
browseOutputFileManagerID = "Browse output"
clear_and_restart = "Clear all content in the media pool"
proxyRunID = "Proxy run"
testAddSigleClip = "Test add single clip"


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
                            "ID": proxyRunID,
                            "Text": "Run",
                            "Weight": 0,
                        }
                    ),
                    ui.Button(
                        {
                            "ID": clear_and_restart,
                            "Text": "Clear And Restart",
                            "Weight": 0,
                        }
                    ),
                    ui.Button(
                        {
                            "ID": testID,
                            "Text": "Test",
                            "Weight": 0,
                        }
                    ),
                    ui.Button(
                        {
                            "ID": testAddSigleClip,
                            "Text": "Test Sigle",
                            "Weight": 0,
                        },
                    ),
                ],
            ),
            ui.Tree(
                {
                    "ID": pathTreeID,
                    "AlternatingRowColors": False,
                    "HeaderHidden": False,
                    "SelectionMode": "ExtendedSelection",
                    "Weight": 1,
                    "AutoScroll": True,
                    "SortingEnabled": True,
                }
            ),
        ],
    ),
)

itm = win.GetItems()
itm[pathTreeID].SetHeaderLabel("Program Message")


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


def on_test_click(ev):
    print(f"{itm[inputPathID].Text}")


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
    resolve.open_page("edit")


def on_run(ev):
    itm[proxyRunID].Enabled = False
    media_path = itm[inputPathID].Text
    proxy_path = itm[outputPathID].Text
    main(media_path, proxy_path)
    itm[proxyRunID].Enabled = True


def on_test_add_single_clip(ev):
    row = itm[pathTreeID].NewItem()
    row.Text[1] = itm[inputPathID].Text
    row.Text[0] = itm[inputPathID].Text
    itm[pathTreeID].AddTopLevelItem(row)


tree_header = {
    0: {"name": "Time", "width": 100},
    1: {"name": "Message", "width": 250},
}


def build_header(treeitem):
    header = treeitem.NewItem()
    treeitem.SetHeaderItem(header)
    for i in range(0, len(tree_header)):
        info = tree_header[i]
        header.Text[i] = info["name"]
        treeitem.ColumnWidth[i] = info["width"]


build_header(itm[pathTreeID])


# Assign events handlers
win.On.myWindow.Close = on_close
win.On[testID].Clicked = on_test_click
win.On[pathTreeID].ItemClicked = on_click_tree_item
win.On[browseInputFileManagerID].Clicked = on_click_input_browse_button
win.On[browseOutputFileManagerID].Clicked = on_click_output_browse_button
win.On[clear_and_restart].Clicked = on_clear_and_restart
win.On[proxyRunID].Clicked = on_run
win.On[testAddSigleClip].Clicked = on_test_add_single_clip

if __name__ == "__main__":
    win.Show()
    dispatcher.RunLoop()
