/* function to delete node dynamically */


function node_delete(area_id) {
    $.ajax({
        type: "GET",
        url:"/simple_locations/delete/" + area_id,
        dataType: "html",
        success: function(data) {
            //location.reload();
             $('.scrollable').html(data);
        }
    });
}

function reload_tree(){
    var e = new Date().getTime();
    var url = "/simple_locations/render_tree/"+"?" + e;

    $.ajax({
        type: "GET",
        url:url,
        dataType: "html",
        success: function(data) {

             $('.scrollable').html(data);

        }  ,

    });


}
function add_node(area_id) {
    {
        $.ajax({
            type: "GET",
            url:"/simple_locations/edit/" + area_id + "/?new=true",
            dataType: "json",
            success: function(data) {
                reload_tree();
                var point = new GLatLng(parseFloat(data['lat']), parseFloat(data['lon']));
                $('#id_name')[0].value = data['name'];
                $('#id_code')[0].value = data['code'];
                $('#id_pk')[0].value = data['pk'];
                map.setCenter(point, 4);
                $('#edit_submit').attr('disabled', false);
                $('#edit_submit').attr('value', 'save');
            }
        });
    }


}
function edit(area_id) {
    var e = new Date().getTime(0);
    var url = "/simple_locations/edit/" + area_id + "/?" + e;
    $.ajax({
        type: "GET",
        url:url,
        dataType: "json",
        success: function(data) {
            var point = new GLatLng(parseFloat(data['lat']), parseFloat(data['lon']));
            $('#id_name')[0].value = data['name'];
            $('#id_code')[0].value = data['code'];
            $('#id_pk')[0].value = data['pk'];
            map.setCenter(point, 4);
            $('#edit_submit').attr('disabled', false);


        }
    });
}
jQuery(function($) {
    //generic comfirm
    $(".confirm").click(function() {
        if (confirm("Are you sure?")) {
            if ($(this).hasClass('delete')) {
                eval($(this).attr('del_func'));
                return false;
            }


            // go ahead
        } else {

            return false;
        }
    });


    $('.point').change(function() {

        var point = new GLatLng(parseFloat($('#lat')[0].value), parseFloat($('#lon')[0].value));
        map.setCenter(point, 4);
    }

            );

    $('form[data-remote=true]').live('submit', function() {
        url = this.action;
        type = this.method;
        data = $(this).serialize();

        $.ajax({
            type: type,
            url:url,
            dataType: "html",
            data:data,
            success: function(data) {
               $('.scrollable').load('/simple_locations/render_tree');

            }
        });

        return false;
    });


}
        );
