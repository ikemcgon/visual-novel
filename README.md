
# Customizeable Visual Novel Engine
This is a little pet project by Isaac McGonagle. I hope you enjoy it :)  

Customizable visual novel engine to provide authors the capability to use words, images, and sounds to tell interactive stories. This engine was developed using Python3 using OpenCV and multiprocessing to concurrently display visuals and audio. The final product involves PyInstaller, which treats Python like a compiled language, in order to generate an easy to use executable (.exe) file.
# How to play
Download the contents to a directory of your choosing. Run the 'visual-novel.exe' to start the game.

*Note: Executable file is compiled for Windows 10 and will not run on other operating systems. For execution on Mac or Linux, execute main.py using a Python3 installation.*

## Main Menu
### Menu Items
New Game - Start the game from the beginning of the script  
Continue - Start the game from a loaded save state (Save file location: data/save.csv)  
Exit - Close the program  

### Controls
Up/Down Arrow Key - Navigate through menu items  
Enter Key - Select the highlighted menu item  
Esc Key - Close the program  

## Mid-Game
### Controls
Enter Key - Progress to next frame  
Esc Key - Close the program. Creates a save state of your current progress (Save file location: data/save.csv)  

# How to Develop Your Own Visual Novel
## Script
The script is the primary source document for controlling the visual novel. It tells the platform which assets to load, when to load them, and the accompanying text to display. The script is a simple text document that uses ':' as a delimiter to convey all the information for any particular frame.   
Each line of the text file contains a definition for either a *scene* or a *frame*. A scene definition contains information about the background and *must* precede the frames that will utilize it. A frame definition depicts the content in the foreground such as the speaking character, their name, and the text that they are speaking.   
Below are templates, followed by a demonstration:   
**Scene Definition**      
> SCENE:backGroundMusic:backGroundImage   
> SCENE:BeautifulDays.wav:HopesPeak.jpg

**Frame Definition**   
> foreGroundImage:voiceClip:speakerName:displayText   
> Nagito2.png:NagitoLaugh1.wav:Nagito:Have you considered that despair is a stepping stone for hope?

Script Location: *data/script.txt*   

## Assets
### Image Files
Background Images should consist of images intended persist throughout the course of a scene. Foreground Images should consist of images (generally with transparency) that are intended to be used on a frame-by-frame basis.
*Directories:*
 - '*bg*' - Background Images 
 - '*fg*' - Foreground Images

*NOTE: Image files must be of the filetype .png or .jpg*   

### Sound Files
Background Music should contain longer tracks that are intended to be repeated over the course of a scene. Voice Clips should be short sounds intended to play once during a single frame.   

*Directories:*
 - '*ost*' - Background Music 
 - '*vc*' - Voice Clips

*NOTE: Sound files must be of the filetype .wav*
