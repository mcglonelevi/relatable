// Shared page behaviour: footer year and mailing-list forms.
document.querySelectorAll("[data-year]").forEach((el) => {
  el.textContent = new Date().getFullYear();
});

document.querySelectorAll(".signup").forEach((form) => {
  const note = form.querySelector(".signup__note");
  form.addEventListener("submit", (event) => {
    const email = form.elements.email;
    if (!email.checkValidity()) {
      event.preventDefault();
      note.textContent = "That email doesn't look quite right. Try again?";
      email.focus();
      return;
    }
    if (!form.dataset.endpoint) {
      // No mailing-list provider connected yet: don't pretend the sign-up worked.
      event.preventDefault();
      note.textContent = "The list opens soon. Check back in a few days!";
      return;
    }
    form.action = form.dataset.endpoint;
  });
});
