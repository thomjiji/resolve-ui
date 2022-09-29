ui = fusion.UIManager
dispatcher = bmd.UIDispatcher(ui)

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
                ],
            ),
            ui.HGroup(
                {
                    "Spacing": 5,
                    "Weight": 0,
                },
                [
                    ui.Button({"Text": "Clear", "Weight": 0, "Height": 0}),
                    ui.Button({"Text": "Find", "Weight": 0, "Height": 0}),
                    ui.Button({"Text": "Replace", "Weight": 0, "Height": 0}),
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

itm = win.GetItems()
print(itm)
