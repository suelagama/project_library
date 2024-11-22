// ============= Toggle button sideber =============

const sidebarToggle = document.querySelector("#sidebar-toggle");
sidebarToggle.addEventListener("click",function(){
    document.querySelector("#sidebar").classList.toggle("collapsed");
});


// ============= Datepicker =============

$(document).ready(function () {
    flatpickr(".flatpcker", {
        dateFormat: "d/m/Y",
        allowInput: true,
        locale: "pt",
        //defaultDate: "today"

    });
});


// ============= Upload image =============

    const inputFile = document.querySelector("#id_cover");
    const pictureImage = document.querySelector(".picture__image");
    const pictureImageTxt = "Choose an image";
    // pictureImage.innerHTML = pictureImageTxt;

    inputFile.addEventListener("change", function (e) {
        const inputTarget = e.target;
        const file = inputTarget.files[0];

        if (file) {
            const reader = new FileReader();

            reader.addEventListener("load", function (e) {
                const readerTarget = e.target;

                const img = document.createElement("img");
                img.src = readerTarget.result;
                img.classList.add("picture__img");

                pictureImage.innerHTML = "";
                pictureImage.appendChild(img);
            });

            reader.readAsDataURL(file);
        } else {
            pictureImage.innerHTML = pictureImageTxt;
        }
    });