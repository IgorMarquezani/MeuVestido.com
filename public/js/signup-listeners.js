const signupForm = document.getElementById("signup-form")

signupForm.addEventListener("submit", (e) => {
  e.preventDefault()

  const emailErr = document.getElementById("email-error")
  emailErr.innerHTML = ""

  const nameField = document.getElementById('name')
  const emailField = document.getElementById('email')
  const passwdField = document.getElementById('password')
  const confirmationField = document.getElementById('password-confirmation')

  if (passwdField.value != confirmationField.value) {
    return
  }

  const input = passwdField.value

  let upper, numeric, special = false

  for (let i = 0; i < input.length; i++) {
    const c = input[i];

    if (c.charCodeAt() >= 'A'.charCodeAt() && c.charCodeAt() <= 'Z'.charCodeAt()) {
      upper = true
    }
    if (c.charCodeAt() >= '0'.charCodeAt() && c.charCodeAt() <= '9'.charCodeAt()) {
      numeric = true
    }

    const ascii = c.charCodeAt()

    if (
      (ascii >= 33 && ascii <= 47) ||
      (ascii >= 58 && ascii <= 64) ||
      (ascii >= 91 && ascii <= 96) ||
      (ascii >= 123 && ascii <= 126)
    ) {
      special = true;
    }
  }

  if (!upper || !numeric || !special || input.length < 8) {
    return
  }

  const form = new FormData()

  form.append('name', nameField.value)
  form.append('email', emailField.value)
  form.append('password', passwdField.value)

  fetch('/signup', {
    method: 'POST',
    body: form
  }).then((resp) => {
    if (resp.status === 208) {
      emailErr.innerHTML = "e-mail já cadastrado"
      return
    }

    if (resp.status != 200) {
      return resp.json()
    }

    window.location = "/"
  }).then((json) => {
    console.log(json)
  })
})

const passwdInput = document.getElementById("password")

passwdInput.addEventListener("keypress", (e) => {
  const lengthDivCheck = document.getElementById("length-check")
  lengthDivCheck.innerHTML = `
    <i id="upper-icon" class="bi bi-dot"></i>
    <span>Min. 8 caracteres</span>`

  const upperCheckDiv = document.getElementById("upper-check")
  upperCheckDiv.innerHTML = `
    <i id="upper-icon" class="bi bi-dot"></i>
    <span>Ao menos 1 letra maiúscula</span>`

  const numericCheckDiv = document.getElementById("numeric-check")
  numericCheckDiv.innerHTML = `
    <i id="upper-icon" class="bi bi-dot"></i>
    <span>Ao menos 1 número</span>`

  const specialCheckDiv = document.getElementById("special-check")
  specialCheckDiv.innerHTML = `
    <i id="upper-icon" class="bi bi-dot"></i>
    <span>Ao menos 1 caractere especial (!@#$...)</span>`

  const input = passwdInput.value + e.key

  let upper, numeric, special = false

  for (let i = 0; i < input.length; i++) {
    const c = input[i];

    if (c.charCodeAt() >= 'A'.charCodeAt() && c.charCodeAt() <= 'Z'.charCodeAt()) {
      upper = true
    }
    if (c.charCodeAt() >= '0'.charCodeAt() && c.charCodeAt() <= '9'.charCodeAt()) {
      numeric = true
    }

    const ascii = c.charCodeAt()

    if (
      (ascii >= 33 && ascii <= 47) ||
      (ascii >= 58 && ascii <= 64) ||
      (ascii >= 91 && ascii <= 96) ||
      (ascii >= 123 && ascii <= 126)
    ) {
      special = true;
    }
  }

  if (upper) {
    upperCheckDiv.innerHTML = `
      <i class="bi bi-check-circle me-1 text-success"></i>
      <span>Ao menos 1 letra maiúscula</span>`
  }
  if (numeric) {
    numericCheckDiv.innerHTML = `
      <i class="bi bi-check-circle me-1 text-success"></i>
      <span>Ao menos 1 número</span>`
  }
  if (special) {
    specialCheckDiv.innerHTML = `
      <i class="bi bi-check-circle me-1 text-success"></i>
      <span>Ao menos 1 caractere especial (!@#$...)</span>`
  }
  if (input.length > 7) {
    lengthDivCheck.innerHTML = `
      <i class="bi bi-check-circle me-1 text-success"></i>
      <span>Min. 8 caracteres</span>`
  }
})

const togglePasswdBtn = document.getElementById("toggle-password")

togglePasswdBtn.addEventListener("click", () => {
  const passwdInput = document.getElementById("password")

  if (passwdInput.type === "password") {
    passwdInput.type = "text"
    togglePasswdBtn.classList.toggle("bi-eye-slash")
    togglePasswdBtn.classList.toggle("bi-eye")
  } else {
    passwdInput.type = "password"
    togglePasswdBtn.classList.toggle("bi-eye")
    togglePasswdBtn.classList.toggle("bi-eye-slash")
  }
})

const passwdConfirmationInput = document.getElementById("password-confirmation")

passwdConfirmationInput.addEventListener("keypress", (e) => {
  const input = passwdConfirmationInput.value + e.key
  const passwdConfirmationErr = document.getElementById("confirmation-password-error")

  if (input !== passwdInput.value && passwdConfirmationErr.classList.contains("d-none")) {
    passwdConfirmationErr.classList.toggle("d-none")
  }
  if (input === passwdInput.value && !passwdConfirmationErr.classList.contains("d-none")) {
    passwdConfirmationErr.classList.toggle("d-none")
  }
})
