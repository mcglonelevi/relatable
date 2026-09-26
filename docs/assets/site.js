// Shared page behaviour: footer year and the mailing-list forms.
document.querySelectorAll("[data-year]").forEach((el) => {
  el.textContent = new Date().getFullYear();
});

// Lucide icons (check-circle, alert-circle): messages never rely on colour alone.
const ICONS = {
  success: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg>',
  error: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><line x1="12" x2="12" y1="8" y2="12"/><line x1="12" x2="12.01" y1="16" y2="16"/></svg>',
};

// Sign-up forms post to MailerLite's subscribe URL (the form's action). MailerLite answers with
// JSON: {"success": true} or {"success": false, "errors": {"fields": {"email": ["…"]}}}.
document.querySelectorAll(".signup").forEach((form) => {
  const note = form.querySelector(".signup__note");
  const button = form.querySelector("button[type=submit]");
  const email = form.elements["fields[email]"];

  const say = (message, kind) => {
    note.innerHTML = kind ? ICONS[kind] : "";
    note.append(message);
  };

  // Counts a form view in MailerLite's stats, like their embed code does.
  fetch(form.action.replace(/\/subscribe$/, "/takel")).catch(() => {});

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (!email.checkValidity()) {
      say("That email doesn't look quite right. Try again?", "error");
      email.focus();
      return;
    }

    button.disabled = true;
    say("Signing you up…");
    try {
      const body = new URLSearchParams(new FormData(form));
      body.append("ajax", "1");
      const res = await fetch(form.action, { method: "POST", body });
      const data = await res.json();
      if (data.success) {
        form.classList.add("signup--done");
        say("You're on the list. We'll send a short note when there's news.", "success");
      } else {
        say(data.errors?.fields?.email?.[0] ?? "Something went wrong on our end. Try again in a minute?", "error");
      }
    } catch {
      say("We couldn't reach the sign-up service. Check your connection and try again.", "error");
    } finally {
      button.disabled = false;
    }
  });
});
