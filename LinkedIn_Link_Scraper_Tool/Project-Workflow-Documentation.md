The Process consists of two parts designed to extract member profile links from a LinkedIn group page. Here's an architectural breakdown:

Part 1: Iterative Link Counting and "Show More" Clicking

Purpose: This part aims to load all group members by repeatedly clicking the "Show More Results" button until a target number of members (500) is reached or the button is no longer available.

Architecture:

countLinks() function:

Input: None (operates on the current page DOM).

Process: Queries the DOM for the list of member elements (ul.artdeco-list...) and extracts the href attribute from each member's profile link (a tag).

Output: Returns an array of extracted links and prints the total number of links found on the current page to the console.

clickShowMoreAndCount() function (recursive):

Input: An array of currently extracted links (links).

Process:

Base Case: If the links array length is 500 or more, it logs a message to the console indicating the target count has been reached.

Recursive Step: If the links array length is less than 500, it queries the DOM for the "Show More Results" button.

If the button is found:

Clears the links array.

Simulates a click on the button using showMoreButton.click().

Waits for 5 seconds (using setTimeout) to allow new content to load.

Recursively calls itself with the result of countLinks(), which retrieves the updated list of links after the "Show More" click.

If the button is not found: Logs a message that the button was not found.

Flow: The clickShowMoreAndCount() function is initially called with an empty array. It iteratively calls countLinks() to extract links, clicks "Show More," waits for the page to update, and repeats until the target member count is met or the "Show More" button disappears.

Part 2: Link Extraction and Saving

Purpose: This part extracts all loaded member profile links and saves them to a text file.

Architecture:

linkgetter() function:

Input: None (operates on the current page DOM).

Process: Similar to countLinks(), it queries the DOM for the list of member elements and extracts the href attributes.

Output:

Prints the total number of links to the console.

Creates a Blob containing the links separated by newline characters.

Creates a downloadable link element (a tag) and triggers a download with the filename links_h1.txt.

Flow: After Part 1 completes (the page is fully loaded with members), linkgetter() is called to extract all the links and initiate the file download.

Overall Architecture Diagram:

Part 1 :

![image](https://github.com/user-attachments/assets/ae43fa7b-360e-461e-89cc-ea66655d78eb)

Part 2:

![image](https://github.com/user-attachments/assets/868bb4e7-66ba-42de-a69b-a17ce608a249)

