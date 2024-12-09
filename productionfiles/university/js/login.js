import { apiUrl } from "./config.js";
import { convertFormData } from "./utils.js";

const url = `${apiUrl}/login`;
const form = document.getElementById("university-form");
const spinnerOverlay = document.getElementById("spinner-overlay");

async function submitEventHandler(form, event) {
  event.preventDefault();
  // Show spinner and disable form
  spinnerOverlay.classList.add("active");
  form.classList.add("form-disabled");
  const formData = $(form).serializeArray();
  const data = convertFormData(formData);
  // try {
  //   const response = await axios.post(url, data);
  //   if (response.data.status === "success") {
  //     window.location.href = "/university";
  //   }
  // } catch (error) {
  //   if (error.response && error.response.data) {
  //     console.log(error.response.data);
  //     Swal.fire({
  //       icon: "error",
  //       title: "Error!",
  //       text: error.response.data.error || "Invalid credentials",
  //       timer: 1500, // Auto close after 1.5 seconds
  //     });
  //   }
  // } finally {
  //   // Hide spinner and re-enable form
  //   spinnerOverlay.classList.remove("active");
  //   form.classList.remove("form-disabled");
  // }
}

$(document).ready(function () {
  // Initialize the form validation
  $("#login-form").validate({
    rules: {
      username: {
        required: true,
        minlength: 6,
      },
      password: {
        required: true,
        minlength: 6,
      },
    },
    messages: {
      username: {
        required: "username is required.",
        minlength: "username must be at least 6 characters long.",
      },
      password: {
        required: "password is required.",
        minlength: "password must be at least 6 characters long.",
      },
    },
    errorElement: "div",
    errorClass: "invalid-feedback",
    highlight: function (element) {
      $(element).closest(".form-control").addClass("is-invalid");
    },
    unhighlight: function (element) {
      $(element).closest(".form-control").removeClass("is-invalid");
    },
    errorPlacement: function (error, element) {
      if (element.prop("type") === "checkbox") {
        error.insertAfter(element.siblings("label"));
      } else {
        error.insertAfter(element);
      }
    },
    // submitHandler: submitEventHandler,
  });
  $("#login-form").submit(function () {
    spinnerOverlay.classList.add("active");
    form.classList.add("form-disabled");
  });
});
