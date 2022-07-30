//loader
$(window).on("load", ()=> {
    $(".loader-container").fadeOut(1000);
})

//responsive navbar
$(".toggleNav").click(() => {
    $(".toggleNav").toggleClass("close");
    $(".navbar-responsive").toggleClass("open");
    $(".navbar-responsive__link").toggleClass("open__link");
})

//make navbar visible
document.addEventListener("scroll", () => {
    const $navbar = $(".navbar");
    $navbar.toggleClass('sticky', $(this).scrollTop() > 250);
})