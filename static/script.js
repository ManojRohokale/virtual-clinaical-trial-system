document.addEventListener("DOMContentLoaded", function() {
  const form = document.getElementById("patientForm");
  if (form) {
    form.addEventListener("submit", function(event) {
      const age = form.querySelector("input[name='Age']").value;
      if (age < 18 || age > 90) {
        alert("Age must be between 18 and 90");
        event.preventDefault();
      }
    });
  }
});
