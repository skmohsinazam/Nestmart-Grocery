function validateForm() {
    const fullName = document.getElementById('fullName').value;
    const email = document.getElementById('email').value;
    const phone = document.getElementById('phone').value;
    const password = document.getElementById('password').value;
    const dob = document.getElementById('dob').value;
    const gender = document.getElementById('gender').value;
    const address = document.getElementById('address').value;
    const imgUpload = document.getElementById('imgUpload').value;

    if (fullName === "" || email === "" || phone === "" || password === "" || dob === "" || gender === "" || address === "" || imgUpload === "") {
        alert("All fields must be filled out");
        return false;
    }

    // Validate phone number
    const phonePattern = /^[0-9]{10}$/;
    if (!phonePattern.test(phone)) {
        alert("Please enter a valid 10-digit phone number.");
        return false;
    }

    // Validate password (at least 8 characters)
    if (password.length < 8) {
        alert("Password must be at least 8 characters long.");
        return false;
    }

    return true;
}
