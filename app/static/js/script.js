// script.js

// Add your JavaScript code here
function previewImage(input, previewId) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function(e) {
            $('#' + previewId).attr('src', e.target.result);
            $('#' + previewId).css('display', 'block');
        }
        reader.readAsDataURL(input.files[0]);
    }
}

function uploadFile(inputId) {
    var fileInput = $('#' + inputId)[0];
    var file = fileInput.files[0];
    if (file) {
        // Code to upload file to server using AJAX or form submission
        // This is just a placeholder
        console.log('Uploading file:', file.name);
    } else {
        console.log('No file selected.');
    }
}

