function removeFlash() {
    const element = document.getElementById("div_flash");
    element.remove();
}

setInterval(removeFlash, 3000)

// $('.alert').alert()
// $(".alert").alert('close')