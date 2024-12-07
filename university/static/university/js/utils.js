export const convertFormData = (formData) => {
  const resultObject = {};

  formData.forEach((item) => {
    if (item.name === "amount") {
      resultObject[item.name] = parseFloat(item.value);
    } else if (item.name === "contact-btn") {
      return;
    } else {
      resultObject[item.name] = item.value;
    }
  });
  return resultObject;
};
