


function togglePasswordForm() {
    const form = document.getElementById("passwordForm");

    if (form.style.display === "none") {
      form.style.display = "block";
    } else {
      form.style.display = "none";
    }
  }



  function togglePassword(element) {
    const input = element.previousElementSibling;

    if (input.type === "password") {
      input.type = "text";
      element.textContent = "🙈";
    } else {
      input.type = "password";
      element.textContent = "👁️";
    }
  }