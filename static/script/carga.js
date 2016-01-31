var $image = $("#lienzo").first();
var $downloadingImage = $("#lienzo");
var arr_img = ['1.jpg', '2.jpg', '3.jpg', '4.jpg', '5.jpg', '6.jpg', '7.jpg', '8.jpg', '9.jpg', '10.jpg', '11.jpg', '12.jpg'];
var i = 0;
var myvar;
function cargaImg(){
	$downloadingImage.load(function(){
		$image.attr("src", $(this).attr("src"));	
	});
	$("#lienzo").attr({src:"img/"+arr_img[i]});
	if(i==11){
		i = 0;
	}else{
		i++;
	}
	clearTimeout(myvar);
	myvar = setTimeout(cargaImg, 3000);
}
myvar = setTimeout(cargaImg, 3000);

$(".menu_img").click(function(){
	clearTimeout(myvar);
	var attr = $(this).attr('src');
	$("#lienzo").attr({src:attr});
});
