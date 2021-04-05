# StoryBoard

# Importing

I can recomend using LiberOffice, just use set seperator to `|` and turn off other separators (character `,` can be used in text)
> Excel have some issues, im don't recomend using it for manipulation of storyboard with it 

# First line:
- `no` - It is not used, but useful for jumps to quickly glanced at
- `action` - Which action is going to be made
- `value1`/`value2` - Values for action
- `set1`/`set2` - Values for values (used only in choice action)
- `person` - Name of character
- `text` - Text written in text box (only in text action)

# Actons 

### 0. Text
- `value1` - Speed of text (from 0 to 9, where 0 is the fastest)
- `person` - Name of person speaking
- `text` - Text to show, partly supports [syntax HTML]([https://pythonhosted.org/pyglet/api/pyglet.text.formats.html-module.html](https://pythonhosted.org/pyglet/api/pyglet.text.formats.html-module.html))
### 1. Choice
- `value1`/`value2` - Text to choice boxes
- `set1`/`set1` - Story index to jump to after choice
### 2. Jump
- `value1` - Jumps to this value
### 3. Character creation
- `value1` - Name of file in `res/char/` (including extension)
- `value2` - Position in pixels of character to be created on  
- `person` - Name of the character for later manipulation
### 4. Moving character
- `person` - Name of the character
-  `value1` - Number of pixels for characters to be moved  
### 5. Removing character
- `person` - Name of character to be removed
### 6. Change background
- `value1` - Name of the file `res/bg/` (including extension)
### 7. Darkening screen
- `value1` - `1` darken, `0` - revert
### 8. odpalenie dzwięku
- `value1` - Name of file in `res/sfx/` (including extension)
### 9. ukrycie pola z tekstem
- None, but with any text action text box shows up automatically
