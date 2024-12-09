Note: Detecting mouse input does not seem to work on Wayland. Use Xorg.

## TTS and sound assets

When Peung runs, it will make the sound asset directory (if it does not exist) and tell you where this is.
If a sound file exists, peung will use it. If it does not exist, a text-to-speech file will be made for the sound.
The TTS audio file can then be replaced with custom audio if desired.

## Getting sound assets

If you have access, download [the sound assets here](https://drive.google.com/file/d/1Ky-RoYqmEFlRVsw-29jSYjuCZUNRZ-Xt/view?usp=drive_link).
Extract the assets into the application data directory.

## Optional chimes

Three "chimes" currently are optional, and will play only if the corresponding file already exists in the assets directory - "undo_chime.mp3", "victory_chime.mp3", and "grand_victory_chime.mp3".

## Disabling mouse movement

One issue with peung is that mouse clicks captured by the program are
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
