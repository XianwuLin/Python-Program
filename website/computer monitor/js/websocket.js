var ws = new WebSocket("ws://192.168.1.104/socket"); //("ws://xiaowu.nat123.net/socket");
var g1 = new JustGage({
	id: "cpuimage",
	value: 0,
	min: 0,
	max: 100,
	title: "CPU占有率",
});

function cam() {
	try {
		ws.send('cam');
	} catch (ex) {
		console.error(ex)
	}
};

function cpu_percent() {
		ws.send('cpu_percent');
};

function closewebsocket(){
	ws.close();
};

function erweima(){
	var data = $("#erweimatext").val();
	ws.send(data + '//////' + 'erweima');
}

ws.onmessage = function(event) {
	var ws_msg = eval('(' + event.data + ')');
	s_type = ws_msg.type
	if (s_type == 'cam') {
		var image = document.getElementById('smallImage');
		image.src = "data:image/jpeg;base64," + ws_msg.data;
	}
	if (s_type == 'cpu_percent') {
		g1.refresh(ws_msg.data);
	}
	if (s_type == 'erweima'){
		$("#erweimaimage").attr("src", "http://qr.liantu.com/api.php?text=" + ws_msg.data);
		console.log(ws_msg);
	}
};
