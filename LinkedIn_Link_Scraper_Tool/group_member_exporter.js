function linkgetter() {
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
 
        // Save the links to a text file
        var textToSave = links.join('\n');
        var blob = new Blob([textToSave], { type: 'text/plain' });
        var a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        a.download = 'links_h1.txt';
        a.click();
    } else {
        console.log("Ul element not found!");
    }
}
 
linkgetter()  
