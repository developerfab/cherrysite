var $image = $("#lienzo").first();
var $downloadingImage = $("#lienzo");
var arr_img = ["1.jpg", "2.jpg", "3.jpg", "4.jpg", "5.jpg", "6.jpg", "7.jpg", "8.jpg", "9.jpg", "10.jpg", "11.jpg", "12.jpg", "13.jpg", "14.jpg", "15.jpg", "16.jpg", "17.jpg", "18.jpg", "19.jpg", "20.jpg", "21.jpg", "22.jpg", "23.jpg", "24.jpg", "25.jpg", "26.png", "27.jpg", "28.png", "29.jpg", "30.jpg", "31.jpg", "32.jpg", "33.jpg", "34.jpg", "35.jpg", "36.jpg", "37.jpg", "38.jpg", "39.jpg", "40.jpg", "41.jpg", "42.jpg", "43.jpg", "44.jpg", "45.jpg", "46.jpg", "47.jpg", "48.jpg", "49.jpg", "50.jpg", "51.jpg", "52.jpg", "53.jpg", "54.jpg", "55.jpg", "56.jpg", "57.jpg", "58.jpg", "59.jpg", "60.jpg", "61.jpg", "62.jpg", "63.jpg", "64.jpg", "65.jpg", "66.jpg", "67.jpg", "68.jpg", "69.jpg", "70.jpg", "71.jpg", "72.jpg", "73.jpg", "74.jpg"];
var i = 0;
var myvar;
function cargaImg(){
	$downloadingImage.load(function(){
		$image.attr("src", $(this).attr("src"));	
	});
	$("#lienzo").attr({src:"img/"+arr_img[i]});
	if(i==74){
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
