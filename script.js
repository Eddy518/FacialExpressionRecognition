const copyrightYear = document.querySelector("#year");
copyrightYear.textContent = (function () {
  return new Date().getFullYear();
})();
