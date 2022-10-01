ui = fusion.UIManager
dispatcher = bmd.UIDispatcher(ui)


ClearID = 'Clear'

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
                    ui.LineEdit({"PlaceholderText": "Text Field"}),
                    ui.LineEdit({"PlaceholderText": "Text Field"}),
                    ui.SpinBox(
                        {
                            "Value": 2,
                            "Minimum": 1,
                            "Maximum": 99,
                            "SingleStep": 1,
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
                    ui.Button({"ID": ClearID,"Text": "Clear", "Weight": 0}),
                    ui.Button({"Text": "Find", "Weight": 0, "Height": 0}),
                    ui.Button({"Text": "Replace", "Weight": 0}),
                ],
            ),
            ui.LineEdit(
                {
                    "PlaceholderText": "example text",
                }
            ),
            ui.Tree(
                {
                    "AlternatingRowColors": True,
                    "HeaderHidden": True,
                    "SelectionMode": "ExtendedSelection",
                    "Weight": 2,
                }
            ),
        ],
    ),
)

# Define the events handlers
def OnClose(ev):
    dispatcher.ExitLoop()

def OnClear(ev):
    print("Clear button was pressed once!")
    

# Assign events handlers
win.On.myWindow.Close = OnClose
win.On[ClearID].Clicked = OnClear


if __name__ == "__main__":
    win.Show()
    dispatcher.RunLoop()
