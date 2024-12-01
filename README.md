Note: Detecting mouse input does not seem to work on Wayland. Use Xorg.

## Getting sound assets

If you have access, download [the sound assets here](https://drive.google.com/file/d/1Ky-RoYqmEFlRVsw-29jSYjuCZUNRZ-Xt/view?usp=drive_link).
Extract them into the directory that contains `peung.py`.

If you don't have access, you will have to create sound files like this inside the peung.py directory:
```txt
assets/serve_0.mp3
assets/serve_1.mp3
assets/win_0.mp3
assets/win_1.mp3
assets/serve_[PLAYERNAME].mp3
assets/win_[PLAYERNAME].mp3
assets/num_[#].mp3
assets/game_score.mp3
assets/match_score.mp3
assets/the_match.mp3
assets/factorio.mp3
assets/match_factorio.mp3
assets/deuce.mp3
assets/peuped.mp3
assets/you_peuped.mp3
```
where
- `[PLAYERNAME]` can be replaced by special player names with their own unique sounds; these are optional
- `[#]` should be replaced by integers starting from 1, so `num_1.mp3`, `num_2.mp3`, etc. to announce scores.

## Disabling mouse movement

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
