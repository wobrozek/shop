window.onload=(e)=>{
    let listingId = window.location.pathname.split('/')[2]
    let buttonStars=document.querySelectorAll('.watchstar')

    for(let button of buttonStars){
        button.addEventListener('click',(e)=>{
            fetch(`http://${window.location.host}/listing/watchlist/${e.target.dataset.id}`).then(res =>{
                if(res.ok){
                    e.target.classList.toggle("star-active")
                }
            })
        })


    }
}