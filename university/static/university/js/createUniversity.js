import { apiUrl } from "./config.js";
import { convertFormData } from "./utils.js";

const url = `${apiUrl}/create`;
const form = document.getElementById("university-form");
const spinnerOverlay = document.getElementById("spinner-overlay");

async function submitEventHandler(form, event) {
  event.preventDefault();
  // Show spinner and disable form
  spinnerOverlay.classList.add("active");
  form.classList.add("form-disabled");

  const formData = $(form).serializeArray();
  const data = convertFormData(formData);
  try {
    const response = await axios.post(url, data);
    if (response && response.data) {
      const data = response.data;
      console.log(data);
      //SWAL.FIRE here
      if (data.status === "success") {
        Swal.fire({
          icon: "success",
          title: "Success!",
          text: "University created !",
          showConfirmButton: false,
          timer: 1500, // Auto close after 1.5 seconds
        }).then(() => {
          // window.location.reload();
          form.reset();
        });
      }
    }
  } catch (error) {
    Swal.fire({
      icon: "error",
      title: "Error!",
      text: error.message || "An unexpected error occurred. Please try again.",
      timer: 1500, // Auto close after 1.5 seconds
    });
  } finally {
    // Hide spinner and re-enable form
    spinnerOverlay.classList.remove("active");
    form.classList.remove("form-disabled");
  }
}

$(document).ready(function () {
  // Initialize the form validation
  $("#university-form").validate({
    rules: {
      university_name: {
        required: true,
        minlength: 3,
      },
      state: {
        required: true,
        minlength: 2,
      },
      tuition_fees: {
        required: true,
        number: true,
        min: 0,
        max: 950000.0,
      },
      program_level: {
        required: true,
      },
      course_title: {
        required: true,
        minlength: 2,
      },
    },
    messages: {
      university_name: {
        required: "University name is required.",
        minlength: "University name must be at least 3 characters long.",
      },
      state: {
        required: "State is required.",
        minlength: "State must be at least 2 characters long.",
      },
      tuition_fees: {
        required: "Tuition fees are required.",
        number: "Please enter a valid number.",
        min: "Tuition fees must be a positive value.",
      },
      program_level: {
        required: "Please select a program level.",
      },
      course_title: {
        required: "Course title is required.",
        minlength: "Course title must be at least 2 characters long.",
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
    submitHandler: submitEventHandler,
  });
});
