/* =========================================================
   ThaiVisaFinder — SHARED SITE JS
   Injects the shared footer (with MailerLite subscribe form) on every
   page so footer edits happen in ONE place.
   Every page needs, in place of the old inline <footer>:
     <div id="site-footer"></div>
     <script src="/assets/site.js" defer></script>  (before </body>)
   ========================================================= */

/* One footer ad slot (160x300, highperformanceformat). */
var TVF_AD =
  '<iframe title="Advertisement" width="160" height="300" scrolling="no" frameborder="0" marginwidth="0" marginheight="0" style="border:0;display:block;overflow:hidden" srcdoc=\'<body style="margin:0;overflow:hidden"><script type="text/javascript">atOptions = {"key":"9fb5ed3f58327b9ed9e9acd4af62f648","format":"iframe","height":300,"width":160,"params":{}};</script><script type="text/javascript" src="https://www.highperformanceformat.com/9fb5ed3f58327b9ed9e9acd4af62f648/invoke.js"></script></body>\'></iframe>';

/* MailerLite subscribe block (same form/list as ThaiThuk, tagged
   Company=ThaiVisaFinder so signups are traceable to this site). */
function subscribeHTML() {
  return `
          <div id="mlb2-44063259" class="ml-form-embedContainer ml-subscribe-form ml-subscribe-form-44063259" style="margin-top:22px;max-width:320px;">
            <div class="ml-form-embedWrapper">
              <div class="ml-form-embedBody row-form">
                <h4>Subscribe</h4>
                <p class="tvf-sub-note">Breaking updates to Thailand's Visa rules and exclusive offers from our network.</p>
                <form class="ml-block-form" action="https://assets.mailerlite.com/jsonp/2528952/forms/193796763912504673/subscribe" data-code="" method="post" target="_blank">
                  <div class="ml-form-fieldRow">
                    <input aria-label="email" aria-required="true" type="email" name="fields[email]" placeholder="Enter your email" autocomplete="email" required class="tvf-sub-input">
                  </div>
                  <input type="hidden" name="fields[company]" value="ThaiVisaFinder">
                  <input type="hidden" name="ml-submit" value="1">
                  <div class="ml-form-embedSubmit">
                    <button type="submit" class="primary tvf-sub-btn">Subscribe</button>
                    <button disabled="disabled" style="display:none" type="button" class="loading tvf-sub-btn">
                      <div class="ml-form-embedSubmitLoad"></div><span class="sr-only">Loading...</span>
                    </button>
                  </div>
                  <input type="hidden" name="anticsrf" value="true">
                </form>
              </div>
              <div class="ml-form-successBody row-success" style="display:none">
                <div class="ml-form-successContent">
                  <h4>Subscribe</h4>
                  <p class="tvf-sub-ok">Thank you — you're on the list! 🎉</p>
                </div>
              </div>
            </div>
          </div>`;
}

function footerHTML() {
  /* Allow a page to opt out of the signup form (e.g. quiz flows) with
     <body data-no-signup>. */
  var showSignup = !(document.body && document.body.hasAttribute('data-no-signup'));
  return `
  <footer data-xadr-footer><div class="xadr xadr-l" aria-label="Advertisement">${TVF_AD}</div><div class="xadr xadr-r" aria-label="Advertisement">${TVF_AD}</div>
    <div class="wrap">
      <div class="fgrid">
        <div style="max-width:340px;">
          <div class="brand-f"><span class="logo" role="img" aria-label="Thai Visa Finder logo"></span> <b>Thai Visa Finder</b></div>
          ${showSignup ? subscribeHTML() : ''}
        </div>
        <div>
          <h4>The tools</h4>
          <a href="/">Visa Finder</a>
          <a href="/#faq">Visa FAQ</a>
          <a href="/city-guide">City Guide</a>
          <a href="https://thaiholidaybudget.com/" target="_blank" rel="noopener">Budget Estimator ↗</a>
        </div>
        <div>
          <h4>Site &amp; legal</h4>
          <a href="/about">About</a>
          <a href="/contact">Contact</a>
          <a href="/privacy">Privacy Policy</a>
          <a href="/terms">Terms &amp; Disclaimer</a>
        </div>
      </div>
      <div class="legal">© 2026 Genext Information Systems. All rights reserved.</div>
    </div>
  </footer>`;
}

/* Styles for the subscribe form (footer is a fixed dark block, so these
   dark-themed values work in both light and dark site themes). */
var TVF_STYLE = `
.ml-form-embedSubmitLoad{display:inline-block;width:20px;height:20px}
.ml-form-embedSubmitLoad:after{content:" ";display:block;width:11px;height:11px;margin:1px;border-radius:50%;border:3px solid #fff;border-color:#fff #fff #fff transparent;animation:tvf-sub-spin 1.2s linear infinite}
@keyframes tvf-sub-spin{0%{transform:rotate(0)}100%{transform:rotate(360deg)}}
.ml-subscribe-form .tvf-sub-note{color:#A6A8CC;font-size:.82rem;margin:0 0 12px}
.ml-subscribe-form .tvf-sub-input{width:100%;box-sizing:border-box;padding:11px 14px;border-radius:8px;background:#EDEEF5;color:#191B2C;font:inherit;font-size:.92rem;border:1px solid transparent;outline:none;margin:0}
.ml-subscribe-form .tvf-sub-input::placeholder{color:#6b6e8f}
.ml-subscribe-form .tvf-sub-input:focus{border-color:#E8C57C;box-shadow:0 0 0 2px rgba(232,197,124,.35)}
.ml-subscribe-form .ml-form-embedSubmit{margin-top:12px}
.ml-subscribe-form .tvf-sub-btn{display:inline-flex;align-items:center;justify-content:center;padding:11px 22px;border-radius:8px;background:#1B1E30;color:#fff;font:inherit;font-size:.9rem;font-weight:600;border:1px solid rgba(232,197,124,.5);cursor:pointer;transition:border-color .15s,color .15s}
.ml-subscribe-form .tvf-sub-btn:hover{border-color:#E8C57C;color:#E8C57C}
.ml-subscribe-form .tvf-sub-ok{color:#E8C57C;font-weight:600;font-size:.92rem;margin:0}
.ml-subscribe-form .sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);border:0}
`;

/* MailerLite success callback (swaps form for the thank-you message). */
window.ml_webform_success_44063259 = function () {
  var $ = window.ml_jQuery || window.jQuery;
  if ($) {
    $('.ml-subscribe-form-44063259 .row-success').show();
    $('.ml-subscribe-form-44063259 .row-form').hide();
  } else {
    document.querySelectorAll('.ml-subscribe-form-44063259 .row-success')
      .forEach(function (el) { el.style.display = ''; });
    document.querySelectorAll('.ml-subscribe-form-44063259 .row-form')
      .forEach(function (el) { el.style.display = 'none'; });
  }
};

function initMailerLite() {
  if (!document.querySelector('.ml-subscribe-form-44063259')) return;
  if (!document.getElementById('ml-webforms-js')) {
    var s = document.createElement('script');
    s.id = 'ml-webforms-js';
    s.src = 'https://groot.mailerlite.com/js/w/webforms.min.js?v83147fa8ce2d95cb73ece7f28b469519';
    s.async = true;
    document.body.appendChild(s);
  }
  try {
    fetch('https://assets.mailerlite.com/jsonp/2528952/forms/193796763912504673/takel');
  } catch (e) {}
}

/* ---------- BOOT ---------- */
document.addEventListener('DOMContentLoaded', function () {
  if (!document.getElementById('tvf-footer-css')) {
    var st = document.createElement('style');
    st.id = 'tvf-footer-css';
    st.textContent = TVF_STYLE;
    document.head.appendChild(st);
  }
  var f = document.getElementById('site-footer');
  if (f) f.outerHTML = footerHTML();
  initMailerLite();
});
