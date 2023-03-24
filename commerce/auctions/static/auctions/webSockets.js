window.onload=(e)=>{
    // connection with websocket
    let listingId = window.location.pathname.split('/')[2]
    let socket=connect(`ws://${window.location.host}/ws/history/${listingId}`,"target")

   let historyForm=document.getElementById('historyForm')
   let commentForm=document.getElementById('commentForm')
   let historyList=document.getElementById('recycleView-history')
   let commentList=document.getElementById('recycleView-comment')
   let priceDiv=document.querySelector('.auction-price')


   const user_id = JSON.parse(document.getElementById('user_id').textContent);
   const auction_id = JSON.parse(document.getElementById('auction_id').textContent);
   const auction_author_id = JSON.parse(document.getElementById('auction_author_id').textContent);


   historyForm?.addEventListener("submit",(e)=>{

       if(user_id==auction_author_id){
           return
       }

       e.preventDefault()
       let bid = e.target[1].value
       socket.send(JSON.stringify({
            "type":"bid",
            "type":"bid",
            "value":bid,
            "user_id":user_id,
            "auction_id":auction_id

       }))
   })

   commentForm?.addEventListener("submit",(e)=>{
       e.preventDefault()
       let comment = e.target[1].value
       socket.send(JSON.stringify({
            "type":"comment",
            "value":comment,
            "user_id":user_id,
            "auction_id":auction_id
       }))
       commentForm.reset()

   })


   function connect(url,target){
    let socket= new WebSocket(url)

    socket.onmessage = (e)=>{
        let data = JSON.parse(e.data)

        addToRecykleView(data)
    }
    return socket
}

   function addToRecykleView(dict){
    if (dict['type']==="comment"){
    //  delete empty palceholder if exist
        let toDelete=commentList.querySelector('.deleteIfNotEmpty')
        toDelete?.remove()

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
        historyForm.reset()
        priceDiv.innerText=`Price: ${dict["value"]}`
        //  delete empty palceholder if exist
        let toDelete=historyList.querySelector('.deleteIfNotEmpty')
        toDelete?.remove()

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

