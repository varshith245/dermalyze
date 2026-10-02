---
name: Clinical Clarity
colors:
  surface: '#f9f9f8'
  surface-dim: '#dadad9'
  surface-bright: '#f9f9f8'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f3f4f3'
  surface-container: '#eeeeed'
  surface-container-high: '#e8e8e7'
  surface-container-highest: '#e2e2e2'
  on-surface: '#1a1c1c'
  on-surface-variant: '#3e4947'
  inverse-surface: '#2f3130'
  inverse-on-surface: '#f1f1f0'
  outline: '#6e7977'
  outline-variant: '#bdc9c6'
  surface-tint: '#006a63'
  primary: '#005c55'
  on-primary: '#ffffff'
  primary-container: '#0f766e'
  on-primary-container: '#a3faef'
  inverse-primary: '#80d5cb'
  secondary: '#a93349'
  on-secondary: '#ffffff'
  secondary-container: '#fe7488'
  on-secondary-container: '#730425'
  tertiary: '#4c5259'
  on-tertiary: '#ffffff'
  tertiary-container: '#646a71'
  on-tertiary-container: '#e5ebf3'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#9cf2e8'
  primary-fixed-dim: '#80d5cb'
  on-primary-fixed: '#00201d'
  on-primary-fixed-variant: '#00504a'
  secondary-fixed: '#ffdadc'
  secondary-fixed-dim: '#ffb2b9'
  on-secondary-fixed: '#400010'
  on-secondary-fixed-variant: '#891933'
  tertiary-fixed: '#dde3eb'
  tertiary-fixed-dim: '#c1c7cf'
  on-tertiary-fixed: '#161c22'
  on-tertiary-fixed-variant: '#41474e'
  background: '#f9f9f8'
  on-background: '#1a1c1c'
  surface-variant: '#e2e2e2'
typography:
  display-lg:
    fontFamily: Manrope
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Manrope
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Manrope
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
  title-md:
    fontFamily: Manrope
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  body-lg:
    fontFamily: Manrope
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Manrope
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-md:
    fontFamily: Manrope
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 20px
    letterSpacing: 0.01em
  caption:
    fontFamily: Manrope
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 8px
  container-max: 1200px
  gutter: 24px
  margin-mobile: 16px
  margin-desktop: 40px
---

## Brand & Style
The design system is anchored in the concept of "Clinical Clarity"—a balance between rigorous medical professionalism and approachable, human-centric care. The target audience includes individuals seeking immediate, credible dermatological guidance. 

The visual style is **Modern Corporate** with a focus on high-legibility and calming aesthetics. It utilizes a card-based architecture to organize complex medical data into digestible units. To evoke trust, the interface avoids aggressive "tech" tropes like dark mode or neon accents, opting instead for a bright, airy, and grounded "White-Label Clinical" aesthetic. Every interaction should feel intentional, stable, and reassuring.

## Colors
The palette is designed to be sterile but warm.
- **Primary (Clinical Teal):** Used for primary actions, active states, and brand-critical elements. It signals authority and medical reliability.
- **Secondary (Soft Coral):** Reserved strictly for urgent calls to action or subtle health alerts. It is used sparingly to prevent alarm.
- **Neutral (Warm Off-White):** The primary background color. Unlike pure white, this off-white reduces eye strain and feels more natural and "skin-like."
- **Surface (White):** Used for cards and input fields to create a clear layer of separation from the background.
- **Text (Charcoal):** High-contrast gray for maximum legibility without the harshness of pure black.

## Typography
This design system utilizes **Manrope** for its balanced, humanist qualities that feel both systematic and friendly. 
- **Headings:** Use bold weights with slightly tightened letter-spacing to appear confident and established.
- **Body Text:** Uses a generous line-height (1.5x) to ensure medical information is easy to parse, especially during stressful user journeys.
- **Scale:** Maintain a clear hierarchy where titles are significantly larger than body text to facilitate quick scanning of reports.

## Layout & Spacing
The layout follows a **Fluid Grid** model with a soft 8px baseline rhythm.
- **Desktop:** 12-column grid with a maximum container width of 1200px to prevent line lengths from becoming unreadable.
- **Mobile:** Single column with 16px side margins. Cards should span the full width minus margins.
- **Philosophy:** Use generous whitespace between sections (48px+) to create a "breathing" interface. Elements should never feel cramped; density is the enemy of a calm medical experience.

## Elevation & Depth
Depth is created through **Tonal Layers** and **Ambient Shadows**. 
- **Level 0 (Background):** #FAFAF9 (Warm Off-White).
- **Level 1 (Cards):** Pure White (#FFFFFF) with a very soft, diffused shadow: `0px 4px 20px rgba(30, 41, 59, 0.05)`.
- **Level 2 (Hover/Active):** Slightly deeper shadow to indicate interactivity: `0px 8px 30px rgba(30, 41, 59, 0.08)`.
- **Outlines:** Use subtle 1px borders (#E2E8F0) on input fields and secondary buttons instead of heavy shadows to maintain a "clean clinical" look.

## Shapes
The shape language is consistently **Rounded**, avoiding sharp corners to appear approachable and safe.
- **Buttons & Inputs:** 8px (rounded-md) for a professional look.
- **Cards & Modals:** 16px (rounded-xl) to create a distinct, friendly container for content.
- **Avatars/Icons:** Circular containers are preferred for medical icons to soften the "technical" feel of the AI components.

## Components
- **Buttons:** 
    - *Primary:* Solid Clinical Teal with white text. High-contrast, 48px height for accessibility.
    - *Secondary:* Ghost style with Teal border and text.
- **Cards:** White background, 16px radius, soft shadow. Used for medical reports, doctor profiles, and AI insight summaries.
- **Input Fields:** Large tap targets (48px height) with 1px border. Focus state uses a 2px Teal ring.
- **Chips:** Used for selecting symptoms (e.g., "Itchy," "Redness"). Light teal background with dark teal text.
- **AI Feedback:** Use a subtle "sparkle" icon and a light blue-tinted background for messages generated by the AI to distinguish them from human/system messages.
- **Medical Disclaimer:** A persistent, low-contrast footer or thin top-banner in #F1F5F9 (Light Gray) with #64748B text. It must be legible but not visually compete with primary navigation.
- **Progress Steppers:** Used for consultation flows. Thin lines with small circular nodes to indicate "Step 1 of 4."