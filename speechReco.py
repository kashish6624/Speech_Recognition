import wmi
import speech_recognition as sr
import os
import webbrowser
import subprocess
import pyautogui  # For automating tasks like clicks, volume
import screen_brightness_control as sbc  # For brightness control
import pygetwindow as gw  # To get active window title


recognizer = sr.Recognizer()

def capture_voice_input():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    return audio

def convert_voice_to_text(audio):
    try:
        text = recognizer.recognize_google(audio)
        print("You said: " + text)
    except sr.UnknownValueError:
        text = ""
        print("Sorry, I didn't understand that.")
    except sr.RequestError as e:
        text = ""
        print(f"Error; {e}")
    return text

def process_voice_command(text):
    text = text.lower()
    active_window = gw.getActiveWindowTitle()

    # Check active window and display for debugging
    if active_window:
        print(f"Active Window: {active_window}")
    else:
        print("No active window detected.")

    # Greeting and Goodbye
    if "hello" in text:
        print("Hello! How can I help you?")
    elif "goodbye" in text or "exit" in text:
        print("Goodbye! Have a great day!")
        return True

    # System control commands
    elif "shut down" in text:
        print("Shutting down the computer...")
        os.system("shutdown /s /t 1")
    elif "restart" in text:
        print("Restarting the computer...")
        os.system("shutdown /r /t 1")
    elif "lock the screen" in text:
        print("Locking the screen...")
        os.system("rundll32.exe user32.dll, LockWorkStation")
    
    # Volume Control
    elif "increase volume" in text:
        pyautogui.press("volumeup", presses=5)
        print("Increasing volume...")
    elif "decrease volume" in text:
        pyautogui.press("volumedown", presses=5)
        print("Decreasing volume...")
    elif "mute" in text:
        pyautogui.press("volumemute")
        print("Muting the sound...")
    elif "unmute" in text:
        pyautogui.press("volumemute")  # Pressing "mute" key again unmutes if it's currently muted
        print("Unmuting the sound...")

    # Brightness control using screen_brightness_control library
    elif "increase brightness" in text:
        current_brightness = sbc.get_brightness(display=0)  # Get brightness of the first display
        if isinstance(current_brightness, list):
            current_brightness = current_brightness[0]  # Handle multiple monitors if necessary
        new_brightness = min(current_brightness + 10, 100)  # Cap brightness at 100%
        sbc.set_brightness(new_brightness)
        print(f"Increasing brightness to {new_brightness}%")
    elif "decrease brightness" in text:
        current_brightness = sbc.get_brightness(display=0)  # Get brightness of the first display
        if isinstance(current_brightness, list):
            current_brightness = current_brightness[0]  # Handle multiple monitors if necessary
        new_brightness = max(current_brightness - 10, 0)  # Do not go below 0%
        sbc.set_brightness(new_brightness)
        print(f"Decreasing brightness to {new_brightness}%")

    # Determine if we are controlling a browser or media player
    is_browser = "chrome" in active_window.lower() or "firefox" in active_window.lower() if active_window else False
    is_vlc = "vlc" in active_window.lower() if active_window else False
    is_wmp = "windows media player" in active_window.lower() if active_window else False

    # Mouse control commands for video control
    if "double click right" in text:
        if is_browser:
            pyautogui.press("right")  # Skips forward 5 seconds (depends on media player)
        elif is_vlc:
            pyautogui.hotkey('ctrl', 'right')  # Skip forward in VLC
        elif is_wmp:
            pyautogui.hotkey('ctrl', 'shift', 'f')  # Skip forward in Windows Media Player
        print("Double clicked right, skipping forward.")
    
    elif "double click left" in text:
        if is_browser:
            pyautogui.press("left")  # Skips backward 5 seconds (depends on media player)
        elif is_vlc:
            pyautogui.hotkey('ctrl', 'left')  # Skip backward in VLC
        elif is_wmp:
            pyautogui.hotkey('ctrl', 'shift', 'b')  # Skip backward in Windows Media Player
        print("Double clicked left, skipping backward.")
    
    elif "pause" in text or "play" in text:
        if is_browser or is_vlc or is_wmp:
            pyautogui.press("space")  # Spacebar toggles pause/play in most media players
        print("Toggling play/pause.")

    # File Management
    elif "open documents" in text:
        print("Opening Documents folder...")
        os.startfile(r'')  # Change path accordingly
    elif "create folder" in text:
        folder_name = text.split("create folder")[-1].strip()
        os.makedirs(os.path.join(os.getcwd(), folder_name))
        print(f"Created folder '{folder_name}'")
    elif "open file" in text:
        file_path = text.split("open file")[-1].strip()
        try:
            os.startfile(file_path)
            print(f"Opening file '{file_path}'")
        except FileNotFoundError:
            print(f"File '{file_path}' not found. Please provide a valid path.")

    # Web Browsing
    elif "open google" in text:
        print("Opening Google...")
        webbrowser.open("https://www.google.com")
    elif "search" in text:
        query = text.split("search for")[-1].strip()
        print(f"Searching for {query}...")
        webbrowser.open(f"https://www.google.com/search?q={query}")

    # Application Control
    elif "open word" in text:
        print("Opening Microsoft Word...")
        os.startfile(r'')  # Change path as per your installation
    elif "open chrome" in text:
        print("Opening Google Chrome...")
        os.startfile(r'')
    elif "open excel" in text:
        print("Opening Microsoft Excel...")
        os.startfile(r'')  # Change path as per your installation

    # Handle unrecognized commands
    else:
        print("I didn't understand that command. Please try again.")
    
    return False

def main():
    end_program = False
    while not end_program:
        audio = capture_voice_input()
        text = convert_voice_to_text(audio)
        end_program = process_voice_command(text)

if __name__ == "__main__":
    main()

