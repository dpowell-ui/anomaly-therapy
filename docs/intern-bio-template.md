# Intern bio card template

Reusable card markup for incoming Accessible Care interns.
Preserved from Paige Ring's card before removal (2026-07-15).

## Original card (Paige Ring)

```html
<!-- Team Member 4 — Paige Ring -->
<article class="member reveal" data-delay="3">
  <div class="member__photo">
    <img src="/images/team/team-5a.jpg" alt="Paige Ring, Therapist Intern." loading="lazy" />
  </div>
  <p class="member__credentials">Intern</p>
  <h3 class="member__name">Paige Ring</h3>
  <p class="member__role">On a waitlist</p>
  <p class="member__bio">Paige works under licensed supervision with clients in our <a href="/services.html#accessible-care" class="tlink" style="font-size: inherit; letter-spacing: 0; text-transform: none;">Accessible Care program</a>. She brings a thoughtful, careful presence to the room.</p>
</article>
```

## Reusable template (for next intern)

Swap the four placeholders: photo path, alt text, name, and bio copy.

```html
<!-- Team Member N — {FIRST LAST} -->
<article class="member reveal" data-delay="3">
  <div class="member__photo">
    <img src="/images/team/team-Na.jpg" alt="{FIRST LAST}, Therapist Intern." loading="lazy" />
  </div>
  <p class="member__credentials">Intern</p>
  <h3 class="member__name">{FIRST LAST}</h3>
  <p class="member__role">Therapist Intern</p>
  <p class="member__bio">{FIRST} works under licensed supervision with clients in our <a href="/services.html#accessible-care" class="tlink" style="font-size: inherit; letter-spacing: 0; text-transform: none;">Accessible Care program</a>. {ONE-SENTENCE BIO}.</p>
</article>
```

## Photo processing notes

- New headshot files live in `/images/team/team-Na.jpg` (a/b/c suffix supported for hover cycle if 3 photos available)
- 1000×1250 (4:5) JPEG, ~200KB, EXIF-normalized
- Use `data-photos="3"` on the article and stack three `<img>` tags if hover-cycle is desired
- See earlier commits (search git log for "hover-cycle") for the multi-photo pattern
