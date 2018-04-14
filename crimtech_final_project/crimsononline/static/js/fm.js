$(document).ready(function(){
	$('#magazine-nav li > a').click(function(){
		$('#magazine-nav a').removeClass('active');
		$(this).addClass('active');
		//alert(this.id);
		$('.magazine-category').hide();
		$('#' + this.id.split('_')[0]).show();
		return false;
	});

	$('#magazine-nav li > a:first').trigger('click');

	$('#magazine-secondary .magazine-mobile-nav a').click(function() {
        event.preventDefault();
        $('#magazine-secondary #magazine-nav').toggleClass('mobile-hidden');
        console.log($('#magazine-secondary #magazine-nav'));
        $(this).toggleClass('active');
    });
});
