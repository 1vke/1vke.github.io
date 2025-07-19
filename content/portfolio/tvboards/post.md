---
title: "Digital Corps Office TV Boards"
date: 2025-03-05
draft: false
---
![tv board](/portfolio/tvboards/thumbnail.jpg)

At my current job, there are two vertically mounted TVs in the office that display a website with daily announcements,
weather updates, countdowns, and specific Slack channel slides, such as one dedicated to sharing pictures of pets. This 
system was originally developed in 2018, but by the time I started working on it in 2024, none of the original developers
were still with the company, as they had graduated. Over time, as I was working, I became more and more curious on how 
they worked and why they would not function correctly sometimes. I eventually just made it my own side project to make 
them better.

One of my first tasks I set off to do was to migrate the operating system of the display computers from Windows to 
Kubuntu. This change provided greater stability, better performance, and improved system management.

Next, I focused on modernizing the codebase by converting it from JavaScript to TypeScript. The original website was 
built using Create-React-App, which I transitioned to a Vite-based TypeScript React app. This migration improved 
performance and helped resolve numerous type inconsistencies and code inconsistencies. Some issues were straightforward 
to fix, while others required deeper logical restructuring.

To improve application stability, I introduced better error handling. Previously, internet connection failures would 
cause the entire website to crash or stall, but I implemented a full-screen error message to notify users of connectivity
issues without breaking the system. Additionally, individual slide failures no longer caused the entire website to 
crash—now, errors are isolated within their respective slides.

I also worked on making the styles more responsive to different screen resolutions. The older TV boards originally ran 
at 4K resolution with a 30Hz refresh rate, which resulted in sluggish animations and performance issues. To address this,
I switched the resolution to 1080p at a 60Hz refresh rate, significantly improving animation fluidity and overall 
responsiveness. However, the styles were originally designed with static dimensions for 4K resolution, meaning they didn’t
scale well across different screen sizes. This issue eventually became less relevant as the aging computers started to 
fail—both of them were consistently running at 100°C. One machine even had its fan fail entirely, leading to extreme lag
due to thermal throttling and rendering issues.

Realizing that the hardware needed an upgrade, I assessed the old computers, identified the necessary functionality, and
researched the market for suitable replacements. After selecting and purchasing new computers, I set them up and installed
them behind the televisions. These upgrades resolved many of the lingering display issues. Previously, the TV outputs 
appeared to suffer from burn-in, but the actual problem was overheating onboard graphics, which caused visual artifacts 
and degraded performance. With the new machines, 4K resolution could now run smoothly at a 60Hz refresh rate, significantly
improving the display quality.

After modernizing the codebase, improving error handling, and reassessing the system architecture, it became clear that a
native application might be a better fit than a web-based solution. Since the display system is only used on two identical
computers and isn’t meant to be accessed elsewhere, a native app—possibly built with Tauri or Electron—would eliminate the
need for web hosting. However, this transition would introduce new challenges, particularly regarding updates. The current
web application benefits from the CI/CD pipelines we have set up, making it easy to push updates and see changes within 
minutes. A native application, on the other hand, would require a built-in update mechanism to ensure that new versions 
could be deployed efficiently. While I haven’t fully researched this yet, it’s an interesting consideration for the future
of the project.