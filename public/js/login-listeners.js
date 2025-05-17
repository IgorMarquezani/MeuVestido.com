const loginForm = document.getElementById("login-form")

loginForm.addEventListener("submit", (e) => {
  e.preventDefault()

  const loginErr = document.getElementById("login-error")
  loginErr.innerHTML = ""

  const email = document.getElementById("email")
  const passwd = document.getElementById("password")

  const form = new FormData()

  form.set("email", email.value)
  form.set("password", passwd.value)

  fetch("/login", {
    method: "POST",
    body: form
  }).then((resp) => {
    if (resp.status === 200) {
      window.location = "/"
    } else if (resp.status === 400) {
      loginErr.innerHTML = "e-mail ou senha inválidos"
    } else {
      loginErr.innerHTML = "erro inesperado"
    }
    return resp.text()
  }).then((data) => {
    console.log(data)
  })

})
