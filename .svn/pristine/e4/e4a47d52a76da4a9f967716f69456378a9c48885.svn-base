// [Copyright]
// SmartPath v1.0
// Copyright 2014-2015 Mountain Pass Solutions, Inc.
// This unpublished material is proprietary to Mountain Pass Solutions, Inc.
// [End Copyright]

var cvApp = cvApp || {};

// BUGBUG: Deprecated??
cvApp._displayAlertMessage = function(options){
    //
    // Generic support for Page/UX level Bootstrap Alert with hide/show button added, style switching, etc
    // NOTE: This is deprecated in favor of a different design below (header message), code can be removed.
    options.target = (options.target) ? $(options.target) : $('errormessage');
    options.class = options.class || 'info';
    options.message = options.message || 'Something happened...';
    options.effect = options.effect || 'none';
    options.dismissible = options.dismissible || false;

    var $target = options.target;

    // Apply type...
    $target.removeClass('alert-warning alert-success alert-info alert-danger hidden').addClass('alert-'+options.class);

    $target.html(options.message);

    // Make Dismissible or not...
    if(options.dismissible){
        var btn = '<button type="button" class="close" aria-label="Close"><span aria-hidden="true">&times;</span></button>';
        if($target.find('button').length <= 0){
            $target.prepend($(btn));
            var $btn = $target.find('button');
            $btn.on('click', function(ev){
                $target.slideUp();
            });
        }
    }
    $target.show();
};
// BUGBUG: Deprecated??


cvApp._showPopoverErrorOnElement = function(options){
    if(options && options.focus !== false){options.focus = true;}
    var $el = $(options.target),
        sPlace = (typeof options.placement === 'string') ? options.placement : 'left';

    $el.parent().addClass(options.code);

    // Arbitrary fix for hidden elements with errors (e.g. Table'd Repeating Forms):
    var $par = $el.parent(),
        $gPar = $par.parent(),
        $ggPar = $gPar.parent(),
        bTriggered = 0;

    $.each([$el, $par, $gPar, $ggPar], function(iO, oO){
        if(!oO.is(':visible')){bTriggered = 0; oO.show(function(){$(this).trigger('wfValidateError');})}
    });
    // End new show() & trigger()

    // Date Tooltips interfere with Popovers...we will enable & disable the tooltip based on Popover state:
    $el.tooltip('destroy');

    window.setTimeout(function(){
        cvApp.scrollIntoView($el, options);
        //console.log('_showPopoverErrorOnElement', $el, options);
        if($el.length == 0){
            // Rare server-specified-non-existent element issue:
            cvApp.showHeaderMessage(data.errors, cvApp.ERROR);
        }
        $el.data('toggle', 'popover')
            .attr('title', options.title)
            .data('content', options.body)
            .data('placement', sPlace)
            .data('html', 'true')
            .data('animation', false)
            .data('container', '.'+options.code)
            //.data('trigger', 'focus')
            .on('click change keydown datePick', function(){
                $el.popover('destroy');
                $el.closest('.has-error').find('.popover').remove();
                // Date Tooltips interfere with Popovers...we will enable & disable the tooltip based on Popover state:
                $el.tooltip('show');
                $el.closest('.has-error').removeClass('has-error');
            })
            .popover('show');
    }, bTriggered);
};

cvApp.scrollIntoView = function(element, options){
    //console.log(element, element.length, options, element.offset());
    if(element.length == 0){
        return false;
    }
    var offset = element.offset().top;
    if(!element.is(":visible")) {
        element.css({"visiblity":"hidden"}).show();
        var offset = element.offset().top;
        element.css({"visiblity":"", "display":""});
    }
    if(options.focus !== false){element.focus();}

    //
    // We may be in a Modal window in CV...
    //
    var isModal = ($(element).closest('.modal-body:first').length > 0) ? $(element).closest('.modal-body:first') : false,
        iTop = (isModal !== false) ? 0 : $('.mpsheader:first').outerHeight() + 10,
        iBot = (isModal !== false) ? 0 : $('.mpsfooter:first').outerHeight() - 5,
        visible_area_start = $(window).scrollTop() + iTop, // for header...
        visible_area_end = visible_area_start - iBot; // for footer...

    if(offset < visible_area_start || offset > visible_area_end){
         // Not in view so scroll to it
         $('html,body, .modal-body').scrollTop(offset - window.innerHeight/3);
         return false;
    }
    return true;
}

cvApp._getDraggableTableRowIDsArray = function($sortTable){
    var zTRs = $sortTable.find('tr.item'),
        zIDs = [];

    for(i=0;i<zTRs.length;i++){
        zIDs.push($(zTRs[i]).data('item-id'));
    }

    return zIDs;
};

cvApp._disableDragAndDropRowUXs = function(){
    $('.cvReorderRow').css('visibility', 'hidden');
};
cvApp._enableDragAndDropRowUXs = function(){
    $('.cvReorderRow').css('visibility', 'visible');
};

cvApp._putDraggableTableRowIDsArray = function(zIDs){
    // BUGBUG: we probably ought to be UX blocking both row drag and table sorts during the POST...
    cvApp._disableDragAndDropRowUXs();
    cvApp.ubiquitousPageRequest({
        url: '/cv/sequence',
        sequence: zIDs,
        success_redirect: function(ev){
            cvApp._enableDragAndDropRowUXs();
            // BUGBUG TBD : Unblock further dragging...

            return false;
        },
        success_error:  function(data, textStatus, xhr){
            alert('Apologies, but something went very wrong - we will refresh the page to where you were before your last action. All of your work before your last action should already be saved...');
            // BUGBUG TBD : Big Hard coded Error Msg and redirect?
            window.location.reload();
            return false;
        },
        error: function(jqXHR, textStatus, errorThrown){
            alert('Apologies, but something went very wrong - we will refresh the page to where you were before your last action. All of your work before your last action should already be saved...');
            // BUGBUG TBD : Big Hard coded Error Msg and redirect?
            window.location.reload();
            return false;
        }
    });
};

// BUGBUG: Deprecated??
cvApp._getElementStateOptions = function($el){
    var state = {};

    // Load in the legacy payload:
    $.each(ajaxPayload, function(key, val){
        state[key] = val;
    });

    // Now get all data-cv-* attrs & add them (reserving a couple??)
    $.each($el.data(), function(key, val){
        var tmp = (key.indexOf("cv") == 0) ? key.substr(2, key.length).replace('-','').toLowerCase() : key ;
        if(tmp != key){
            state[tmp] = val;
        }
    });

    return state;
};
// BUGBUG: Deprecated??


cvApp._handleRepeatingFields = function(jOpts, dom){
    //
    // Feature: allow additional form controls in fieldType==Repeating in Details Add/Edit Modal
    //

    if(typeof jOpts != 'undefined'){
        jOpts.iCols = (typeof jOpts.iCols == 'undefined') ? 8 : jOpts.iCols;
        jOpts.iOffset = (typeof jOpts.iOffset == 'undefined') ? 3 : jOpts.iOffset;
        jOpts.sClass = (typeof jOpts.sClass == 'undefined') ? '' : jOpts.sClass;
        jOpts.isTabled = (typeof jOpts.isTabled == 'undefined') ? '' : jOpts.isTabled;
        jOpts.removeEmptyNs = false;
    }
    else{ jOpts = {iCols: 8, iOffset: 3, sClass: '', isTabled: false} }

    // Handle Repeating Text/Select fields:
    mpsApp._initRepeatingTextFields(jOpts, dom);


    // Handle Repeating FORMs:
    mpsApp._initRepeatingForms(jOpts, dom);

    return true;
};

cvApp.triggerLoadingStates = function(table){
    var $table = $('table.cv-data-table, .cv-singleentry-outer-panel').filter(":visible");
    $table.each(function(i,el){
        var $this = $(this),
            bTable = $this.hasClass('cv-data-table'),
            $body = (bTable) ? $this.find('tbody') : $this;

        $body.find('tr, .cv-list-singleentry-row').hide();
        $('.cv-table-footer-add-link').hide();
        if(bTable){
            $body.prepend($('<tr><td class="cv-table-loading" colspan="42"><img src="/default/images/ajax-loader.gif"/>Saving changes...</td></tr>'));
        }
        else{
            $body.prepend($('<div class="cv-table-loading"><img src="/default/images/ajax-loader.gif"/>Saving changes...</div>'));
        }

    });
    //cvApp.showHeaderMessage('Saving changes...', 'warning', true);
};

cvApp.INFO = 'info';
cvApp.WARN = 'warning';
cvApp.ERROR = 'danger';
cvApp.showPageMessage = function(text, msgType, element){
    // Newer: use page header UX for this?
    cvApp.showHeaderMessage(text, msgType);
    return true;
};
cvApp.hidePageMessage = function(element){
    // Newer: use page header UX for this:
    cvApp.hideHeaderMessage();
    return true;

};

cvApp.showHeaderMessage = function(msg, msgType, hideIcons, hideFirstIcon){
    var $element = $('.cv-global-message');

    // console.log('showHeaderMessage(): ', msg, msgType);
    if(hideIcons){
        $element.find('.glyphicon').hide();
        $element.show();
    }
    else{
        if(msgType === 'danger'){
            $element.find('.glyphicon').not('.cv-nochange').removeClass('glyphicon-ok').addClass('glyphicon-warning-sign');
        }
        else{
            $element.find('.glyphicon').not('.cv-nochange').removeClass('glyphicon-warning-sign').addClass('glyphicon-ok');
        }
        $element.find('.glyphicon').show();
        if(hideFirstIcon === true){
            $element.find('.glyphicon').not('.cv-nochange').hide();
        }
    }

    $element.find('.cv-global-message-content').empty().append(msg);
    $element.removeClass('cv-global-warning cv-global-danger cv-global-info')
            .addClass('cv-global-'+msgType)
            .slideDown('slow');
    //window.setTimeout(function(){cvApp.hideHeaderMessage();}, 4000);
};
cvApp.hideHeaderMessage = function(smsg, bClearMsg){
    var $element = $('.cv-global-message');
    $element.removeClass('cv-global-warning cv-global-danger cv-global-info')
            .addClass('cv-global-info');
    $element.find('.glyphicon').show();
    if(bClearMsg === true){
        $element.hide();
    }
    else if(smsg && typeof smsg === 'string'){
        if(!$element.is(':visible')){$element.slideDown('fast');}
        $element.find('.cv-global-message-content').text(smsg);
        $element.delay(1500).slideUp();
    }
    else{
        $element.slideUp(1500);
    }
    $('body').removeClass('cv-show-global-message');
    $('#wf-modal-backdrop').hide().addClass('starthidden');
};


cvApp._processTabsToPreventScrolling = function(target){

        var panel = $(target).closest('div[role="tabpanel"]'),
            tabs = panel.find('ul[role="tablist"] li a'),
            panes = panel.find('.tab-content .tab-pane'),
            selectedHref = $(target).attr('href'),
            iSeld = 0;

        for(i=0;i < tabs.length;i++){
            if($(tabs[i]).attr('href') == selectedHref){
                iSeld = i;
            }
            $(tabs[i]).parent().removeClass('active');
            $(panes[i]).removeClass('active').hide();
            var $id = $(panes[i]).attr('id');
            $(panes[i]).attr('id', $id.replace('tab_', 'mps_'));

        }
        //console.log(target, iSeld, $(tabs[iSeld]), $(panes[iSeld]))
        $(tabs[iSeld]).parent().addClass('active');
        $(panes[iSeld]).addClass('active').show();
};

cvApp.bootstrap_tab_bookmark = function(selector) {
    if (selector == undefined) { selector = ''; }

    // Automagically jump on good tab based on anchor
    $(document).ready(function() {
        url = window.location.href.split('#');
        if(url[1] != undefined) {
            $(selector + '[href=#'+url[1]+']').tab('show');
            //console.log('showed tab?:', '[href=#'+url[1]+']');
            // Finally:
            cvApp._processTabsToPreventScrolling($(selector + '[href=#'+url[1]+']'));
        }
    });

    var update_location = function (event) {
        document.location.hash = this.getAttribute("href");
    }

    // Update hash based on tab
    $(selector + "[data-toggle=pill]").click(update_location);
    $(selector + "[data-toggle=tab]").click(update_location);

};

cvApp.postRedirect = function(sURL){
    var currentPath = window.location.pathname,
        currentHash = window.location.hash,
        _newLoc = parseUri(sURL),
        newPath = _newLoc['path'],
        newHash = '#'+_newLoc['anchor'];

    //console.log('postRedirect:', _newLoc, currentPath, currentHash);

    if(currentPath != newPath){
        window.location = sURL;
    }
    else{
        window.location.hash = newHash; // change JUST the #hash (no reload)
        window.location.reload(true);   // NOW reload, new hash will be included...
    }
};

//
// Add/Edit Warning Message for Unsaved Changes on Page unLoad
//
cvApp.isUnsavedModalWork = false;
cvApp._confirmUnsavedModalChanges = function(ev){
    if(cvApp.isUnsavedModalWork){
        var isOK = confirm('You have Unsaved changes. Click OK to abandon them, or Cancel to continue editing.');
        if(!isOK){return false;}
    }
    return true;
}

cvApp.getSectionName = function(){
    var sEction = location.pathname.substr(location.pathname.lastIndexOf('/')+1),
        zPaths = location.pathname.split('/');
        // Note: we don't want to include the userName in the URL if we are on a default /cv/view/community/userName or /cv/view/community/userName/ URL:
        if(zPaths.length == 5 || (zPaths.length == 6 && zPaths[5] == "")){
            sEction = 'Demographics'
        }
        return sEction;
}

var wfApp = wfApp || {};
//

//Mustache automagically escapes HTML, the trouble is, we use large blocks of html
Mustache.escape = function (string){ return String(string)};

wfApp.wfTemplate = function(str, data){
    //{{= is the mustache change tag sequence.
    str = "{{=[[ ]]=}} " + str;
    return Mustache.render(str, data);
};
wfApp.collectionToArray = function(collection){
    var zA = [];
    $.each(collection, function(i,item){
        zA.push(item);
    });
    return zA;
};
wfApp.usedGuids = [];
wfApp._createUniqueID = function(root){
    root = wfApp._safeDomGuid(root) || Math.floor(Math.random() * 20)+'';
    if($.inArray(root, wfApp.usedGuids) >= 0 || $('#'+root).length > 0){
        return wfApp._createUniqueID((root + Math.floor(Math.random() * 20)+''));
    }
    else{
        wfApp.usedGuids.push(root);
        return root;
    }
}
wfApp._safeDomGuid = function(root){
    return root.replace(/[^a-z0-9]/gi,'');
}

var isUxDebugMode = isUxDebugMode || false;
var uxDebug = function(){
  if(this.console && isUxDebugMode){
    console.log( Array.prototype.slice.call(arguments) );
  }
}

wfApp.replaceLineBreaks = function(str) {
    return (str + '').replace(/([^>\r\n]?)(\r\n|\n\r|\r|\n)/g, '$1'+ '<br/>' +'$2');
}

$(function() {
    $('.wf-details-footer-back').click(function(e){
        e.preventDefault();
        window.history.back();
    });
});

