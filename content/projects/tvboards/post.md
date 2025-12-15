---
title: "Digital Corps Office TV Boards"
date: 2024-03-05
draft: true
---
# Digital Corps Office TV Boards

![tv board](/portfolio/tvboards/thumbnail.jpg)

At my previous role at the Digital Corps, two large TV screens served as the daily pulse of the team, displaying announcements, weather, and photos of our pets. But this system, built years ago, was starting to show its age. It was unreliable, and with the original developers long since graduated, it had become a bit of a mystery. My curiosity got the best of me, and I decided to take it on as a personal project to see if I could breathe new life into it.

My investigation started with the software. I began by migrating the underlying computers from Windows to Kubuntu for better stability and performance. Then, I dove into the codebase, modernizing the original JavaScript React app to use Vite and TypeScript. This wasn't just a simple conversion; it was an archeological dig through old code, fixing type inconsistencies and restructuring logic to be more robust. I also implemented better error handling, so a lost internet connection or a failing slide would no longer crash the entire display.

But even with a modernized and more stable codebase, the performance was still sluggish. Animations were choppy, and the display would occasionally glitch. This pushed me to look beyond the code and investigate the hardware itself. The aging computers were running at a scorching 100°C, with one machine's fan having failed completely. The "burn-in" I thought I was seeing on the TVs was actually the result of the onboard graphics overheating and creating visual artifacts. The hardware was the true bottleneck.

This discovery turned my software project into a full-stack hardware and software overhaul. I researched and sourced new computers, set them up, and installed them behind the TVs. The difference was immediate. With capable hardware, the displays could finally run smoothly at 4K resolution and a 60Hz refresh rate, making the entire system feel responsive and new.

This project was a powerful lesson in looking at the bigger picture. It taught me to diagnose problems from the application layer all the way down to the physical hardware. The experience also sparked ideas for future improvements, like transitioning to a native application using Tauri or Electron. What started as simple curiosity became a comprehensive project that reinforced my love for diving deep, solving complex problems, and making a tangible impact on the environment around me.