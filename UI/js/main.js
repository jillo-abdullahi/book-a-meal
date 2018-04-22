function myFunction() {
	    var x = document.getElementById("myTopnav");
	    if (x.className === "topnav") {
	        x.className += " responsive";
	    } else {
	        x.className = "topnav";
	    }
	}

	function addToCart() {
		var order_item = document.getElementById("item").innerText;
		alert(order_item);

		

	}