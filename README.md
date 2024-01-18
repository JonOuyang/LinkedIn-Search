### I don't like LinkedIn

# Tesseract
This program manually interacts with a half screen page of LinkedIn using Pytesseract, pyautogui, and computer vision to see what is currently on the screen. This method is emulates mouse and keystrokes (extremely inefficient but necessary when dealing with non-HTML).

# Selenium
This program is a more practical solution, using the HTML code of a website to interact with it rather than emulating mouse movements and keystrokes. Note: requires chrome driver. To find the specific element use inspect element once to open the HTML code and then right click on desired element and hit inspect to jump to the HTML code responsible for element.

https://www.geeksforgeeks.org/scrape-linkedin-using-selenium-and-beautiful-soup-in-python/ 
