// [Copyright]
// SmartPath v1.0
// Copyright 2014-2015 Mountain Pass Solutions, Inc.
// This unpublished material is proprietary to Mountain Pass Solutions, Inc.
// [End Copyright]

//
// Print button Magic: Clone to Header top right, bind Print Click to Alert user if Print is not going to be current do to Edits in page.
//      This JS file should be included in any page that has a Print Button in the button bar (eg Uber form & Visitor Uber forms, any other one-offs we want Print in.)
//

//
// BUGBUG: This should NOT be loaded ~12 times per WF page... Widgetize it so each form only gets One _create...
//

mpsApp = mpsApp || {};
mpsApp._copyPrintBtnToHeader = function($form){
    $('.wf-itemWidgetWrapper .wf-header-title .wf-print-item').remove()
    var $print = $form.find('.wf-details-form-btn-bar .wf-print-item'),
        isFormEdited = false;
    $form.one('change', 'input, textarea, select', function(){
        isFormEdited = true;
    });
    $print.
        one('click', function(e){
            e.preventDefault();
            e.stopPropagation();
            var $form = $(e.target).closest('.wf-itemWidgetWrapper').find('.mps-form:first');
            if(!($form.hasClass('wf-item-is-disabled') || isFormEdited === false)){
                var isWarned = confirm('The form you are about to print has been changed without first being Saved. \n\nPress OK to open the last saved version of this form - your print will not include any changes you have made.\n\nPress Cancel, then Save or Save as Draft, then Print in order to include any changes you have made on this page. ');
                if(isWarned){
                    window.open($print.attr('href'));
                }
            }
            else{
                window.open($print.attr('href'));
            }
        });
    var $clone = $print.clone(true);
    $clone
        .css({'margin-right':'15px', 'float': 'right'})
        .toggleClass('btn-primary btn-default')
        .appendTo($print.closest('.wf-itemWidgetWrapper').find('.wf-header-title:first'));
}