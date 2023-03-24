window.onload=(e)=>{
    // connection with websocket
    let listingId = window.location.pathname.split('/')[2]
    let socket=connect(`ws://${window.location.host}/ws/history/${listingId}`,"target")

   let historyForm=document.getElementById('historyForm')
   let commentForm=document.getElementById('commentForm')
   let historyList=document.getElementById('recycleView-history')
   let commentList=document.getElementById('recycleView-comment')

   const user_username = JSON.parse(document.getElementById('user_username').textContent);
   const user_img = JSON.parse(document.getElementById('user_img').textContent);
   const auction_author = JSON.parse(document.getElementById('auction_author').textContent);


   historyForm?.addEventListener("submit",(e)=>{

       if(user_username==auction_author){
           return
       }

       e.preventDefault()
       let bid = e.target[1].value
       socket.send(JSON.stringify({
            "type":"bid",
            "value":bid,
            "user":user_username,
            "img":user_img
       }))
   })

   commentForm?.addEventListener("submit",(e)=>{
       e.preventDefault()
       let comment = e.target[1].value
       socket.send(JSON.stringify({
            "type":"comment",
            "value":comment,
            "user":user_username,
            "img":user_img
       }))
       commentForm.reset()

   })


   function connect(url,target){
    let socket= new WebSocket(url)

    socket.onmessage = (e)=>{
        let data = JSON.parse(e.data)
        console.log(data)

        addToRecykleView(data)
    }
    return socket
}

   function addToRecykleView(dict){
    if (dict['type']==="comment"){
        commentList.innerHTML+=`            
        <li class="d-flex justify-content-between align-content-center recycleView-bid">
            <div class="d-flex">
                <div class="image-circleWraper" >
                    <img src=${dict["img"]} alt="profile image">
                </div>
                <div class="d-flex flex-column">
                    <div>${dict["user"]}</div>
                    <div>${dict["value"]}</div>
                </div>
            </div>
        </li>`
    }

    if(dict['type']==="bid"){
        historyList.innerHTML+=`               
        <li class="d-flex justify-content-between align-content-center recycleView-bid">
        <div class="d-flex">
            <div class="image-circleWraper" >
                <img src=${dict["img"]} alt="profile image">
            </div>
            ${dict["user"]}
        </div>
        <div>
            ${dict["value"]} PLN
        </div>
    </li>`
    }
        

}


}

