var voted={};var flash_close=true;function flash(b,a,c){flash_close=!a;$("#flash").html(b).slideDown("slow").attr("title",flash_close?"Click to dismiss":"");if(!c){$.scrollTo("flash")}}function require_login(){if(!logged_in){flash('You must <a href="'+login_url+'">log in</a> to do that.')}if(banned){flash("Sorry, but you have been blocked from doing that.")}return !logged_in||banned}function ri(){$("#reportform").ajaxForm({success:function(){flash("Quote reported")},beforeSubmit:function(){flash('<img src="/img/ajax-loader.gif" alt="Loading..." />')}})}function cf(){$("#flash").slideUp("slow")}$(function(){$("#flash").click(function(){if(flash_close){$(this).slideUp("slow")}});function b(e,c,d){if(c>1||c<-1){return false}$.post("/quote/rate/"+e,{rating:c},d,"json");return true}function a(c,e,d){if(require_login()){return false}c.fadeOut("slow");return b(e,d,function(f){c.html(f.toString());c.fadeIn("slow")})}$q=$("#q");$q.addClass("s-inactive");$q.blur(function(){if(this.value===""){this.value="Search";$(this).addClass("s-inactive")}});$q.focus(function(){$(this).removeClass("s-inactive");if(this.value==="Search"){this.value=""}});$(".u").click(function(){$this=$(this);$parent=$this.parent(".rating");$count=$this.next("p").children(".cnt");id=$parent.attr("id").substring(6);if(voted[id]==1){return}else{if(voted[id]==-1){return;$parent.children(".du").removeClass("du");voted[id]=0;$count.html(parseInt($count.html())+1);return}}if(a($count,id,1)){$this.addClass("uu");voted[id]=1}});$(".d").click(function(){$this=$(this);$parent=$this.parent(".rating");$count=$this.prev("p").children(".cnt");id=$parent.attr("id").substring(6);if(voted[id]==-1){return}else{if(voted[id]==1){return;$parent.children(".uu").removeClass("uu");voted[id]=0;$count.html(parseInt($count.html())-1);return}}if(a($count,id,-1)){$this.addClass("du");voted[id]=-1}});$(".report").click(function(){if(require_login()){return false}flash('<img src="/img/ajax-loader.gif" alt="Loading..." />',true);id=$(this).parent(".rating").attr("id").substring(6);$("#flash").load("/report/new/"+id)});$(".delete").click(function(){id=$(this).parent(".rating").attr("id").substring(6);flash('Are you sure you want to <a href="/quote/delete/'+id+'">delete</a> this quote?')})});