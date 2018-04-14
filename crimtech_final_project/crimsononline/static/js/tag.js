$(document).ready(function() {
	$('input[value="all"]').change(function() {
		if (this.getAttribute('name') == 'section')
		{
			$('#sectionform input[type="checkbox"]').prop('checked', false);
			$('#sectionform').children().trigger('change');
		}
		else
		{
			$('#typeform input[type="checkbox"]').prop('checked', false);
			$('#typeform').children().trigger('change');
		}
	});

	$('#sectionform, #typeform').children().change(function() {
		$('#loadingimg').show();
		//alert($('#articlezone').html());
		$('.articles').fadeOut('fast', function() {
			$(this).empty().html('<img src="' +  $('#preloadingimg').attr('src') + '" id="loadingimg">').fadeIn('fast', function() {
				var tagname = $('#sectionform input[type="hidden"]').val();
				var ajaxurl = '/tag/' + tagname + '/';
				if ($('#sectionform :checked').length > 0)
				{
					$('input[name="section"][value="all"]').prop('checked', false);
					ajaxurl += 'sections/'
					$('#sectionform :checked').each(function() {
						ajaxurl += $(this).val() + ',';
					});
					ajaxurl = ajaxurl.substr(0, ajaxurl.length - 1);
					ajaxurl += '/';
				}
				else if (this.getAttribute('value')!="all")
				{
					$('input[name="section"][value="all"]').prop('checked', true);
				}

				if ($('#typeform :checked').length > 0)
				{
					$('input[name="type"][value="all"]').prop('checked', false);
					ajaxurl += 'types/'
					$('#typeform :checked').each(function() {
						ajaxurl += $(this).val() + ',';
					});
					ajaxurl = ajaxurl.substr(0, ajaxurl.length - 1);
					ajaxurl += '/';
				}
				else if (this.getAttribute('value')!="all")
				{
					$('input[name="type"][value="all"]').prop('checked', true);
				}
				//alert(ajaxurl);
				window.history.pushState('Object', 'Title', ajaxurl);

				ajaxurl += '?ajax=1';
				$.ajax({url: ajaxurl}).done(function(data) {
					//alert(data);
					$('.articles').fadeOut('fast', function() {
						$('#articlezone').html(data);
						$('.articles').fadeIn('fast');
						$('#loadingimg').hide();
					});
				});
			});
		});
	});
});
