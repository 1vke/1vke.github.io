---
title: "Ball State Bus Tracker (in development)"
date: 2025-03-06
draft: false
---

The Bus Tracker widget for the MyBallState app is being developed to provide real-time bus tracking, ensuring students 
and faculty can conveniently view bus locations. This project is designed to replace the previous TransLoc system with 
an in-house solution.

The widget is built with Preact, a lightweight React framework that integrates seamlessly into the MyBallState app. 
Preact was chosen over pure JavaScript for its maintainability and because our team has extensive experience with React.
The widget also leverages MapLibre with OpenFreeMap, an open-source mapping solution that eliminates hosting costs. For 
route mapping, we used OSRM (Open Source Routing Machine) to generate bus loop geometries based on bus stops. The loop 
data is stored in GeoJSON format, a structured format widely used for mapping applications.

One of the biggest challenges has been handling route visualization. Initially, we aimed to offset overlapping routes, 
similar to subway maps. However, dynamically detecting and shifting overlapping sections proved complex. Instead, we 
opted to allow route overlap while providing toggle buttons for individual visibility. Another challenge has been 
animating bus markers smoothly. I implemented transitions using requestAnimationFrame to interpolate between position 
updates, ensuring smooth movement and preventing abrupt jumps.

The project has required extensive research into digital cartography and mapping best practices. I have explored various
mapping libraries, evaluated data sources, and studied map tile types, zoom levels, and vector versus raster tiles. This
research ensures we select the best tools for the job and build a reliable system.

Once completed, this project will significantly improve campus transportation usability. Reliable tracking will reduce 
uncertainty, making bus usage more efficient for students and faculty. The removal of TransLoc left many commuters 
struggling, and this widget aims to restore essential functionality. Personally, as a former dorm resident and now an 
off-campus commuter, I understand the necessity of real-time bus tracking. Waiting in the cold or missing a bus due to a
lack of information is frustrating, and this solution seeks to mitigate those issues.

I have played a key role in this project as the sole front-end developer. I have led the front-end reseavrch, development,
and implementation of the widget, collaborating with the UX and design team on the designs and backend developers to 
integrate tracking functionalities. Ensuring feature parity with previous systems has been a top priority. This project 
is not just a one-time solution; it is expected to continue evolving, potentially leading to a native mobile app in the 
future.

Being part of a project that directly impacts the daily lives of students and faculty has been incredibly rewarding. Not 
a day goes by when I don’t hear someone wishing for a bus tracker. Knowing that I am playing a crucial role in making it 
happen is a fulfilling experience, and I look forward to seeing how this project grows.