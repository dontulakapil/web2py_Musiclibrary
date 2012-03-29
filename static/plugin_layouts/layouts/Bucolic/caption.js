// Title: caption.js
// AUthor: Sadhana Ganapathiraju, aka SimplyGold <http://www.nikhedonia.com/>
// Purpose: automatically creates captiosn for images that want to be captionated
// Version: 1.0
// Notes: Currently doesn't work in IE. (Works in Firefox and Safari and Opera.)

var caption = 
{ 
	init : function()
	{	
		// Does the browser support the methods we use?
		if ( ! document.getElementById || ! document.createElement || ! document.appendChild )
		{
			return false;
		}
		
		// Find all images that want to get captionated
		var imageList = document.getElementsByTagName("img");
		
		var doCaption = new RegExp("(^|\\s)captionated(\\s|$)");
		
		for (i = 0; i < imageList.length; i++)
		{
			// Save the current image
			var current = imageList[i];			
			
			// Does the current image want to be captionated?
			if (doCaption.test(current.className) == false)
			{
				continue;
			}
			
			var altText = current.getAttribute("alt");
				
			if(altText == null || altText == "")
			{
				continue;
			}
			
			// We want the paragraph to span the full width of the image
			var imageWidth = parseInt(current.getAttribute("width"), 10);
			
			// Account for the padding
			imageWidth = imageWidth - 20;
			imageWidth = imageWidth + "px";
			
			var captionParagraph = document.createElement("p");
			captionParagraph.style.width = imageWidth;
			
			if (captionParagraph.opacity != undefined)
			{
				captionParagraph.opacity = .80;
			}
			
			else if (captionParagraph.style.MozOpacity != undefined)
			{
				// Mozilla
				captionParagraph.style.MozOpacity = 0.80;
			}
			
			else if(captionParagraph.style.filter != undefined)
			{
				// IE
				captionParagraph.style.filter = "alpha(opacity=80);";
			}
			
			captionParagraph.appendChild(document.createTextNode(altText));
			
			current.parentNode.appendChild(captionParagraph);
		}
	},

	addEvent : function(what, type, func)
	{
		if (what.addEventListener)
		{
			what.addEventListener(type, func, false);
		}
		
		else if (what.attachEvent)
		{
			what["e" + type + func] = func;
			
			what[type + func] = function() 
			{
				what["e" + type + func](window.event); 
			}
		}
	}
};

caption.addEvent(window, "load", function() { caption.init(); } );