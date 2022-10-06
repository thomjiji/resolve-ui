# Sample Workflow Integration script

import sys

# some element IDs
winID = "com.blackmagicdesign.resolve.SampleWIScript"  # should be unique for single instancing
textID = "TextEdit"
execID = "Exec"
clearID = "Clear"

ui = fusion.UIManager
dispatcher = bmd.UIDispatcher(ui)

# check for existing instance
win = ui.FindWindow(winID)
if win:
    win.Show()
    win.Raise()
    exit()

# otherwise, we set up a new window, with HTML header (using the Examples logo.png)
logoPath = fusion.MapPath(
    r"AllData:../Support/Developer/Workflow Integrations/Examples/SamplePlugin/img/logo.png"
)
header = '<html><body><h1 style="vertical-align:middle;">'
header = header + '<img src="' + logoPath + '"/>&nbsp;&nbsp;&nbsp;'
header = header + "<b>Resolve_Workflow_Integrations Sample Workflow Integration Script</b>"
header = header + "</h1></body></html>"

# define the window UI layout
win = dispatcher.AddWindow(
    {
        "ID": winID,
        "Geometry": [100, 100, 600, 500],
        "WindowTitle": "Resolve_Workflow_Integrations Sample Workflow Script",
    },
    ui.VGroup(
        [
            ui.Label(
                {
                    "Text": header,
                    "Weight": 0.1,
                    "Font": ui.Font({"Family": "Times New Roman"}),
                }
            ),
            ui.Label(
                {
                    "Text": "Workflow script",
                    "Weight": 0,
                    "Font": ui.Font({"Family": "Times New Roman", "PixelSize": 12}),
                }
            ),
            ui.TextEdit(
                {
                    "ID": textID,
                    "TabStopWidth": 28,
                    "Font": ui.Font(
                        {
                            "Family": "Sans Mono",
                            "PixelSize": 12,
                            "MonoSpaced": True,
                            "StyleStrategy": {"ForceIntegerMetrics": True},
                        }
                    ),
                    "LineWrapMode": "NoWrap",
                    "AcceptRichText": False,
                    # Use python lexer for syntax highlighting; other options include lua, html, json, xml, markdown, cpp, glsl, etc...
                    "Lexer": "python",
                }
            ),
            ui.HGroup(
                {
                    "Weight": 0,
                },
                [
                    ui.Button({"ID": execID, "Text": "Execute"}),
                    ui.HGap(2),
                    ui.Button({"ID": clearID, "Text": "Clear"}),
                    ui.HGap(0, 2),
                ],
            ),
        ]
    ),
)


# Event handlers
def OnClose(ev):
    dispatcher.ExitLoop()


def OnExec(ev):
    script = win.Find(textID).PlainText

    # run the user's script
    exec(script)


def OnClear(ev):
    win.Find(textID).PlainText = ""


# assign event handlers
win.On[winID].Close = OnClose
win.On[execID].Clicked = OnExec
win.On[clearID].Clicked = OnClear

# Sample script
deftext = """
project = resolve.GetProjectManager().CreateProject("Hello World");
"""

win.Find(textID).PlainText = deftext

# Main dispatcher loop
win.Show()
dispatcher.RunLoop()