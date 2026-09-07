# Nuno Mikael Nugroho's Portofolio Website

## Overview
A static personal portfolio website built for "Individual Assignment 1" Pemrograman Berbasis Platform, showcasing my background, skills, and projects as a Computer Science student at Universitas Indonesia.

## Features
- **Responsive layout**
    adapts from desktop to mobile using CSS Grid and media queries
- **Sticky navigation header**
    with smooth scroll to page sections
- **Projects section**
    text/image layout alternates per project for visual rhythm
- **Lightbox image viewer**
    click any project image to view it full-size, built with pure CSS (`:target` selector, no JavaScript)
- **Skills section**
    with icon-labeled pills, grouped visually by category
- **Custom CSS background for header, body, and footer**
    image / texture backgrounds for header and footer, gradient coloring background for body

## Tech Stack
- **HTML5**
    semantic elements (`<header>`, `<nav>`, `<main>`, `<section>`, `<footer>`)
- **CSS3** 
    Grid layout, custom properties (CSS variables), media queries, `:target` for interactivity
- **Google Fonts**
    Space Grotesk

No JavaScript was used in this project. All interactivity were achieved through pure HTML / CSS techniques.

## Reflection
1.  Yes, I used semantic HTML5 elements, specifically `<header>`, `<nav>`, `<main>`, `<section>`, and `<footer>`. I
    used`<section>` three times to group content thematically (profile, skills, and projects) each with an `id` used as an anchor target for navigation.

    `<article>` was not used, since none of the content is meant to be independently distributable outside the page. Each section is a dependent part of a single cohesive page rather than standalone syndicated content.
    `<aside>` was also not used, as all content presented (profile info, skills, and projects) is primary and directly relevant to the portfolio's purpose. There was no supplementary content I wanted to add to warrant using `<aside>`

2. The main challenge in building a responsive layout was reworking elements that are arranged side-by-side on desktop into a
    stacked layout on mobile, without breaking the logical reading order. For example, the hero photo is positioned beside the identity / details text on desktop via `grid-template-areas` but needed a deliberate reordering on mobile so it sits between the identity and details sections rather than in a confusing position. A similar challenge appeared in the projects section, where the desktop layout alternates text-left / image-right and image-left / text-right per project; this alternation doesn't translate meaningfully to a single-column mobile layout, so all project rows were unified into one consistent stacking order on mobile. Element sizing for certain images was also adjusted for smaller viewports.
    
    The general evaluation principle used was elements arranged horizontally on desktop were converted to vertical stacking on mobile, since horizontal space becomes too narrow to preserve readability. I tested it using the browser DevTools' Device Toolbar to verify layout behavior across breakpoints.

3. As a purely static site, a few limitations became apparent to me while trying to present content optimally:
    - Image lightbox
        Implemented using the CSS `:target` selector, which works but has real limitations, such as not being able to be closed by clicking outside the image or pressing escape.
    - No project filtering
        Project tags (Film, Hardware, Research, etc.) are currently static labels with no interactive behavior, so visitors can't filter or sort projects by category despite the growing variety.
    - Manual project markup
        Each new project requires manually copying and pasting an entire `project-row` HTML block, making the codebase repetitive and harder to maintain as more projects are added.

    Plans I have for dynamic functionality in the next iteration:
    - A proper JavaScript-based modal (closable via outside click or escape key) to replace the CSS-only lightbox
    - Interactive tag-based filtering for the projects section
    - A data-driven rendering approach for the projects section

## AI Disclosure
I used AI for mainly two things, which was brainstorming and bug fixes. Whenever I was confused on what else to add to make the site more interesting, I asked AI chatbots such as Google's Gemini and Claude for ideas. One example was on the skills section when at first I wanted to make a basic list but thought that would be visually unappealing. I asked Gemini for some ideas and the idea I went with was creating small interactive pills.
Here was the prompt used:
"okay so i want to add skills section next. i want to put it above projects but i dont really have an idea on how to make the layout interesting"
Other than brainstorming, I used AI whenever I got stuck on a bug, to tidy up my messy code, and to add comments to make the code more readable. While I used AI, I always check the code twice and not just copy paste it to add my own adjusments and tweaks. This is because AI, mostly, don't understand how to make things look visually inetersting for us humans. So, I use the codes I got from AI as a template that I will alter myself, usually stuff like colors, size, and brightness. Because this assignment is making a website, AI can't directly see what the final product looks like, so they might not understand that some of the codes they make create an awkward or messy look to the site. An example was when I was creating the projects section, I used an AI generated template and the photo was way too big and not aligned with the box, which was also too big. The AI didn't know why, so I fixed it myself by creating boundaries for both not only for laptop layout, but also for mobile layout.

## Author
**Nuno Mikael Nugroho**
NPM: 2506624865
Class: PBP D
S1 Ilmu Komputer, Fakultas Ilmu Komputer, Universitas Indonesia

## License
This project is created for academic purposes as part of coursework at Universitas Indonesia.