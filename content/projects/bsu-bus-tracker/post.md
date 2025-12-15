---
title: "Ball State Bus Tracker Widget"
date: 2025-12-06
draft: false
---

{{< figure src="/projects/bsu-bus-tracker/thumbnail.jpg" alt="Lucas standing in front of a TV that is displaying a live advert of the Ball State Bus Tracker widget when it was first released to students in the beginning of the fall semester." caption="Me standing in front of a digital signage display promoting the new bus tracker launch. I was honestly so excited in this picture! Also, this was just a website, so the tracker was live and interactive, super cool. S/O Digital Corps!" >}}

Waiting in the freezing Indiana winter for a bus that never shows up is a rite of passage for many Ball State students. When the previous tracking system, TransLoc, disappeared without notice, the campus was understandably upset and so was I. 

I immediately started egging on my superiors at the Digital Corps, convinced that we had the talent to build a better, in-house solution. As it turned out, the university's Transportation Department came to us looking for answers amidst the student outrage. It became an official Digital Corps project, and I jumped at the chance to be the sole front-end developer. As a daily commuter myself, I was building this for me as much as for the thousands of other students left in the cold.

## The Tech Stack

We needed a solution that was lightweight, maintainable, and cost-effective.

*   **Preact:** I chose Preact for its tiny footprint. It integrates seamlessly into the existing app while allowing us to use the React ecosystem our team is already comfortable with.
*   **MapLibre & Protomaps:** To avoid the high costs of commercial mapping APIs, we leveraged Protomaps with MapLibre. We host a specific PMTiles archive of the campus area on an AWS S3 bucket, giving us a robust, self-contained vector mapping solution. Utilizing Protomaps also meant we didn't have to make a map style, as it comes with some great out of the box styling!
*   **Data Pipeline:** We used the Open Source Routing Machine (OSRM) to generate precise route geometries from our bus stops, storing everything in GeoJSON for easy consumption.

## Engineering Challenges

### **The "Subway Map" Problem**  
One of our biggest hurdles was visualizing overlapping routes. We initially aimed for a dynamic "subway style" map where lines would automatically offset to avoid clutter. However, detecting and shifting overlapping sections dynamically proved to be an incredibly complex algorithmic challenge. We pivoted to a more user-centric approach: allowing users to toggle individual routes on and off. This keeps the interface clean while giving users control over what they see, while giving the developers a better development experience

### **Choosing the Right Map Stack**
Selecting the right mapping interface was critical. While Google Maps was the precedent set by TransLoc, its pricing model was prohibitive for our budget. I needed a solution that was cost-effective without sacrificing performance. I evaluated several options, including AWS Location Service, Leaflet, and OpenFreeMap. Ultimately, I settled on **MapLibre** paired with **Protomaps**. This combination offered the perfect balance of vector-based performance and self-hosted control, allowing us to deliver a high-quality map without the recurring costs of a commercial provider.

### **Generating Accurate Routes**
Early in development, our bus routes were simple straight lines connecting stops. They looked unnatural and ignored the actual road geometry. I quickly realized that manually drawing GeoJSON paths was not scalable or maintainable for the administrators. I needed a way to snap these paths to the road network automatically. I discovered **OSRM (Open Source Routing Machine)**, which allowed me to feed in a list of bus stops and receive a precise, road-aligned GeoJSON route in return. This turned a tedious manual task into an automated, accurate pipeline.

### **Navigating Platform Constraints**
The tracker lives as a widget inside an iFrame within the MyBallState app (powered by Pathify). This presented significant integration challenges. We had no direct control over the host environment, meaning any issues with the parent app had to be relayed to the vendor, often with slow turnaround times. For instance, while we wanted to show the user's location on the map, the geolocation API was unreliable within the mobile app's web view. Additionally, the widget had to function within a constrained, nearly square aspect ratio on mobile devices, despite available screen real estate. We had to be clever with our responsive design, ensuring the UI remained usable and uncrowded regardless of the arbitrary container dimensions.

### **Delivering Under Pressure**
Despite its importance to students, the project initially faced resource constraints due to competing business needs. However, the deadline was immovable for me personally. I was set to leave for an internship at Sweetwater Sound and wanted to leave behind a polished, finished product. In less than three months, working only a few hours a week, our small team delivered a robust solution. The pressure to finish before my departure drove me to ensure the code was clean, documented, and ready for the next generation of Digital Corps developers (I hope I did ok!!!).

### **Smoothing the Jitter**  
Our GPS data isn't realtime, it jumps between locations. A bus shouldn't teleport across the map. To solve this, I implemented a custom animation system using `requestAnimationFrame`. This allows the application to interpolate the bus's position between updates, creating smooth, realistic movement rather than abrupt jumps.

## My Role

As the **sole front-end developer**, I owned the implementation from research to code. I spent weeks diving into digital cartography, studying vector tiles, zoom levels, and coordinate systems, to ensure we built something reliable. I worked closely with our UX designers to translate their vision into code and collaborated with the sole backend engineer to ensure our data feed was robust.

## Impact

Reflecting on this now, eight months after leaving the Digital Corps, this project stands out as one of my proudest contributions. It is a daily utility for the community I was a part of, with a large amount of students using it every day. The launch triggered a snowball effect that continued long after I handed off the repository:

1.  **Continued Investment:** The Digital Corps has continued to iterate on the tracker, building robust administration tools and adding new features to improve the student experience.
2.  **New Opportunities:** The success of this in-house solution impressed the university administration, solidifying the Corps' reputation for tackling high-impact, technical challenges.
3.  **Real-World Difference:** Even now, I still hear how the bus tracker helps students get to class on time or avoid a long wait in the rain.

There’s a unique satisfaction in building the tool you wish you had. Knowing that I played a crucial role in restoring this service, and leaving it in a better state than I found it, was the perfect way to start to cap off my time at the university (Yes, I built this as a Sophomore in college, not very many people can claim they have done something like that!).
