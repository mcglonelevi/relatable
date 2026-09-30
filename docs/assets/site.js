// Shared page behaviour: footer year and the mailing-list forms.
document.querySelectorAll("[data-year]").forEach((el) => {
  el.textContent = new Date().getFullYear();
});

// Header logo. The clock "o" shows the visitor's local time: on load the hands sweep forward to it
// (the minute hand takes an extra lap), then they're nudged along every 30 seconds. The die over the
// "i" rolls on load. Hovering (or tabbing to) the logo rolls the die again and spins both hands a full turn.
document.querySelectorAll(".logo").forEach((logo) => {
  const clock = logo.querySelector(".logo-clock");
  const die = logo.querySelector(".logo-die");
  if (!clock) return;
  const hands = { hour: clock.querySelector(".logo-hour"), minute: clock.querySelector(".logo-minute") };
  // Angles the hands are drawn at in the artwork, in degrees clockwise from 12 o'clock.
  const DRAWN = { hour: 305.5, minute: 38 };
  const reduceMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;
  // Rotation applied on top of the artwork: what's on screen now, and where each hand is headed.
  // Both only ever grow, so the hands always move clockwise.
  const shown = { hour: 0, minute: 0 };
  const heading = { hour: 0, minute: 0 };
  const runs = {};

  // The hands live in the clock's own 100 x 100 space, centred on (50, 50).
  const rotate = (name, deg) => {
    shown[name] = deg;
    hands[name].setAttribute("transform", `rotate(${deg.toFixed(2)} 50 50)`);
  };

  // Ease a hand from wherever it is now to `to`, replacing any animation already running on it.
  const animate = (name, to, duration) => {
    heading[name] = to;
    if (reduceMotion || !duration) return rotate(name, to);
    const from = shown[name];
    const start = performance.now();
    const run = (runs[name] = {});
    const frame = (now) => {
      if (runs[name] !== run) return; // a newer animation took over
      const t = Math.min(Math.max((now - start) / duration, 0), 1);
      rotate(name, from + (to - from) * (1 - Math.pow(1 - t, 3))); // ease-out
      if (t < 1) requestAnimationFrame(frame);
    };
    requestAnimationFrame(frame);
  };

  const moveToNow = (extraLap, duration) => {
    const d = new Date();
    const minutes = d.getMinutes() + d.getSeconds() / 60;
    const target = { hour: ((d.getHours() % 12) + minutes / 60) * 30, minute: minutes * 6 };
    for (const name of ["hour", "minute"]) {
      const pointing = (DRAWN[name] + heading[name]) % 360;
      const step = (((target[name] - pointing) % 360) + 360) % 360 + (name === "minute" ? extraLap : 0);
      animate(name, heading[name] + step, duration);
    }
  };

  // A full turn for both hands; they land back on the current time.
  const spin = () => {
    for (const name of ["hour", "minute"]) animate(name, heading[name] + 360, 900);
  };

  // Restart the CSS roll.
  const roll = () => {
    if (!die || reduceMotion) return;
    die.classList.remove("is-rolling");
    die.getBoundingClientRect(); // reflow, so re-adding the class starts the animation over
    die.classList.add("is-rolling");
  };
  die?.addEventListener("animationend", () => die.classList.remove("is-rolling"));

  const play = () => { roll(); spin(); };
  logo.addEventListener("mouseenter", play);
  logo.addEventListener("focus", () => { if (logo.matches(":focus-visible")) play(); });

  moveToNow(360, 1400);
  roll();
  setInterval(() => moveToNow(0, 600), 30_000);
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
