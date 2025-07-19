---
title: "Inventory Management System"
date: 2025-03-01
draft: false
---
![Inventory management system](/portfolio/inventory-management/thumbnail.png) 

In my senior year of high school, I built a web application that allowed users to scan devices into a database and 
generate barcodes for each one. When a barcode was scanned, the system would pull up all relevant device data on a 
dedicated page, or add the device to the database if the code didn’t exist, depending on how the settings were 
configured.

At the time, my teacher was teaching Python, but since I already had some experience with it, he encouraged me to take 
on a more advanced project. I chose to develop this system, despite having no prior experience with the framework I used
or working with databases. Over the course of six weeks, I learned both on the fly and successfully built a functional 
solution.

In terms of functionality, the system featured a barcode scanner that accepted input from either a USB scanner or a 
keyboard, triggering an action when the Enter key was pressed. Since most USB barcode scanners append an Enter key after
scanning, the system was designed to process the input accordingly. If the scanned item was already in the database, 
the system would navigate to its dedicated product page; otherwise, if the appropriate settings were enabled, it would 
add the item to the database. Additionally, a commit history tracked all items added to the system. The application also
included an asset viewer, which displayed paginated results from the database and allowed for inline editing of certain 
columns. Each item had its own dedicated page showing detailed information and listing any associated comments. Another 
key feature was the report generator, which enabled users to define custom filters, search through the database, and 
generate a summary page followed by a detailed list of matching items.

Looking back, both the code and the technology stack could be improved, as well as the overall structure and planning of
the system. However, as a first major project, it was a valuable learning experience in web development, databases, and 
problem-solving.

This project is especially meaningful to me because I see it as the true beginning of my software development journey. 
Before this, I had worked on class assignments and small personal projects, but this was the first time I took an idea, 
planned it out, built it, and watched it being used in a real-world setting. It was an entirely new experience—one that 
made me realize how much I love solving real problems by creating real solutions. Seeing something I built make an 
impact, albeit small, was incredibly rewarding, and it solidified my passion for software development. This project not 
only pushed me to learn new technologies but also gave me the confidence to take on bigger challenges in the future. I 
credit this project as the reason I am where I am today.