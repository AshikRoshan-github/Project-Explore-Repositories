// Function to count the number of links
function countLinks() {
   // Select the ul element with the specified class
   var ulElement = document.querySelector('ul.artdeco-list.groups-members-list__results-list');
   if (ulElement) {
       // Select all the li elements within the ul element
       var liElements = ulElement.querySelectorAll('li.artdeco-list__item.groups-members-list__typeahead-result.relative.p0');
       var links = []; // Array to store the extracted links
       // Loop through each li element
       liElements.forEach(function(li) {
           // Find the anchor tag within each li element
           var anchorTag = li.querySelector('a');
           // Check if anchorTag exists and has an href attribute
           if (anchorTag && anchorTag.href) {
               // Push the href attribute value to the links array
               links.push(anchorTag.href);
           }
       });
       // Print the count of links
       console.log("Total links:", links.length);
       return links;
   } else {
       console.log("Ul element not found!");
       return [];
   }
}
 
 
// Recursive function to click the "Show More Results" button and count links until 433 links are found
function clickShowMoreAndCount(links) {
   // Check if the count has reached 433
   if (links.length >= 500) {
       console.log("Reached the target member count. Stopping the program.");
       // Display the list of links
       console.log('over');
   } else {
       // If the count is less than 433, click the "Show More Results" button
       var showMoreButton = document.querySelector('.artdeco-button.artdeco-button--muted.artdeco-button--1.artdeco-button--full.artdeco-button--secondary.ember-view.scaffold-finite-scroll__load-button');
       if (showMoreButton) {
           // Clear the list of links
           links = [];
           // Simulate a click event on the button
           showMoreButton.click();
           // Wait for a moment for the new content to load
           setTimeout(function() {
               // Recursively call the function after clicking the button
               clickShowMoreAndCount(countLinks());
           }, 5000); // 15 second delay
       } else {
             
            console.log("Show More Results button not found.");
       }
   }
}
 
 
// Start the process
clickShowMoreAndCount([]);

