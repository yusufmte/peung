Note: Detecting mouse input does not seem to work on Wayland. Use Xorg.

One issue with this program is that mouse clicks captured by the program are
still sent to other applications. This results in an annoying right click menu
that needs to be dodged.

A peupy solution for now: disable mouse movement.

Here's how to do this with X:

Do
```sh
xinput --list
```
to determine the ID of the mouse you are using. Let's say it's 10.

Do
```sh
xinput --list-props 10
```
to list the configurable properties of the mouse.
Look for the id of something like "coordinate transformation matrix."
Let's say it's 181.

Do
```sh
xinput set-prop 10 181 0, 0, 0, 0, 0, 0, 0, 0, 1
```
to disable mouse movement.

To enable it again, set the matrix back to identity:
```sh
xinput set-prop 10 181 1, 0, 0, 0, 1, 0, 0, 0, 1
```
