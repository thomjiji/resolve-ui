ui = fusion.UIManager
dispatcher = bmd.UIDispatcher(ui)

win = dispatcher.AddWindow(
    {
        "ID": "myWindow",
        "WindowTitle": "sample",
    },
    ui.VGroup(
        {"Spacing": 5},
        [
            ui.HGroup(
                {
                    "Spacing": 5,
                },
                [
                    ui.LineEdit(
                        {
                            "PlaceholderText": "This is a placeholder"
                        }
                    ),
                    ui.LineEdit(
                        {
                            "PlaceholderText": "This is another placeholder"
                        }
                    ),
                ],
            ),
            ui.HGroup(
                {
                    "Spacing": 5,
                },
                [
                    ui.Button({"Text": "Clear", "Weight": 0, "Height": 0}),
                    ui.Button({"Text": "Find", "Weight": 0, "Height": 0}),
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


def OnClose(ev):
    dispatcher.ExitLoop()


win.On.myWindow.Close = OnClose

win.Show()
dispatcher.RunLoop()