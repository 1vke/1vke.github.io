---
title: "Digital Corps Office TV Boards"
date: 2025-12-05
draft: false
---

{{< figure src="/projects/tvboards/thumbnail.jpg" alt="Digital Corps Office TV Board displaying team photos and announcements" caption="One of the digital signage displays at the Digital Corps, serving as the daily pulse of the office." >}}

At my previous role at the Digital Corps, two large TV screens served as the daily pulse of the team, displaying announcements, weather, and photos of our pets, as well as other things. But this system, built years ago, was starting to show its age. It was unreliable, and with the original developers long since graduated, it had become a bit of a mystery. My curiosity got the best of me, and I decided to take it on as a personal project to see if I could breathe new life into it.

## The Tech Stack

After some investigation, I found out that I needed to modernize the stack to ensure stability and maintainability for future cohorts.

*   **React + Vite + TypeScript:** I migrated the legacy JavaScript React codebase to a modern Vite and TypeScript setup. This involved fixing type inconsistencies and restructuring logic to be more robust.
*   **Kubuntu Linux:** I replaced the unstable Windows environment on the underlying mini-PCs with Kubuntu, providing a lightweight and reliable OS for the display kiosks.
*   **Hardware Overhaul:** I identified that the software issues were compounded by thermal throttling and failing hardware, leading to a complete replacement of the compute units.

## Engineering Challenges

### **Moving from a JavaScript Create-React-App React app, to a Vite Typescript React app**
Phew, that title is a mouthful. Anyways, this was not very simple and it took a good amount of time. I basicaly said YOLO and put most of the code into a new TypeScript Vite React project. I chipped away at the project until I got something to compile, then I started to fix bugs that became aparent with the code now being in TypeScript. This went great as there weren't really any hiccups in the process! It is so fascinating how many things start to become issues when you migrate to TypeScript from JavaScript. There were a ton of type inconsistencies in the original application that TypeScript was not having at all.

### **Solving reliability issues**
Porting the project over to another framework meant that I really was in deep into the project. This left me with some time and the knowledge to solve some of the issues that were plaguing the kiosk. 

For one, when the kiosk would lose connection, the entire kiosk website would go down and never come back up. Sure, a simple refresh of the website will do, but these are TVs and computers mounted on the wall. What that really means is in order to fix it, a restart of the computer is required, because noone wants to stand in front of a TV with a keyboard and mouse. I found out that someone had written the web app in a way that if there was any exception at all, the entire thing would crash. This is funny because we are constantly hitting a variety of APIs, so any fault there would cause the web app to crash. I ended up fixing this and added better error handling to prevent internet outages or unrecoverable errors from breaking the web app.

For two, there was a ton of timing issues, so sometimes slides were skipped, including important slides! This was a bug with the slide timing system. After investigating, it seemed as if someone wrote some logic that clearly misunderstood the timing implementation, causing all sorts of issues. I fixed that logic, then rewrote some of the timing logic. Now it works great!

### **Diagnosing the Hardware Bottleneck**
Even with a modernized and more stable codebase, the performance was still sluggish. Animations were choppy, and the display would occasionally glitch. The output from the computers made the TV look like they had a super warm picture! I fiddled with a ton of TV settings before I gave up on the color. This pushed me to look beyond the code and investigate the hardware itself. I discovered the aging computers were running at a scorching 100°C, with one machine's fan having failed completely. The "burn-in" I thought I was seeing on the TVs was actually the result of the onboard graphics overheating and creating visual artifacts. The hardware was the true bottleneck.

The discovery of the computers failing turned my software project into a full-stack hardware and software overhaul. I researched and sourced new computers, set them up, and installed them behind the TVs. The difference was immediate. With newer and more capable hardware, the displays could finally run smoothly at 4K resolution and a 60Hz refresh rate, making the entire system feel responsive and new. We were originally running the website at 50% scale with the resolution being 1080p because of all the issues, now we could run the website at it's actual scale!

## My Role

I took this on as a personal initiative, driven by curiosity and a desire to improve our office environment. I acted as the sole developer and systems administrator, handling everything from the software migration (React/TypeScript) to the OS installation (Linux) and the physical hardware procurement and installation.

## Impact

This project was a powerful lesson in looking at the bigger picture. It taught me to diagnose problems from the application layer all the way down to the physical hardware. The experience also sparked ideas for future improvements, like transitioning to a native application using Tauri or Electron (although, that is probably not the ideal stack for a mostly web-technology based team). What started as simple curiosity became a comprehensive project that reinforced my love for diving deep, solving complex problems, and making a tangible impact on the environment around me.
