
class MessageText():

    usage_text = (
        """
        <h1> Usage </h1>

        <h2> Reading frame from the connected camera </h2>
        The view area on the left of the window shows frame from the connected camera. The frame
        switching automatically every time read frame.

        <h2> Button action </h2>
        Pressing each button on top of the window works as follows.
        <ul>
            <li> Quit (Ctrl + q)
                <ul> Finish this program. </ul>
            </li>
            <li> Save (Ctrl + s)
                <ul> Save the current frame. </ul>
            </li>
            <li> Stop (Ctrl + s)
                <ul> Pause reading frame from usb camera. </ul>
                <ul> When pressed, stop button's text changes "Start".</ul>
                <ul> When pressed again, Resume reading frame.</ul>
            </li>
            <li> Usage (Ctrl + h)
                <ul> Show this usage. </ul>
            </li>
            <li> Light / Dark (Ctrl + t)
                <ul> Switch theme of the main window to the other. </ul>
            </li>
            <li> Record (Experimental) (Ctrl + r)
                <ul> Start recoding. </ul>
            </li>
        </ul>

        <h2> Change parameters </h2>
        The sliders on right of the window allow users to change values of parameter interactively.
        The string on the left of slider shows parameter's name, the label on the right
        does its current value.

        <h2> Coordinates and pixel value </h2>
        The status bar below the window shows the coordinates and values (RGBA) of
        the pixel where the pointer is placed.


        """)

    about_text = (
        """
        About the program

        Visit https://github.com/git-ogawa/usbcamGUI
        """
    )

    keylist = [
            ["Ctrl + a", "About the program"],
            ["Ctrl + d", "Set parameters to default value"],
            ["Ctrl + f", "Change font"],
            ["Ctrl + h", "Show usage"],
            ["Ctrl + k", "Show the list of Keyboard shortcut"],
            ["Ctrl + l", "Show the list of paramaters supported by camera"],
            ["Ctrl + n", "Change naming convension of filename"],
            ["Ctrl + p", "Stop reading frame"],
            ["Ctrl + q", "Exit the program"],
            ["Ctrl + r", "Start recording"],
            ["Ctrl + s", "Save the current frame"],
            ["Ctrl + t", "Switch theme ( Light/Dark )"],
        ]