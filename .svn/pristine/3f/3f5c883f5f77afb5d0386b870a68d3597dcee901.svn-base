// [Copyright]
// SmartPath v1.0
// Copyright 2014-2015 Mountain Pass Solutions, Inc.
// This unpublished material is proprietary to Mountain Pass Solutions, Inc.
// [End Copyright]

$(function() {
    // Support #names in URL loads & page reloads to get user back into sub-tabs
    cvApp.bootstrap_tab_bookmark(".nav-tabs li a");

    $('div[role="tabpanel"] .nav-tabs li').on('click', 'a', function(e){
	    // console.log('clicky:', e.target)
	    cvApp._processTabsToPreventScrolling(e.target);
	    e.preventDefault();
	    e.stopPropagation();
	});


    /*
    // Main NavBar auto-open menus: [Saved for later?]
    $('.mpsheader .navbar .dropdown').hover(function() {
        $(this).addClass('open');
        //$(this).find('.dropdown-menu').first().stop(true, true).slideDown(150);
    }, function() {
        $(this).removeClass('open');
        //$(this).find('.dropdown-menu').first().stop(true, true).slideUp(105)
    });
    */


    //
    // Global Status/Error Message Removal after page load (the msg is in the DOM when loaded).
    //
    if($('body .cv-global-message-content').text().replace(' ','').length > 0){
        var $bar = $('body .cv-global-message');
        window.setTimeout(function(){cvApp.showHeaderMessage($('body .cv-global-message').text(), 'info')}, 0);
        window.setTimeout(function(){cvApp.hideHeaderMessage()}, 6000);
    }
    $('body .cv-global-message .cv-close').on('click', function(){cvApp.hideHeaderMessage()});


    // Global Modal Initialization (Scroll Top, and Enable Button)
    $('#editModal').on('shown.bs.modal', function () {
        $('#editModal .modal-body').scrollTop(-600);
        $('#editModal #modalSaveButton').prop('disabled', false);
    });

    // Confirm Loss of unsaved Modal Edits:
    $('#editModal').on('change', ':input', function(){cvApp.isUnsavedModalWork = true;});
    $('#modalSaveButton').on('click', function(){cvApp.isUnsavedModalWork = false;});
    $('#editModal').on('hide.bs.modal', function(event){return cvApp._confirmUnsavedModalChanges(event)});

    // Singularize & Grammar fix the Add & Edit button Text (Category names are plural, Add/Edit should be singular)...
    /*  01/19/2016: Totally Remving This functionality
    var zBtns = $('.cvSingularize');
    zBtns.each(function(){
        var $btn = $(this), $txt = $btn.text(), root = '', ellip = '', wrds = '';
        if($txt.indexOf('...') > -1){
            ellip = '...';
            $txt = $txt.replace(ellip, '');
        }
        root = $txt.substr(0, $txt.indexOf(' '));
        var zWrds = $txt.replace(root, '').split(' ');
        for(i=0;i<zWrds.length;i++){
            var wrd = zWrds[i];
            if(wrd == "&" || wrd == "/"){wrd = 'or';}
            else{
                var noComma = wrd.replace(',','');
                wrd = noComma.singularize() + ((wrd.length > noComma.length) ? ',' : '');
            }
            zWrds[i] = wrd;
        }
        for(i=0;i<zWrds.length;i++){root += ' ' + zWrds[i];}
        $btn.text(root + ellip);
    });
    */

    // 01/25/2016 - String Terminating so that we don't have buttons that say e.g. 'Add Mentoring Activities Involving Junior Faculty or Post-Doctoral Students...'
    var zBtns = $('.cvmodaleditdetaillink .cvSingularize');
    zBtns.each(function(){
        var $btn = $(this), txt = $btn.text();
        // First try: Stop at first space >= 24th character?
        if(txt.length > 24){
            var rem = txt.substr(24),
                iS = rem.indexOf(' '),
                snew = (iS >= 0) ? txt.substr(0, 24+iS) + '...' : txt;
            $btn.text(snew);
        }

    });

    // Google Analytics: Log Print events:
    $('.cvPrint').on('click', 'ul:not(.mps-menu-disabled) a', function(e){
        var eType = ($(this).text().trim() == 'Print All') ? 'print_cv' : 'print_section',
            eLabel = cvApp.getSectionName();
        if (typeof ga != "undefined") {
	        ga('send', 'event', 'cv_print', eType, eLabel);
	    };
	});

	// Google Analytics: Log pubMed Import/export events:
    $('.cvManageExternalData').on('click', 'ul:not(.mps-menu-disabled) a', function(e){
        if (typeof ga != "undefined") {
            var eType = ($(this).text().trim() == 'Import CV') ? 'import_cv' : 'export_cv';
	        ga('send', 'event', 'external_data_menu', eType, {useBeacon: true});
	    };
	});

    // Slightly Kludge-y JS Layout fix as we have an abs-ps'd leftNav that might or might not be taller than content area
    window.setTimeout(function(){   // Timeout is to allow other things (e.g. Repeating Fields, etc) to render first...

        if($('body').hasClass('cv-import-page')){ return false; } // Not on Pubmed page: its leftNav is never taller than right side min-height

        var $TOC = $('body.cv .cv-body-content .cv-menu'),
            $Content = $('body.cv .cv-body-content');

        if($TOC.length > 0 && $Content.length > 0){
            var iTOC = $TOC.height(),
                iContent = $Content.height();
            if(iContent < iTOC){
                $Content.height(iTOC+45); // 45 ~= padding diffs etc (skin doesn't seem to matter)
            }
            else if(iTOC < iContent + 45){
                $TOC.height(iContent - 45); // In rare case where content is longer than leftNav, this extends the BG down
            }
        }
    },0);

});


