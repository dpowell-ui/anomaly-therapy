/* ============================================================
   /know-someone — message tabs, "Copy message" and "Copy link"
   ============================================================ */

(() => {
  const LINK = 'anomalytherapy.com/know-someone';
  const MSGS = {
    friend: "Hey, I've been thinking about you. You've had a lot on your plate, and I have watched as you hold everything together. I came across Anomaly Therapy, a private mental health practice in Nashville that works with people who are doing well on paper and still carrying a lot. They offer a free 15-minute consult to get started. No pressure at all. I just wanted you to have it: " + LINK,
    partner: "I love you, and I've noticed how much we've both been carrying lately. I found a practice in Nashville, Anomaly Therapy, that works with couples and individuals. They offer a free 15-minute consult. Would you be open to looking at it with me? Here's the page: " + LINK,
    colleague: "Not work-related, just from me. I know how much you take on, and I wanted to pass along something that's been helpful to people I know. Anomaly Therapy in Nashville works with high-performing professionals, privately, in person or virtual across Tennessee. They offer a free 15-minute consult: " + LINK,
  };
  const DEFAULT_STATUS = 'Nothing is sent from this page. Paste it into a text or email.';

  const msg = document.getElementById('ks-msg');
  const status = document.getElementById('ks-copy-status');
  const copyBtn = document.getElementById('ks-copy-btn');
  const shareBtn = document.getElementById('ks-share-btn');
  const shareStatus = document.getElementById('ks-share-status');
  const tabs = Array.from(document.querySelectorAll('.ks-tab'));
  if (!msg || !copyBtn) return;

  let current = 'friend';

  const show = (key) => {
    current = key;
    msg.textContent = MSGS[key];
    tabs.forEach((t) => t.setAttribute('aria-selected', t.dataset.k === key ? 'true' : 'false'));
    status.textContent = DEFAULT_STATUS;
  };

  tabs.forEach((t) => t.addEventListener('click', () => show(t.dataset.k)));

  const selectText = (el) => {
    const range = document.createRange();
    range.selectNodeContents(el);
    const sel = window.getSelection();
    sel.removeAllRanges();
    sel.addRange(range);
  };

  // Clipboard API where allowed; otherwise select the text so it can be copied by hand
  const copy = (text, el, ok, fallback) => {
    try {
      navigator.clipboard.writeText(text).then(ok, () => {
        if (el) selectText(el);
        fallback();
      });
    } catch {
      if (el) selectText(el);
      fallback();
    }
  };

  copyBtn.addEventListener('click', () => {
    copy(MSGS[current], msg,
      () => { status.textContent = 'Copied. Paste it into a text or email.'; },
      () => { status.textContent = 'Selected. Press Ctrl+C or Cmd+C to copy.'; });
  });

  if (shareBtn && shareStatus) {
    shareBtn.addEventListener('click', () => {
      shareStatus.hidden = false;
      copy('https://' + LINK, null,
        () => { shareStatus.textContent = 'Link copied: ' + LINK; },
        () => { shareStatus.textContent = 'Link: ' + LINK; });
    });
  }

  show('friend');
})();
