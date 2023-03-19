connect(`ws://${window.location.host}/ws/history/`,"target")

function connect(url,target){
const socket= new WebSocket(url)

socket.onmessage = (e)=>{
    let data = JSON.parse(e.data)
    console.log('Data:',data)
}

}