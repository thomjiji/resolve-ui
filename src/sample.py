import os
from pybmd import Bmd
from pybmd import toolkits

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
                            "PlaceholderText": "Please enter the media full path here",
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
                    "HeaderHidden": True,
                    "SelectionMode": "ExtendedSelection",
                    "Weight": 1,
                    "AutoScroll": True,
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


# Genaral functions


# Define the events handlers
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
    input_path = itm[inputPathID].Text
    # 从 input path 的 raw 路径里，通过 get_sub_folder_list 方法拿到该 raw 路径下的
    # 子路径
    input_subpath_list = media_storage.get_sub_folder_list(input_path)
    cam_name = [os.path.split(i)[1] for i in input_subpath_list]
    print(cam_name)

    top_level_items = []
    for i in cam_name:
        row = itm[pathTreeID].NewItem()
        row.Text[0] = i
        top_level_items.append(row)
    itm[inputPathID].AddTopLevelItems(top_level_items)


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
