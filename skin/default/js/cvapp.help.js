// [Copyright]
// SmartPath v1.0
// Copyright 2014-2015 Mountain Pass Solutions, Inc.
// This unpublished material is proprietary to Mountain Pass Solutions, Inc.
// [End Copyright]

$(function () {
    //
    // HELP Buttons & HELP Mode
    //
    $('body').on('click', '.cvHelpButton', function(event){
        var $btn = $(event.target),
            $help = $('.cv-category-help');

        if(!$help.is(':visible')){
            $help.slideDown().fadeIn();
            $btn.addClass('active');
            $('body').addClass('cvHelpOpen');

            // Send an event to GA:
            if (typeof ga != "undefined") {
                var eLabel = cvApp.getSectionName();
                ga('send', 'event', 'category_help', eLabel);
            };
        }
        else{
            $help.slideUp().fadeOut();
            $btn.removeClass('active');
            $('body').removeClass('cvHelpOpen');
        }

    });
    $('body').on('click', '.cv-close-help', function(event){
        var $btn = $(event.target),
            $help = $('.cv-category-help');

        $help.slideUp().fadeOut();
        $('.cvHelpButton').removeClass('active');
        $('body').removeClass('cvHelpOpen');
    });

    $('body').on('click', '.cvModalHelpButton', function(ev){
        var $btn = $(this),
            $icon = $btn.find('.glyphicon:first'),
            $form = $btn.closest('.modal-content').find('.modal-body form');

        ev.preventDefault();
        ev.stopPropagation();

        if(!$btn.hasClass('active')){
            $form.find('.cvFieldHelpBtn').fadeIn();
            $btn.addClass('active').find('.cv-button-title').html('Hide Help');
            $icon.removeClass('glyphicon-question-sign').addClass('glyphicon-remove');

            // Send an event to GA:
            if (typeof ga != "undefined") {
                var eLabel = cvApp.getSectionName();
                ga('send', 'event', 'modal_help', eLabel);
            };
        }
        else{
            $form.find('.cvFieldHelpBtn').fadeOut();
            $btn.removeClass('active').find('.cv-button-title').html('Show Help');
            $icon.removeClass('glyphicon-remove').addClass('glyphicon-question-sign');
        }
    });

    // Google Analytics: Log Modal Help Field click events:
    $('body').on('show.bs.popover', function(e){
	    var eLabel = cvApp.getSectionName(),
	        eRow = $(e.target).closest('.form-row').find('label:first').text().replace(/\W+/g, '');
	    if(typeof ga === 'function'){
	        ga('send', 'event', 'modal_help_popover', eRow, eLabel);
	    }
	});
});


