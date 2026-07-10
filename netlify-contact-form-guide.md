# Netlify AJAX Contact Form — Reusable Setup Guide

A drop-in contact form that submits in the background (no redirect to Netlify's
generic "submission received" page), shows an on-page "Your message was sent"
toast, and emails each submission to your inbox.

Two halves: **(A) the page code** and **(B) the Netlify dashboard setup**. Both
are required. Skipping B means submissions are captured but no email is sent.

---

## A. Page code

### 1. The form markup

Requirements Netlify checks for: the `data-netlify="true"` attribute, a unique
`name` on the `<form>`, a hidden `form-name` input that matches it, and a unique
`name` on every field.

```html
<form id="contactForm" class="cform" name="contact" method="POST"
      data-netlify="true" data-netlify-honeypot="bot-field">
  <input type="hidden" name="form-name" value="contact">
  <input type="hidden" name="subject" id="c-subject" value="General question">
  <p class="hp" hidden><label>Don't fill this out if you're human: <input name="bot-field"></label></p>

  <label for="c-name">Your name</label>
  <input id="c-name" name="name" autocomplete="name" required>

  <label for="c-email">Your email</label>
  <input id="c-email" name="email" type="email" autocomplete="email" required>

  <label for="c-msg">Message</label>
  <textarea id="c-msg" name="message" rows="6" required></textarea>

  <button type="submit" class="contact-btn">Send message →</button>
</form>
```

### 2. The toast element (place anywhere, e.g. right before `</main>`)

```html
<div id="sentToast" class="toast" role="status" aria-live="polite">
  <span class="tick" aria-hidden="true">✓</span><span>Your message was sent</span>
</div>
```

### 3. The toast CSS

```css
.toast{position:fixed;left:50%;bottom:28px;transform:translateX(-50%) translateY(20px);
  background:#26276B;color:#fff;font-weight:700;font-size:1rem;
  padding:14px 22px;border-radius:12px;box-shadow:0 14px 34px -10px rgba(0,0,0,.45);
  display:flex;align-items:center;gap:10px;z-index:60;opacity:0;pointer-events:none;
  transition:opacity .3s ease,transform .3s ease;max-width:calc(100% - 32px);}
.toast.show{opacity:1;transform:translateX(-50%) translateY(0);}
.toast .tick{display:inline-flex;width:22px;height:22px;border-radius:50%;background:#fff;
  color:#26276B;align-items:center;justify-content:center;font-size:.85rem;font-weight:800;flex:0 0 auto;}
.contact-btn:disabled{opacity:.7;cursor:default;}
```

### 4. The submit script (place before `</body>`)

The key trick: `e.preventDefault()` stops the redirect, and `fetch('/')` posts the
form to Netlify in the background. On success it resets the form and shows the toast.

```html
<script>
  (function(){
    var form    = document.getElementById('contactForm');
    var btn     = form.querySelector('button[type="submit"]');
    var toast   = document.getElementById('sentToast');
    var toastTimer;

    // Optional: keep a hidden "subject" field synced to a <select id="c-topic">.
    // Delete this block if your form has no topic dropdown.
    var topic   = document.getElementById('c-topic');
    var subject = document.getElementById('c-subject');
    function syncSubject(){ if(topic && subject){ subject.value = topic.value; } }
    if(topic){ topic.addEventListener('change', syncSubject); }
    syncSubject();

    function showToast(){
      toast.classList.add('show');
      clearTimeout(toastTimer);
      toastTimer = setTimeout(function(){ toast.classList.remove('show'); }, 5000);
    }

    form.addEventListener('submit', function(e){
      e.preventDefault();
      if(!form.checkValidity()){ form.reportValidity(); return; }
      syncSubject();
      var label = btn.textContent;
      btn.disabled = true;
      btn.textContent = 'Sending…';
      fetch('/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams(new FormData(form)).toString()
      }).then(function(res){
        if(!res.ok){ throw new Error('Bad response'); }
        form.reset();
        syncSubject();
        showToast();
      }).catch(function(){
        alert('Sorry — something went wrong. Please email us directly and we\'ll get right back to you.');
      }).finally(function(){
        btn.disabled = false;
        btn.textContent = label;
      });
    });
  })();
</script>
```

> Note: this plain-HTML approach works because Netlify sees the real `<form>` in
> the served HTML. In a **SPA (React/Vue) where the form is JS-rendered**, you must
> also add a hidden static HTML form with the same `name` and fields so Netlify's
> build-time scan can detect it.

---

## B. Netlify dashboard setup (per site)

Do this once for every new site. **Capturing a submission and emailing it are two
separate things** — the form dashboard fills up automatically, but no email goes
out until you add a notification.

1. **Enable form detection.** Site → **Forms**. If the form isn't listed, click
   **Enable form detection**.

2. **Redeploy.** Form detection only re-scans on deploy. Your git push triggers
   one; otherwise **Deploys → Trigger deploy → Clear cache and deploy site**.

3. **Add the email notification.** Site → **Project configuration → Notifications
   → Form submission notifications → Add notification → Email notification.**
   Enter the inbox address and save.

4. **Test with a NEW submission.** Notifications are **not retroactive** — only
   submissions received *after* the notification exists get emailed.

---

## Gotchas that cost time (checklist)

- **Double-check the recipient address for typos.** A one-letter misspell
  (`thaivisafider` vs `thaivisafinder`) sends every email into the void with no
  error shown. This is the #1 silent failure.
- **Not retroactive.** Existing submissions never resend. Always test with a fresh one.
- **Check Spam / All Mail.** Netlify sends from `formresponses@netlify.com`; the
  first message often gets filtered. Mark "Not spam" + allowlist the sender.
- **Capture ≠ email.** Seeing submissions in the Forms dashboard does not mean an
  email was sent. That's the notification's job.
- **Your domain's SPF/DKIM/DMARC are irrelevant here.** Those govern mail sent
  *from* your domain. Notifications come *from* netlify.com *to* your inbox, so
  your DNS records don't gate them. (With a catch-all mailbox, any
  `anything@yourdomain.com` recipient will land in your inbox.)
- **Replies.** The notification arrives from `formresponses@netlify.com`; the
  visitor's real email is in the body. Reply to that address, not with plain "Reply."

---

## Quick per-project checklist

- [ ] Form has `data-netlify="true"`, unique `name`, hidden `form-name`, honeypot, uniquely-named fields
- [ ] Toast element + CSS added
- [ ] Submit script added (`preventDefault` + `fetch('/')`)
- [ ] Netlify: form detection enabled
- [ ] Netlify: redeployed
- [ ] Netlify: email notification added — **recipient address spelled correctly**
- [ ] Sent a fresh test; confirmed it landed (checked Spam too)
