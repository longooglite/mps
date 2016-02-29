// [Copyright]
// SmartPath v1.0
// Copyright 2014-2015 Mountain Pass Solutions, Inc.
// This unpublished material is proprietary to Mountain Pass Solutions, Inc.
// [End Copyright]

$(function () {
    //
    // Table Drag & Drop sorting (simple client side only sorting below)
    //
    $('table.ui-sortable').each(function(index, el){
        var $sortTable = $(this),
            table_width = $sortTable.width();

        // Hmmm - some width & height setting necessary?
        var _fixInvisibleLayouts = function(table){
            $(table).find('tr').each(function(index){
                $(this).css({width: $(table).width(), height: $(this).height()});
                $(this).find('td').each(function(ind){
                    $(this).css({width:$(this).width(), height: $(this).height()});
                });
            });
        }

        $sortTable.find('tbody').sortable({
          axis: 'y',
          items: '.item',
          cursor: 'move',
          //revert: true,
          placeholder: "ui-state-highlight",
          opacity: 0.5,
          start: function(e, ui){
            _fixInvisibleLayouts(ui.item.closest('table'));
          },
          sort: function(e, ui){
            ui.item.addClass('active-item-shadow');
          },
          stop: function(e, ui){
            ui.item.removeClass('active-item-shadow');
            // highlight the row on drop to indicate an update
            ui.item.children('td').effect('highlight', {}, 1000);
          },
          update: function(e, ui){
            if(ui.item.closest('table').hasClass('ui-sortable-ajax')){
                // Get the row IDs in order...
                var zIDs = cvApp._getDraggableTableRowIDsArray($sortTable);
                // BUGBUG TBD : Block further dragging until response???  With timeout to reload?
                cvApp._putDraggableTableRowIDsArray(zIDs);
            }
          }
        });
    });

    $('body').on('click', 'table .ui-sortable .cvReorder', function(ev){
        var $row = $(ev.target).closest('tr'),
            $target = (!$(ev.target).hasClass('cvReorder')) ? $(ev.target).closest('a') : $(ev.target);
        if($target.hasClass('cvReorderUp')){
            // Move UP
            $row.prev().before($row);
        }
        else{
            // Move Down
            $row.next().after($row);
        }
        if($row.closest('table').hasClass('ui-sortable-ajax')){
            var zIDs = cvApp._getDraggableTableRowIDsArray($row.closest('table'));
            cvApp._putDraggableTableRowIDsArray(zIDs);
        }
        $row.children('td').effect('highlight', {}, 1000);
        ev.preventDefault();
    })

    //
    // Custom Tablesorter mm/yyyy dates - add parser through the tablesorter addParser method
    //
    $.tablesorter.addParser({
        // set a unique id to use as a className handle
        id: 'cvdates',
        is: function(s) {
            // return false so parser is not auto detected
            return false;
        },
        format: function(s, table, cell) {
            // format data-attr for normalization: columns will have YYYY, YYYY-MM, YYYY-MM-DD, '', or 'Present' (maybe other arbitrary strings also)
            if(typeof $(cell).find('span:first, a:first').data('cvDate') != 'undefined'){
                var sDate = $(cell).find('span:first, a:first').data('cvDate').toString();  // Force string...
                if(sDate.length > 0){
                    if(!((sDate).indexOf('-') >= 0)){sDate = sDate+'-01'}
                    return sDate.replace('-', '');
                }
            }
            return s;
        },
        // set type: text for sort algo
        type: 'text'
    });

    //
    // On Load, give all other tables column sorting (not the draggable ones above)
    //
    var zSortTables = $('table.cv-clientsort');
    for(i=0;i<zSortTables.length;i++){
        var count = $(zSortTables[i]).find('tbody:first tr').length;
        if(count > 1){
            $(zSortTables[i]).tablesorter({
            theme: 'bootstrap'
            })
            .bind('sortEnd', function(e,t){
                var $table = $(t);
                if($table.hasClass('ui-sortable')){
                    // BUGBUG: We probably need to be UX blocking the drag & drop & re-ordering during POST..
                    var zIDs = cvApp._getDraggableTableRowIDsArray($table);
                    cvApp._putDraggableTableRowIDsArray(zIDs);
                }
            });
        }
        else{
            // Hid other sort-type UXs...
            $(zSortTables[i]).find('.cv-row-sort-controls').hide();
        }
    };
});