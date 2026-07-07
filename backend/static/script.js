// Welcome Message
console.log("Todo Management Loaded Successfully");

// Delete Confirmation
const deleteLinks = document.querySelectorAll("a[href*='delete']");

deleteLinks.forEach(link => {
    link.addEventListener("click", function(e) {

        if(!confirm("Are you sure you want to delete this item?")){

            e.preventDefault();

        }

    });
});

// Smooth Button Click
const buttons = document.querySelectorAll("button");

buttons.forEach(btn=>{

    btn.addEventListener("click",()=>{

        btn.style.transform="scale(.97)";

        setTimeout(()=>{

            btn.style.transform="scale(1)";

        },100);

    });

});