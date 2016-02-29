// [Copyright]
// SmartPath v1.0
// Copyright 2014-2015 Mountain Pass Solutions, Inc.
// This unpublished material is proprietary to Mountain Pass Solutions, Inc.
// [End Copyright]

//
// This takes Text inputs or Selects and adds [-][+] buttons to the right of them...
//      Params:
//          jOpts: a {} of options, there is a wrapper func cvApp._handleRepeatingFields that handles these if missing.
//          dom: the scope of the wrapper to make repeating inputs inside of
//
var mpsApp = mpsApp || {};
mpsApp._initRepeatingTextFields = function(jOpts, dom, doDec){
    doDec = (typeof doDec == 'undefined') ? false : doDec;
    var zRepeats = (typeof dom !== 'undefined') ? dom.find('.cvRowRepeating_Text') : $('.cvRowRepeating_Text');
    zRepeats.each(function(i,v){
        // Clear out any old buttons...
       var $that = $(this);
       $that.find('.cv-add-field, .cv-remove-field').remove();

        // create + buttons on last row...
        var $inputs = $that.find('input, select');

        // create buttons '-' on all other rows...
        for(i=0;i<$inputs.length;i++){
            var $input = $($inputs[i]);
            var sType = $input.is('select') ? 'Repeating_Select' : 'Repeating_Text';
            if($input.prop('disabled') == true){
                return false;
            }

            var _insertPlusBtn = function(){
                var $plusBtn = $('<button class="btn btn-sm btn-default cv-add-field" alt="Add another line..."><span class="glyphicon glyphicon-sm glyphicon-plus"></span></button>');
                $input.parent().find('.cv-repeating-controls').prepend($plusBtn);
                $plusBtn.bind('click', function(ev){
                    ev.stopPropagation();
                    ev.preventDefault();
                   var $newInput = _addNewRepeatingInput();
                   $newInput.focus();
                   mpsApp._initRepeatingTextFields(jOpts, dom);
                });
            };

            var _insertMinusBtn = function(){
                // Append '-' button...
                var $minusBtn = $('<button class="btn btn-sm btn-default cv-remove-field"><span class="glyphicon glyphicon-sm glyphicon-minus"></span></button>');
                $input.parent().find('.cv-repeating-controls').prepend($minusBtn);
                $minusBtn.bind('click', function(ev){
                    ev.stopPropagation();
                    ev.preventDefault();
                    var $row = $(ev.target).closest('.'+sType);
                    $row.prev().find('input:first, select:first').focus();
                    $row.remove();
                    mpsApp._initRepeatingTextFields(jOpts, dom);
                });
            };

            var _addNewRepeatingInput = function(){
                // ADD new Row on + clicks...
                   var $newInput = $that.find('input:first, select:first').clone().val(''),
                       $newRow = $('<div class="col-xs-offset-'+jOpts.iOffset+' col-xs-'+jOpts.iCols+' '+sType+' '+jOpts.sClass+'" alt="Remove this line..."><div class="cv-repeating-controls pull-right"></div></div>');

                   $newRow.append($newInput);
                   //$that.append($newRow); // FLRR need these to go above all DOM that isn't repeating fields...
                   var $lastRepeater = $that.find('.Repeating_Text, .Repeating_Select');
                   $newRow.insertAfter( $lastRepeater.eq($lastRepeater.length-1) );
                   return $newInput;
            }

            // The Logic:
            if( $inputs.length == 1 && i == 0 && doDec){
                //  We are going to have 2 minimum by inserting one now (unless the user just removed the 2nd manually)
                _addNewRepeatingInput();
                mpsApp._initRepeatingTextFields(jOpts, dom, true);
            }
            else if( i == $inputs.length - 1){
                // Last Input: gets the + button:
                _insertPlusBtn();
            }
            if( i > 0 ){
                // All not-first get Minus:
                _insertMinusBtn();
            }

            // TabIndex fix: put repeaters AFTER input in DOM:
            var oRow = $input.parent(),
                oDiv = oRow.find('.cv-repeating-controls');
            oDiv.insertAfter($input);

        }
    });
}