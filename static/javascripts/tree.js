/* jquery treeview for Djangosms cvs location data
 * @Author  Mugisha Moses
 */

var parent={};
var children={};
$(document).ready( function() {

	expand_collapse();
	select_deselect();	
});
//
// expand and collapse

function expand_collapse(){
	$("#tree").find('input').each(function(){
		
			var id=$(this)[0].id;
			var input=$(this);
			$("#anchor_"+$(this)[0].id).click(function(){
				if ($('#'+children[parseInt(id)][0]).parent().is(":hidden"))
				{
					
				$('#'+id).parent().show();	
				
				 $(children[parseInt(id)]).each(function(key,val){
					 $('#'+val).parent().show()});
				}
				else {
					
					 $(children[parseInt(id)]).each(function(key,val){
						 $('#'+val).parent().hide();
						 });
				}
			});
			
	}	
			);}

function select_deselect(){
	$("#tree").find('input').each(function(){
		$(this).change(function(){
			var id=$(this)[0].id
			 if(!$(this).attr("checked"))
			    {
				  
				 deselect(id);
			        
			    }
			 else{
				 select(id); 
			 }
		});	
	});
}
	
function select(id){
	
	$(children[parseInt(id)]).each(function(key,val){
		
		$('#'+val).attr('checked', true);
		
		select(val);
	});
		}
function deselect(id){
	
	
	
	$(children[parseInt(id)]).each(function(key,val){
		$('#'+val).attr('checked', false);
		
		
		
		deselect(val);
	});
	deselect_parents(parent[parseInt(id)]);
}

function deselect_parents(id)
{
	$('#'+id).attr('checked', false);
	if(parent[parseInt(id)])
	{
		deselect_parents(parent[parseInt(id)]);
	}
	
}
