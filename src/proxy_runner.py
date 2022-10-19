import os
from pprint import pprint
import re
from typing import Union
from resolve_toolkits import main
from pybmd import Bmd
from pybmd import timeline as bmd_timeline
from pybmd import folder as bmd_folder

# Constants
INVALID_EXTENSION = ["DS_Store", "JPG", "JPEG", "SRT"]

# Initialize Resolve base object using pybmd
resolve = Bmd()
project = resolve.get_project_manager().get_current_project()
media_pool = project.get_media_pool()
root_folder = media_pool.get_root_folder()
media_storage = resolve.get_media_stroage()

# Initialize the UI
fusion = bmd.scriptapp("Fusion")  # type: ignore
ui = fusion.UIManager
dispatcher = bmd.UIDispatcher(ui)  # type: ignore

# Declare UI elements ID
inputPathID = "Input path"
outputPathID = "Output path"
testID = "Test click"
pathTreeID = "Path tree"
clearSelectedPathID = "Clear selected path"
comboBoxID = "Combo Box"
browseInputFileManagerID = "Browse input"
browseOutputFileManagerID = "Browse output"
clearAndRestartID = "Clear all content in the media pool"
proxyRunID = "Proxy run"
testAddSingleClip = "Test add single clip"
clearAllMessageID = "Clear all message"


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
                            "ID": proxyRunID,
                            "Text": "Run",
                            "Weight": 0,
                        }
                    ),
                    ui.Button(
                        {
                            "ID": clearAndRestartID,
                            "Text": "Clear And Restart",
                            "Weight": 0,
                        }
                    ),
                    ui.Button(
                        {
                            "ID": clearAllMessageID,
                            "Text": "Clear All Message",
                            "Weight": 0,
                        }
                    ),
                    ui.Button(
                        {
                            "ID": testAddSingleClip,
                            "Text": "Test Single Add",
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


# Get items of the UI
itm = win.GetItems()

tree_header = {
    0: {"name": "Time", "width": 100},
    1: {"name": "Message", "width": 250},
}


# General functions
def absolute_file_paths(path: str) -> list[str]:
    """
    Get the abs of all files from the input path, exclude files from
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


def get_sorted_path(path: str) -> list[str]:
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
    fullpaths = [filename_and_fullpath_dict.get(i, "") for i in filenames]
    return fullpaths


def get_all_timeline() -> list[bmd_timeline.Timeline]:
    """
    Get all existing timelines. Return a list containing timeline object.

    Returns
    --------
    list
        A list containing all the timeline object in the media pool.

    """
    all_timeline = []
    for timeline_index in range(1, project.get_timeline_count() + 1, 1):
        all_timeline.append(project.get_timeline_by_index(timeline_index))
    return all_timeline


def get_subfolder_by_name(subfolder_name: str) -> Union[str, bmd_folder.Folder]:
    """
    Get subfolder (Folder object) under the root folder in the media
    pool.
    """
    all_subfolder = root_folder.get_sub_folder_list()
    subfolder_dict: dict[str, bmd_folder.Folder] = {
        subfolder.get_name(): subfolder for subfolder in all_subfolder
    }
    return subfolder_dict.get(subfolder_name, "")


def build_header(tree_item):
    """
    Build the header of the tree.

    tree_item is TreeItem element, this func take TreeItem as input.
    """
    header = tree_item.NewItem()
    tree_item.SetHeaderItem(header)
    for i in range(0, len(tree_header)):
        info = tree_header[i]
        header.Text[i] = info["name"]
        tree_item.ColumnWidth[i] = info["width"]


def read_logs() -> list[str]:
    """
    Read line by line from a fixed path log file and store each line in a list,
    each line is an element of the list.
    """
    with open("/Users/thom/code/resolve-ui/src/log/proxy_runner.log", "r") as f:
        log_lines = [line.strip() for line in f.readlines()]
        return log_lines


def _add_logs(log_lines: list[str]) -> None:
    for log_line in log_lines:
        row = itm[pathTreeID].NewItem()
        row.Text[0] = re.findall(r"\d{2}:\d{2}:\d{2}", log_line)[0]
        row.Text[1] = log_line.split(":")[3].strip()
        itm[pathTreeID].AddTopLevelItem(row)


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
    media_pool.delete_clips(root_folder.get_clip_list())
    resolve.open_page("edit")


def on_run(ev):
    itm[proxyRunID].Enabled = False
    media_path = itm[inputPathID].Text.strip()
    proxy_path = itm[outputPathID].Text.strip()
    main(media_path, proxy_path)
    _add_logs(read_logs())
    itm[proxyRunID].Enabled = True


def on_test_add_single_clip(ev):
    pass


def on_clear_all_message(ev):
    itm[pathTreeID].Clear()


# Assign events handlers
win.On.myWindow.Close = on_close
win.On[testID].Clicked = on_test_click
win.On[pathTreeID].ItemClicked = on_click_tree_item
win.On[browseInputFileManagerID].Clicked = on_click_input_browse_button
win.On[browseOutputFileManagerID].Clicked = on_click_output_browse_button
win.On[clearAndRestartID].Clicked = on_clear_and_restart
win.On[proxyRunID].Clicked = on_run
win.On[testAddSingleClip].Clicked = on_test_add_single_clip
win.On[clearAllMessageID].Clicked = on_clear_all_message

build_header(itm[pathTreeID])

if __name__ == "__main__":
    win.Show()
    dispatcher.RunLoop()
