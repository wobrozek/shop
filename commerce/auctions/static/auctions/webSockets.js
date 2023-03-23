let listingId = window.location.pathname.split('/')[2]
let socket=connect(`ws://${window.location.host}/ws/history/${listingId}`,"target")


function connect(url,target){
    let socket= new WebSocket(url)

    socket.onmessage = (e)=>{
        let data = JSON.parse(e.data)

        console.log(data)

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

   const user_id = JSON.parse(document.getElementById('user_username').textContent);
   const user_img = JSON.parse(document.getElementById('user_img').textContent);


   historyForm?.addEventListener("submit",(e)=>{
       e.preventDefault()
       let bid = e.target[1].value
       socket.send(JSON.stringify({
            "type":"bid",
            "value":bid,
            "user":user_id,
            "img":user_img
       }))
   })

   commentForm.addEventListener("submit",(e)=>{
       e.preventDefault()
       let comment = e.target[1].value
       socket.send(JSON.stringify({
            "type":"comment",
            "value":comment,
            "user":user_id,
            "img":user_img
       }))
       commentForm.reset()

   })


}
