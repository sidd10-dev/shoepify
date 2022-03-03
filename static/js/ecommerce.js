const menu = document.querySelector('.menu')
menu.addEventListener('click',()=>{
    (document.querySelectorAll('.target')).forEach((item) => {
        item.classList.toggle('change');
    })
})

// Index slideshow
const slides = document.querySelectorAll('.bg')
let i = 1
function slideshow()
{
setInterval(() => {
    if(i!=0)
    {
        slides[i-1].style.opacity = 0
    }
    else
    {
        slides[slides.length-1].style.opacity = 0
    }
    slides[i].style.opacity = 1
    i++
    if(i == slides.length)
    {   
        i = 0;
    }
},5000)
}
slideshow()