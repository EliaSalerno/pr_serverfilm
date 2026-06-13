---
name: Cinematic Immersive System
colors:
  surface: '#0c1324'
  surface-dim: '#0c1324'
  surface-bright: '#33394c'
  surface-container-lowest: '#070d1f'
  surface-container-low: '#151b2d'
  surface-container: '#191f31'
  surface-container-high: '#23293c'
  surface-container-highest: '#2e3447'
  on-surface: '#dce1fb'
  on-surface-variant: '#c6c5d5'
  inverse-surface: '#dce1fb'
  inverse-on-surface: '#2a3043'
  outline: '#908f9f'
  outline-variant: '#454653'
  surface-tint: '#bfc2ff'
  primary: '#bfc2ff'
  on-primary: '#141994'
  primary-container: '#00008b'
  on-primary-container: '#7981f5'
  inverse-primary: '#4951c3'
  secondary: '#ffffff'
  on-secondary: '#003737'
  secondary-container: '#00fbfb'
  on-secondary-container: '#007070'
  tertiary: '#b7c8e1'
  on-tertiary: '#213145'
  tertiary-container: '#16263a'
  on-tertiary-container: '#7d8da5'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#e0e0ff'
  primary-fixed-dim: '#bfc2ff'
  on-primary-fixed: '#00006e'
  on-primary-fixed-variant: '#3037aa'
  secondary-fixed: '#00fbfb'
  secondary-fixed-dim: '#00dddd'
  on-secondary-fixed: '#002020'
  on-secondary-fixed-variant: '#004f4f'
  tertiary-fixed: '#d3e4fe'
  tertiary-fixed-dim: '#b7c8e1'
  on-tertiary-fixed: '#0b1c30'
  on-tertiary-fixed-variant: '#38485d'
  background: '#0c1324'
  on-background: '#dce1fb'
  surface-variant: '#2e3447'
typography:
  display-lg:
    fontFamily: Sora
    fontSize: 64px
    fontWeight: '800'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  display-md:
    fontFamily: Sora
    fontSize: 48px
    fontWeight: '700'
    lineHeight: '1.2'
    letterSpacing: -0.01em
  headline-lg:
    fontFamily: Sora
    fontSize: 32px
    fontWeight: '700'
    lineHeight: '1.3'
  headline-lg-mobile:
    fontFamily: Sora
    fontSize: 24px
    fontWeight: '700'
    lineHeight: '1.3'
  headline-md:
    fontFamily: Sora
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.4'
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.6'
  label-md:
    fontFamily: Geist
    fontSize: 14px
    fontWeight: '500'
    lineHeight: '1'
    letterSpacing: 0.05em
  label-sm:
    fontFamily: Geist
    fontSize: 12px
    fontWeight: '600'
    lineHeight: '1'
    letterSpacing: 0.08em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 8px
  container-max: 1440px
  gutter: 24px
  margin-desktop: 64px
  margin-tablet: 32px
  margin-mobile: 16px
---

## Brand & Style

The design system is built to provide a high-end, theatrical experience that recedes into the background, allowing the content to remain the protagonist. The brand personality is **premium, immersive, and sleek**, evoking the feeling of a modern private cinema.

The visual style employs a blend of **Minimalism** and **Glassmorphism**. By using deep, expansive dark surfaces and subtle translucent layers, the UI creates a sense of infinite depth. High-contrast accents are used sparingly to guide the eye without breaking the immersion. Every transition should feel fluid and cinematic, prioritizing motion that mimics the movement of light.

**Target Audience:** Cinephiles, casual viewers, and tech-savvy users who appreciate a polished, distraction-free viewing environment.

## Colors

The palette is anchored in a **Dark Mode** default to reduce eye strain and maximize the vibrance of movie posters and video content.

- **Primary (Deep Navy):** Used for deep background gradients and core branding elements. It provides more character than pure black while maintaining high contrast.
- **Secondary (Vibrant Cyan):** The "Action Color." Reserved for calls to action, active states, progress bars, and critical highlights.
- **Neutral (Slate Grays):** A scale of slate grays is used for surfaces, borders, and secondary text to create hierarchical separation without the harshness of pure white or grey.
- **Background:** The foundation is a rich `#020617` (Deepest Navy/Slate) to ensure the deepest blacks in the video content feel integrated into the interface.

## Typography

This design system utilizes a three-font strategy to balance cinematic impact with technical clarity:

1.  **Sora (Headlines):** A geometric sans-serif with a futuristic edge. It is used for large titles and category headers to provide a "blockbuster" feel.
2.  **Inter (Body):** A highly legible workhorse used for synopses, reviews, and general settings. It ensures readability over long periods.
3.  **Geist (Labels/Metadata):** A mono-spaced influenced sans-serif used for durations, release years, and technical specs (4K, HDR, etc.). Its precision reinforces the "high-end tech" aspect of the platform.

**Scale Strategy:**
- Use `Display LG` exclusively for Hero Banners on Desktop.
- Headlines use tight tracking (letter-spacing) to appear more authoritative and modern.
- Labels use increased tracking for better legibility at small sizes against dark backgrounds.

## Layout & Spacing

The layout follows a **Fluid Grid** model with generous margins to create an expansive, premium feel. 

- **Desktop (12 Columns):** 64px outer margins, 24px gutters. Content is centered with a max-width of 1440px to prevent excessive scanning on ultra-wide monitors.
- **Tablet (8 Columns):** 32px outer margins, 16px gutters.
- **Mobile (4 Columns):** 16px outer margins, 12px gutters.

**Rhythm:**
A strict 8px base grid is used for all internal component spacing. Elements like movie cards and text blocks should follow increments of 8px (e.g., 16, 24, 32, 48, 64) to maintain a cohesive visual cadence.

## Elevation & Depth

In this dark-themed environment, depth is communicated through **Tonal Layering** and **Backdrop Blurs** rather than traditional heavy shadows.

- **Level 0 (Base):** Deep Navy/Black background (#020617).
- **Level 1 (Surfaces):** Slate Gray (#0F172A) surfaces with a subtle 1px border (#1E293B) to define edges.
- **Level 2 (Overlays/Modals):** Glassmorphic panels with `backdrop-filter: blur(20px)` and 60% opacity. This keeps the user connected to the background content even when a menu or detail view is open.
- **Interactive Depth:** When a movie card is focused or hovered, it should scale slightly (1.05x) and gain a soft, Cyan-tinted outer glow to simulate light emitting from the screen.

## Shapes

The design system utilizes **Rounded (Level 2)** shapes to strike a balance between friendly accessibility and modern precision.

- **Movie Cards:** 1rem (16px) corner radius to soften the edges of the high-energy posters.
- **Buttons & Inputs:** 0.5rem (8px) corner radius.
- **Badges/Chips (e.g., "HD", "New"):** Pill-shaped (fully rounded) to differentiate them from functional UI buttons.
- **Selection States:** Active selections in navigation or sliders should use a subtle rounded indicator rather than sharp underlines.

## Components

### Hero Banner
- **Visuals:** Full-bleed background imagery with a "Vignette Gradient" (Deep Navy to Transparent) to ensure text legibility on the left or bottom.
- **Content:** Headline (Display LG), metadata (Label MD), and primary CTA (Cyan filled button).

### Movie Cards
- **Aspect Ratio:** 2:3 for posters or 16:9 for "continue watching" thumbnails.
- **Interaction:** On hover, display a "Quick Play" icon and a subtle progress bar if the title is in progress. 
- **Details:** Titles should be truncated at one line below the card, using Label MD for secondary info (Year, Rating).

### Category Sliders
- **Navigation:** Arrow buttons should be "Ghost" style (border only) and only appear when the mouse is over the row. 
- **Overflow:** Cards should bleed off the edge of the screen to indicate further content, inviting horizontal scrolling.

### Buttons
- **Primary:** Solid Cyan (#00FFFF) with black text for maximum contrast.
- **Secondary:** Transparent with a 1px Slate border and white text.
- **Icon Buttons:** Circular with a Glassmorphic background for playback controls (Play, Pause, Shuffle).

### Input Fields
- **Search:** Darker than the background with a 1px Slate border. On focus, the border transitions to Cyan with a subtle outer glow.