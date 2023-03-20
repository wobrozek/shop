let listingId = window.location.pathname.split('/')[2]
let socket=connect(`ws://${window.location.host}/ws/history/${listingId}`,"target")


function connect(url,target){
    let socket= new WebSocket(url)

    socket.onmessage = (e)=>{
        let data = JSON.parse(e.data)

        if(data.type === 'comment'){
            console.log(data)
        }

        if(data.type === 'bid'){
            console.log(data)
        }
    }
    return socket
}

window.onload=(e)=>{
   let historyForm=document.getElementById('historyForm')
   let commentForm=document.getElementById('commentForm')

   historyForm.addEventListener("submit",(e)=>{
       e.preventDefault()
       let bid = e.target[1].value
       socket.send(JSON.stringify({
            "bid":bid
       }))
   })

   commentForm.addEventListener("submit",(e)=>{
       e.preventDefault()
       let comment = e.target[1].value
       socket.send(JSON.stringify({
            "comment":comment
       }))
       commentForm.reset()

   })


}
