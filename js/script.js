$(function() {
	main()
});

/*
	1. load jquer
	2. load xml
	3. parse xml
	4. add xml nodes to page
	5. add actions upvote, downvote, dismiss for each node
	6. user triggers action
	7. herp 

*/

var xmlDoc;
var findings;
var data = new Array();
function main () {
	xmlDoc = loadXMLDoc('./results/master_inspection.xml');
	findings = xmlDoc.getElementsByTagName("finding");
	addToData();
	addToPage();

}

function loadXMLDoc(filename) {
	if (window.XMLHttpRequest) {
	  	xhttp=new XMLHttpRequest();
	}
	else {// code for IE5 and IE6
	  	xhttp=new ActiveXObject("Microsoft.XMLHTTP");
	}
	
	xhttp.open("GET",filename,false);
	xhttp.send();
	return xhttp.responseXML;
} 

function addToData() {
	for (var i = 0; i < findings.length; i++) {
		finding = findings[i]
		data[i] = new Array();
		data[i]['finding'] = finding
		data[i]['id'] = finding.id;
		data[i]['link']= finding.getElementsByTagName("link")[0].innerHTML;
		data[i]['score'] = finding.getElementsByTagName("score")[0].innerHTML;
		data[i]['url'] = finding.getElementsByTagName("url")[0].innerHTML;
		data[i]['file'] = finding.getElementsByTagName("file")[0].innerHTML;
	};
}

function addToPage() {

	qmainDiv = $('#main').empty();
	for (var i = 0; i < data.length; i++) {
		qDiv = $('<div/>');
		qLink = createJQLink( data[i] );
		qH = createJQHeader( data[i] );
		qbtnUp = createJQButton( data[i], "up");
		qbtnDown = createJQButton( data[i], "down");
		qbtnDis = createJQButton( data[i], "dis");

		qH.appendTo(qDiv);
		qLink.appendTo(qDiv);
		qbtnUp.appendTo(qDiv);
		qbtnDown.appendTo(qDiv);
		qbtnDis.appendTo(qDiv);

		qDiv.appendTo(qmainDiv);

	};

}

function createJQLink(arg) {
	return 	jQuery('<a/>', {
			    id: 'link_' + arg['id'],
			    href: arg['url'],
			    target: '_blank',
			    text: arg['link'],
			    class: arg['id']
			});
}

function createJQHeader(arg) {
	return 	jQuery('<h2/>', {
			    id: 'h2_' + arg['id'],
			    text: arg['link'] + " - Score: " + arg['score'],
			    class: arg['id']
			});
}

function createJQButton(arg, type) {
	var qBtn = 	jQuery('<button/>', {
		    		id: 'btn_' + arg['id'],
			    	text: type,
			    	class: arg['id']
				});

	if (type === "up") {
		qBtn.click(function(){ ajax(arg['id'], "up")})
	}
	else if (type === "down") {
		qBtn.click(function(){ ajax(arg['id'], "down")})
	}
	else if (type === "dis") {
		qBtn.click(function(){ ajax(arg['id'], "dis")})
	}

	return qBtn
	
}

function ajax (id, vote) {
	$.ajax({
	    type: "POST",
	    url: "server.php",
	    data: {id: id, vote: vote},
	    contentType: 'application/x-www-form-urlencoded; charset=UTF-8',
	    beforeSend: function() {
	    	$('#main').empty();
	    },
	    success: function(data) {
	        location.reload(true)
	    },
	    error: function(data){
	        alert('Error');
	    }
	});
}