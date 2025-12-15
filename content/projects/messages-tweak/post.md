---
title: "iOS Messages Jailbreak Tweak"
date: 2025-03-02
draft: true
---
# iOS Messages Jailbreak Tweak

![ios messages tweak](/portfolio/messages-tweak/thumbnail.jpg)

I developed an iOS jailbreak tweak that allows users to modify the colors of message balloons in the iOS Messages app. 
This tweak was built using Theos, a cross-platform build system for jailbreak software development, and was written in 
Objective-C.

Using existing jailbreak software as a foundation, I reverse-engineered the Messages app to understand how to inject my 
own modifications. I had always wanted a way to customize message balloon colors, so I set out to create a solution 
myself.

To accomplish this, I utilized various reverse engineering tools. Flex helped me inspect the app’s view hierarchy to 
understand how the message balloons were rendered, while the LLDB debugger allowed me to set breakpoints and analyze 
where I needed to inject my custom color modifications.

I also built a preferences package, enabling users to customize the message balloon colors directly from the iOS 
Settings app. This project gave me valuable insight into how iOS applications and services are developed at a low level.
Additionally, it provided a deeper understanding of how a compromised system—such as a jailbroken iOS device—can be 
modified to achieve functionality beyond its stock capabilities.