function testAjax(page, records) {
	var xhr:XMLHttpRequest = new XMLHttpRequest();
	xhr.open("GET", "/app/data?page="+page+"&records="+records)
	xhr.onreadystatechange = function() {
		if(xhr.status==200 && xhr.readyState==4) {
			console.log(JSON.parse(xhr.responseText))
		}
	}
	xhr.send()
}