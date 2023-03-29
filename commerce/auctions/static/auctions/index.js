async function getResponse(id,callback){
    const response = await fetch(`http://${window.location.host}/listing/watchlist/${id}`)
    const data = await response.json()

    callback(data)
}

window.onload=(e)=>{
    let listingId = window.location.pathname.split('/')[2]
    let buttonStars=document.querySelectorAll('.watchstar')
    let numberOfWatch=document.querySelector('.watch-list-number')

    for(let button of buttonStars){
        button.addEventListener('click',(e)=>{
            e.target.classList.toggle("star-active")
            getResponse(e.target.dataset.id,(data)=>numberOfWatch.innerText=data.watchList)
        })
    }
}