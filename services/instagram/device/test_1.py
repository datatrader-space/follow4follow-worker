import subprocess
import time
import random
from uiautomator import Device
# Delay between actions
ACTION_DELAY = 3
# Initialize the UI Automator device
d = Device()
# Function to generate a unique screenshot file name
def generate_screenshot_name(index, action):
    timestamp = int(time.time())  # Current Unix timestamp
    return f"tiktok_screenshot_{index}_{action}_{timestamp}.png"
# Function to simulate swiping, liking, following, and capturing screenshots
def simulate_actions(num_swipes):
    for index in range(num_swipes):
        # Open TikTok app
        subprocess.run(["adb", "shell", "am", "start", "-n", "com.zhiliaoapp.musically/com.ss.android.ugc.aweme.splash.SplashActivity"])
        time.sleep(ACTION_DELAY)
        # Simulate swiping through Explore section
        for _ in range(5):
            subprocess.run(["adb", "shell", "input", "swipe", "500", "1500", "500", "1000"])
            time.sleep(1)
        # Click on a random video
        video_x = random.randint(300, 1000)
        video_y = random.randint(300, 800)
        subprocess.run(["adb", "shell", "input", "tap", str(video_x), str(video_y)])
        time.sleep(ACTION_DELAY)
        # Simulate follow action
        subprocess.run(["adb", "shell", "input", "tap", "672", "1216"])  # Adjust X and Y for follow
        time.sleep(ACTION_DELAY)
        # Simulate like action
        subprocess.run(["adb", "shell", "input", "tap", "672", "962"])  # Adjust X and Y for like
        time.sleep(ACTION_DELAY)
        # Extract user information
        username_element = d(resourceId="com.zhiliaoapp.musically:id/mfb")
        followers_element = d(resourceId="com.zhiliaoapp.musically:id/df3")
        following_element = d(resourceId="com.zhiliaoapp.musically:id/dfd")
        username = username_element.text
        followers = followers_element.text
        following = following_element.text
        # Print user information
        print("Username:", username)
        print("Followers:", followers)
        print("Following:", following)
        # Take a screenshot after liking and following
        like_follow_screenshot_name = generate_screenshot_name(index, "like_follow")
        subprocess.run(["adb", "shell", "screencap", "-p", "/sdcard/" + like_follow_screenshot_name])
        subprocess.run(["adb", "pull", "/sdcard/" + like_follow_screenshot_name, like_follow_screenshot_name])
        time.sleep(ACTION_DELAY)
        # Tap to open user profile and fetch username
        subprocess.run(["adb", "shell", "input", "tap", "70", "1358"])  # Adjust X and Y for username
        time.sleep(ACTION_DELAY)
        # Take a screenshot after going to the specified coordinates
        coordinate_screenshot_name = generate_screenshot_name(index, "coordinates")
        subprocess.run(["adb", "shell", "screencap", "-p", "/sdcard/" + coordinate_screenshot_name])
        subprocess.run(["adb", "pull", "/sdcard/" + coordinate_screenshot_name, coordinate_screenshot_name])
        time.sleep(ACTION_DELAY)
        # Go back to Explore
        subprocess.run(["adb", "shell", "input", "keyevent", "4"])
        time.sleep(ACTION_DELAY)
# Main function
def main():
    num_swipes = 5  # Adjust the number of swipes you want to perform
    print(f"Performing {num_swipes} TikTok swipes, likes, follows, and screenshots...")
    simulate_actions(num_swipes)
    print("Actions completed!")
if __name__ == "__main__":
    main()