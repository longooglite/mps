// [Copyright]
// SmartPath v1.0
// Copyright 2014-2015 Mountain Pass Solutions, Inc.
// This unpublished material is proprietary to Mountain Pass Solutions, Inc.
// [End Copyright]

var wfApp = wfApp || {};

wfApp._sessionExpiryLogoutRequired = function(data){
    // NEW: Emergency 'succesful post, but response is a Login due to session Expiry' handling:
    if(typeof data == 'string' && data.indexOf('id="logginform"') > -1){
        var $unexpectedContentError = 'As a security measure, your session has timed out from disuse. Your last action was not completed.<br/><br/><a href="/mps/login">Please re-login to continue...</a>';
        cvApp.showHeaderMessage($unexpectedContentError, 'danger', false, true);
        $('#wf-modal-backdrop').show();
        return true;
    }
    else{
        return false;
    }
}

wfApp._WF_commonErrorHandler = function($form, data, textStatus, xhr){
    if(typeof data.errors == 'object'){
        wfApp._renderFormErrors(data.errors, $form);
    }
    if(typeof data.errors === 'string'){
        cvApp.showHeaderMessage(data.errors, cvApp.ERROR);
    }
    if ('msgid' in data){
        $.cookie('msgid', data.msgid, { path: '/'});
    }
    if(typeof data.redirect === "string"){
        cvApp.postRedirect(data.redirect);
    }
};

//
// _renderFormErrors() is similar to CV's _commonErrorHandler() et al, except that it is somewhat WF specific (eg .form-row logic)
//
wfApp._renderFormErrors = function(errors, $form){
    // New: remove any old error popovers & states:
    $('.has-error').removeClass('has-error');
    $('.popover').filter(function(){return $(this).attr('id').indexOf('popover') == 0}).popover('destroy');

    // highlight & popover on each error...backwards for rendering & ending scrolled to first:
    for(k=errors.length-1;k >=0 ;k--){
        var error = errors[k],
            $input = $form.find('input[name='+error.code+']:first, select[name='+error.code+']:first, textarea[name='+error.code+']:first');

        $input.focus().closest('.form-row').addClass('has-error');
        if($input.is(':visible'))$('html,body').scrollTop($input.offset().top-150);
        else{
            // hidden validation errors should not happen...but just in case?

        }

        // Generic Error Message for Date Input errors - but should/doies this ever get triggered with the undefined & length == 0 checks?
        if($input.hasClass('mps-date-picker') && (typeof error.message == 'undefined' || error.message.length == 0) ){
            error.message = 'Date should be in '+$input.attr('placeholder');
        }

        var $targSel = ($input.closest('.wf-form-right').length > 0) ? $input.closest('.wf-form-right') : ($input.parent().find('.wf-form-right').length > 0) ? $input.parent().find('.wf-form-right') : $input;
        cvApp._showPopoverErrorOnElement({
            target: $targSel,
            title: '',
            body: error.message,
            code: error.code,
            placement: 'right'
        });

        $input.closest('.form-row').find('.wf-form-right').click(function(){
            $(this).removeClass('has-error');
        });
    }
    return true;
}

wfApp.inputDelay = (function(){
    var timer = 0;
    return function(callback, ms){
        clearTimeout (timer);
        timer = setTimeout(callback, ms);
    };
})();

wfApp.textNodes = function(el) {
    return $(el).clone()
            .children()
            .remove()
            .end()
            .text();
};