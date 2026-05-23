# Anomaly Therapy — Website

**Volume 02 brand rebuild · Static site · No build step required**

A custom static site replacing the Squarespace deployment of anomalytherapy.com.
Built to match the Volume 02 brand kit and the physical aesthetic of the
Patterson Street office.

---

## File structure

```
anomaly-therapy/
├── index.html              Welcome (home)
├── services.html           Three buckets: traditional, accessible, workplace
├── about.html              Who we are + team grid + office
├── contact.html            Request appointment + send a note
├── faqs.html               9 FAQs (footer link)
├── media.html              Press + podcasts (footer link)
├── careers.html            Internship / associate / licensed roles (footer link)
├── 404.html                Branded not-found
├── netlify.toml            Deploy config: caching, redirects, headers
├── css/
│   └── style.css           Full design system (~700 lines, tokens + components)
├── js/
│   └── main.js             Mobile menu, popup, floating CTA, reveals
└── images/
    ├── team/               Headshots + group photo
    ├── interior/           Office rooms + hallway
    └── lifestyle/          Detail shots
```

---

## Deploying to Netlify

### Option 1 — Drag & drop (fastest)

1. Sign in at [app.netlify.com](https://app.netlify.com).
2. Click **Add new site → Deploy manually**.
3. Drag the entire `anomaly-therapy` folder onto the drop zone.
4. Netlify will give you a temporary `*.netlify.app` URL within ~30 seconds.
5. **Domain settings → Add custom domain → `anomalytherapy.com`** and follow
   the DNS instructions. (You'll need to point your registrar's nameservers
   or A/CNAME records at Netlify.)

### Option 2 — Git-based deploys (recommended for ongoing edits)

1. Initialize a git repo and push to GitHub:
   ```bash
   cd anomaly-therapy
   git init
   git add .
   git commit -m "Initial commit — Volume 02"
   git branch -M main
   git remote add origin https://github.com/YOUR-USER/anomaly-therapy.git
   git push -u origin main
   ```
2. In Netlify: **Add new site → Import an existing project → GitHub**, pick the
   repo, accept defaults (Netlify reads `netlify.toml`), and deploy.
3. Every `git push` now triggers a redeploy.

This is the path that pairs best with Claude Code — Jess can ask Claude to
make a change, review the diff, commit, and the site updates automatically.

---

## Editing with Claude Code

From the repo directory, run `claude` in your terminal and ask in plain English:

- *"Update the second team bio in `about.html` — change Cayce Smith's name to X."*
- *"In `services.html`, change the standard session fee from $175–$250 to $200–$275."*
- *"Add a new FAQ to `faqs.html` about evening appointments."*
- *"Swap `team-3.jpg` for a new photo — I'll put it in `images/team/`."*

Claude reads the existing files, follows the patterns, and edits in place. The
design system is in CSS variables (`css/style.css`, top of file) so global
color/spacing changes are one-line edits.

---

## ⚠️ Things to verify before launch

### 1. Team photo → name mapping (please verify the inferred ones)

Team photo assignments (corrected per Jess's feedback May 23):

| Slot | File | Person | Confidence |
|------|------|--------|------------|
| 1 | `images/team/team-1.jpg` | Jess Mansell, LPC-MHSP (Founder) | ✓ confirmed by Jess |
| 2 | `images/team/team-2.jpg` | Ashley Wellander | inferred by elimination |
| 3 | `images/team/team-3.jpg` | Cayce Smith | ✓ confirmed by Jess |
| 4 | `images/team/team-4.jpg` | Jillee Walter | assumed unchanged |
| 5 | *(monogram placeholder)* | Paige Ring | photo not provided |

**Please confirm slots 2 and 4 explicitly.** Photo 2 is the woman in the dark blazer with gold chain necklace; photo 4 is the older woman in the beige/light blazer. If either is wrong, swap the file names in `images/team/` — the HTML references slot numbers, not names.

To replace Paige's monogram placeholder with a real photo, drop the file in `images/team/team-5.jpg` and ask Claude Code to swap the monogram block in `about.html` for an image block matching the others.

### 2. Fonts (Recoleta substitution)

The brand kit specifies **Recoleta** for display type. Recoleta is an Adobe
Fonts–only family and requires a paid Adobe Fonts kit ID to embed on the
live site.

The current build uses **Fraunces** (Google Fonts, free) as a near-visual
stand-in — same warm-modernist serif feel. Fraunces stays in the fallback
stack even after Recoleta is enabled, so the swap is purely additive.

**To switch to Recoleta when you have an Adobe Fonts kit:**

1. In Adobe Fonts, create a Web Project with Recoleta selected.
2. Adobe gives you a kit URL like `https://use.typekit.net/abc1234.css`.
3. In every HTML file, find this line near the top:
   ```html
   <link href="https://fonts.googleapis.com/css2?family=Fraunces..." rel="stylesheet" />
   ```
   Add (do not replace) the Adobe line right after it:
   ```html
   <link rel="stylesheet" href="https://use.typekit.net/YOUR-KIT.css" />
   ```
4. In `css/style.css`, find this line near the top:
   ```css
   --serif: 'Fraunces', 'Recoleta', Georgia, ...;
   ```
   Swap the order:
   ```css
   --serif: 'Recoleta', 'Fraunces', Georgia, ...;
   ```

Or just ask Claude Code: *"Swap Fraunces for Recoleta. My Adobe Fonts kit
URL is X."*

### 3. EHR link

Every "Book a Consult" and "Request Appointment" button points to:
**`https://anomalytherapy.sessionshealth.com`**

If your EHR URL changes, do a project-wide find/replace on that string.

### 4. Phone number, email, address

Currently uses `hello@anomalytherapy.com`, `(615) 988-1158`, and
`1916 Patterson Street, Suite 202`. These appear in `contact.html`, the
footer of every page, and a few mailto links on `careers.html` /
`media.html`. Update via find/replace if anything changes.

---

## Design notes (what we built and why)

- **Typographic hero on Welcome** — no big photo, per your direction. The
  Fraunces serif at scale carries the room.
- **Three-bucket grid** is the primary visual hierarchy on Welcome and
  Services. Traditional · Accessible · Workplace, each with its own price
  signal and CTA.
- **Marquee ticker** runs across the top of every page with the five
  brand-kit signature phrases. Slow (~56s loop), pauses on hover, respects
  `prefers-reduced-motion`.
- **Floating "Book a Consult"** appears bottom-right after the user scrolls
  ~480px. Hidden on `contact.html` since that page *is* the CTA.
- **Accessible Care popup** slides up from bottom-left after 9 seconds OR
  when the user has scrolled 40% of the page (whichever comes first).
  Dismissal stored in `localStorage` for 7 days so it doesn't nag returning
  visitors. Hidden on `contact.html` and `404.html`.
- **Footer** uses the four-column pattern with Mission / Practice / More /
  Studio. The mission statement is the lead — modeled on the Wealthy
  Practitioner footer you flagged. FAQs, Media, and Careers live only in
  the "More" column, per your discard list.
- **Page-numbered editorial chrome** (e.g. *"01 — Welcome / Nashville ·
  Tennessee"*) at the top of every section, mimicking the page-number
  motif in the brand kit PDF.
- **All animations respect `prefers-reduced-motion`** — marquee, reveals,
  and the popup slide-up all stop for users with motion sensitivity.

---

## Suggested next iterations

When you're ready for v1.1:

1. **Individual team member bio pages.** Link each team card on
   `about.html` to a dedicated `/team/jess-mansell.html` etc. Keep the
   editorial typography; add a longer bio + specialties + a personal
   "what I work best with" section.
2. **Video integration.** A single short video (60–90s) on Welcome or
   About — Jess speaking directly to camera about who Anomaly is for.
   Embed as a self-hosted MP4 or via Mux/Vimeo Pro to avoid YouTube's
   visual baggage.
3. **Editorial journal / Reflections.** A `/reflections/` directory of
   short essays (like the "No. 14" social card in the brand kit). 4–8
   pieces a year. SEO + brand depth.
4. **Real EHR-embedded scheduling** instead of the outbound link, if
   SessionsHealth supports a widget.
5. **Workplace Wellness one-pager** as a separate PDF download — a
   leave-behind for HR / People teams. Could live at `/workplace.pdf`.

---

## Tech stack

Pure static HTML + CSS + vanilla JS. No build step, no framework, no
dependencies. Google Fonts (Fraunces + Inter) loaded via `<link>`.

The whole site is well under 1 MB without images, and loads to interactive
in under a second on a typical connection.

---

## License & ownership

All site code, copy, and design produced for and owned by Anomaly Therapy.
Brand kit and photography are owned by the practice.

— Built with Claude · Volume 02 · Revision MMXXVI
