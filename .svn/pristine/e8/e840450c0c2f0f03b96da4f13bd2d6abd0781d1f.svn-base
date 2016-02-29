// [Copyright]
// SmartPath v1.0
// Copyright 2014-2015 Mountain Pass Solutions, Inc.
// This unpublished material is proprietary to Mountain Pass Solutions, Inc.
// [End Copyright]

//
// Lots of MPS pages & forms have a feature that allows one set of controls to show a different set of controls
//      e.g. 'Are you requesting a job waver?  Yes ( )  No ( )  <- Yes asks for a Text Area (an entire row)
//      with 'Reason for job posting waver' & a textarea.
//

// Params: (el) a jquery element

var mpsApp = mpsApp || {};
mpsApp._uberShow = function(el) {
    var oneCode;
    var mySplits;
    var $scope = (el.closest('.Repeating-Form').length > 0) ? el.closest('.Repeating-Form') : el.closest('form');
    // console.log('show scope is:', $scope);
    if(typeof el.data('showCodes') != 'undefined' && el.data('showCodes').length > 0) {
        mySplits = el.data('showCodes').split(",");
        $.each(mySplits, function(i, oneCode){
            $scope.find('.uberForm_'+oneCode).show().toggleClass('starthidden', false);
        });
    };
},

mpsApp._uberHide = function(el) {
    var oneCode;
    var mySplits;
    var $scope = (el.closest('.Repeating-Form').length > 0) ? el.closest('.Repeating-Form') : el.closest('form');
    // console.log('hide scope is:', $scope);
    if(typeof el.data('hideCodes') != 'undefined' && el.data('hideCodes').length > 0) {
        mySplits = el.data('hideCodes').split(",");
        $.each(mySplits, function(i, oneCode){
            $scope.find('.uberForm_'+oneCode).hide().toggleClass('starthidden', true);
        });
    };
},

mpsApp._uberFlipFlop = function(el) {
    mpsApp._uberHide(el);
    mpsApp._uberShow(el);
}