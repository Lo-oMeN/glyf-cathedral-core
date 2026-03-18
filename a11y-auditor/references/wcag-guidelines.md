# WCAG 2.1 Guidelines Reference

## Overview

Web Content Accessibility Guidelines (WCAG) 2.1 defines how to make web content more accessible to people with disabilities. The guidelines are organized around four principles (POUR):

- **Perceivable**: Information must be presentable in ways users can perceive
- **Operable**: Interface components must be operable by all users
- **Understandable**: Information and operation must be understandable
- **Robust**: Content must work with current and future assistive technologies

## Compliance Levels

### Level A (Minimum)
Basic accessibility requirements. Must be met to allow assistive technologies to function.

**Key Requirements:**
- Text alternatives for images (`alt` attributes)
- Keyboard accessibility for all functionality
- Captions/transcripts for prerecorded audio/video
- Color not used as the only visual means of conveying information
- Form labels and instructions

### Level AA (Standard)
Industry standard for accessibility compliance. Required by most regulations.

**Key Additional Requirements:**
- Color contrast ratio of at least 4.5:1 for normal text
- Resizable text up to 200% without assistive technology
- Consistent navigation and identification
- Error prevention for important submissions
- Status messages announced to screen readers

### Level AAA (Enhanced)
Highest level of accessibility. Not required as a general policy but ideal for critical services.

**Key Additional Requirements:**
- Color contrast ratio of at least 7:1 for normal text
- Sign language interpretation for prerecorded media
- Extended audio description for video
- Reading level at lower secondary education level
- All functionality operable without time limits

## Common Accessibility Issues

### Images
- **Missing alt text**: All images need alternative text descriptions
- **Decorative images**: Use `alt=""` for purely decorative images
- **Complex images**: Provide detailed descriptions or link to them

### Forms
- **Missing labels**: Every input needs an associated label
- **Error identification**: Errors must be clearly identified and described
- **Error suggestions**: Provide suggestions for correction when known

### Navigation
- **Skip links**: Provide mechanism to skip repetitive content
- **Focus order**: Logical and predictable tab order
- **Page titles**: Descriptive and unique for each page

### Color and Contrast
- **Minimum contrast**: 4.5:1 for normal text (AA), 7:1 for AAA
- **Large text contrast**: 3:1 for 18pt+ or 14pt+ bold
- **Color independence**: Never rely on color alone

### Keyboard Access
- **All functionality**: Must be operable via keyboard
- **Focus indicators**: Visible focus states on all interactive elements
- **No keyboard traps**: Users must be able to tab away from all elements

## Testing Tools

### Automated Testing (via axe-core)
1. **Color contrast**: Automated detection of contrast issues
2. **Missing labels**: Detection of form inputs without labels
3. **Image alt**: Verification of alt text presence
4. **Heading structure**: Validation of heading hierarchy
5. **ARIA usage**: Checking for proper ARIA implementation

### Manual Testing Required
1. **Keyboard navigation**: Full site operation using only keyboard
2. **Screen reader testing**: Verification with NVDA, JAWS, or VoiceOver
3. **Zoom testing**: Functionality at 200% and 400% zoom
4. **Color blindness**: Visual checks for color-dependent information

## ARIA Roles and Properties

### Landmark Roles
- `role="banner"` - Site header
- `role="navigation"` - Navigation sections
- `role="main"` - Main content
- `role="complementary"` - Supporting content (sidebars)
- `role="contentinfo"` - Footer/copyright
- `role="search"` - Search functionality

### Widget Roles
- `role="button"` - Clickable action
- `role="link"` - Navigation link
- `role="tab"` - Tab in a tablist
- `role="dialog"` - Modal dialog
- `role="alert"` - Important message
- `role="status"` - Status update

### Key Properties
- `aria-label` - Accessible name when not visible
- `aria-labelledby` - References element providing label
- `aria-describedby` - References element providing description
- `aria-expanded` - State of expandable content
- `aria-hidden` - Hides element from accessibility tree
- `aria-live` - Announces dynamic content changes

## References

- [WCAG 2.1 Specification](https://www.w3.org/TR/WCAG21/)
- [WCAG Quick Reference](https://www.w3.org/WAI/WCAG21/quickref/)
- [axe-core Rules](https://dequeuniversity.com/rules/axe/4.8)
- [WebAIM WCAG Checklist](https://webaim.org/standards/wcag/checklist)
