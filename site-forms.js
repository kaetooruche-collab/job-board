/* Shared submit handler for the site's forms (signup on the home page, /free-check, /order).
 * Posts JSON to /api/subscribe (api/subscribe.js) and shows the real answer. No keys here; the server holds the Brevo key. */
(function () {
  var EMAIL = (window.SITE && window.SITE.email) || 'yirehcareers@gmail.com';

  window.submitSiteForm = async function (ev, kind) {
    ev.preventDefault();
    var form = ev.target;
    var msg = form.querySelector('[data-msg]');
    var btn = form.querySelector('button[type="submit"]');
    var fd = new FormData(form);
    var payload = {
      form: kind,
      email: fd.get('email') || '',
      firstName: fd.get('firstName') || '',
      level: fd.get('level') || '',
      package: fd.get('package') || '',
      role: fd.get('role') || '',
      tips: fd.get('tips') === 'on',
      website: fd.get('website') || ''
    };
    function show(text, bad) {
      msg.hidden = false;
      msg.textContent = text;
      msg.className = 'form-msg ' + (bad ? 'is-bad' : 'is-ok');
    }
    btn.disabled = true;
    show('Sending...', false);
    var ok = false;
    try {
      var res = await fetch('/api/subscribe', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
      var data = await res.json();
      if (data && data.message) { show(data.message, !data.ok); ok = !!data.ok; }
      else show("We couldn't confirm that it went through. Please try again, or email us at " + EMAIL + '.', true);
    } catch (err) {
      show("We couldn't confirm that it went through. Please try again, or email us at " + EMAIL + '.', true);
    }
    if (ok) {
      form.reset();
      var done = document.querySelector('[data-after-success]');
      if (done) done.hidden = false;
    }
    btn.disabled = false;
    return false;
  };
})();
